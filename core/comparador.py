"""
comparador.py — Lógica de comparación entre datos de Sunrun y HubSpot.

Recibe dos dicts (uno por fuente) y devuelve un resultado estructurado
que clasifica cada campo en una de cuatro categorías:
  · "igual"       → mismo valor en ambas fuentes
  · "diferente"   → valores distintos en cada fuente
  · "solo_hs"     → solo existe en HubSpot (Sunrun no lo tiene)
  · "solo_sunrun" → solo existe en Sunrun (HubSpot no lo tiene)

Este módulo es puro Python sin dependencias externas: solo recibe datos
y devuelve el análisis. Toda la lógica de extracción vive en sus módulos
correspondientes ( api.py y scraping_sunrun.py).
"""

import re
from rapidfuzz import fuzz
from data.api import HubSpotAPI, _buscar_fsd_por_id_cliente

# ══════════════════════════════════════════════════════════════════════
#  Helpers de normalización
# ══════════════════════════════════════════════════════════════════════


def _norm(texto: str) -> str:
    """
    Normaliza un texto para comparación:
      - MAYÚSCULAS
      - sin tildes
      - sin espacios dobles
      - sin puntuación extra

    Así "María" y "Maria" o "SAN JUAN" y "San Juan" se consideran iguales.
    """
    if not texto or texto.strip() in ("No encontrado", "No detectado", ""):
        return ""

    reemplazos = str.maketrans("áéíóúüñàèìòùÁÉÍÓÚÜÑ", "AEIOUUNAEIOUAEIOUUN")
    texto = texto.translate(reemplazos)
    texto = texto.upper().strip()
    texto = re.sub(r"\s{2,}", " ", texto)
    texto = re.sub(r"[.,;:'\"]", "", texto)
    return texto


def _comparar_nombres(valor_hs: str, valor_sr: str, umbral: float = 0.70) -> dict:
    """
    Compara nombres usando lógica token-based con rapidfuzz.
    Maneja nombres hispanos con segundos apellidos opcionales.
    """
    na = _norm(valor_hs)
    nb = _norm(valor_sr)

    # NUEVO: Normalizar separadores como espacios antes de tokenizar
    na = re.sub(r"[-/\\|]+", " ", na)
    nb = re.sub(r"[-/\\|]+", " ", nb)

    # Coincidencia exacta post-normalización
    if na == nb:
        return {"similitud": 1.0, "estado": "igual", "nota": "Coinciden exactamente."}

    tokens_a = set(na.split())
    tokens_b = set(nb.split())

    # Token containment: todos los tokens del nombre más corto
    # están presentes en el nombre más largo
    shorter_tokens = tokens_a if len(tokens_a) <= len(tokens_b) else tokens_b
    longer_tokens = tokens_b if len(tokens_a) <= len(tokens_b) else tokens_a

    if shorter_tokens and shorter_tokens.issubset(longer_tokens):
        # Puntaje basado en qué proporción de tokens únicos coinciden
        overlap_ratio = len(shorter_tokens) / max(len(tokens_a | tokens_b), 1)
        sim = max(overlap_ratio, 0.85)
        return {
            "similitud": sim,
            "estado": "similar",
            "nota": (
                "Posible coincidencia: todos los tokens del nombre más corto "
                "están contenidos en el nombre más largo."
            ),
        }

    # Usar rapidfuzz con múltiples métricas token-based
    token_set = fuzz.token_set_ratio(na, nb) / 100.0
    token_sort = fuzz.token_sort_ratio(na, nb) / 100.0
    partial = fuzz.partial_ratio(na, nb) / 100.0
    wratio = fuzz.WRatio(na, nb) / 100.0

    best = max(token_set, token_sort, partial, wratio)

    if best >= 0.85:
        return {
            "similitud": best,
            "estado": "similar",
            "nota": f"Alta similitud en nombres ({best:.0%}).",
        }
    else:
        return {
            "similitud": best,
            "estado": "diferente",
            "nota": f"Nombres distintos ({best:.0%}).",
        }


def _similitud(a: str, b: str) -> float:
    """
    Devuelve un valor entre 0.0 y 1.0 indicando qué tan similares son
    dos strings (1.0 = idénticos, 0.0 = completamente distintos).

    Útil para detectar errores tipográficos leves (ej: "Cruz" vs "Gruz").
    """
    return fuzz.ratio(_norm(a), _norm(b)) / 100.0


def _vacio(valor: str) -> bool:
    """Devuelve True si el valor es vacío, None o un placeholder de error."""
    return not valor or _norm(valor) == ""


def _normalizar_telefono(telefono: str) -> str:
    """
    Normaliza un número de teléfono removiendo todo carácter no numérico
    y el código de país '1' inicial si está presente.

    Ejemplos:
        "+17872979317"      → "7872979317"
        "(787)297-9317"     → "7872979317"
        "787-297-9317"      → "7872979317"
        "1-787-297-9317"    → "7872979317"
    """
    if not telefono:
        return ""
    # Eliminar todos los caracteres no numéricos
    limpio = re.sub(r"[^0-9]", "", telefono)
    # Eliminar el código de país "1" al inicio si da 11 dígitos
    if len(limpio) == 11 and limpio.startswith("1"):
        limpio = limpio[1:]
    return limpio


# ══════════════════════════════════════════════════════════════════════
#  Lógica de comparación
# ══════════════════════════════════════════════════════════════════════

# Umbral de similitud para considerar dos valores como "similares" en vez de
# "iguales". Por ejemplo 0.85 permite pequeñas diferencias tipográficas.
UMBRAL_SIMILAR = 0.85

# Conjunto de campos que representan números de teléfono.
# Se comparan usando _normalizar_telefono() en lugar de _norm() genérico.
CAMPOS_TELEFONO = {"Telefono", "Telefono Alterno"}

# Agregar a la clase Comparador


def buscar_hubspot_por_estrategia(self, criterio, tipo_busqueda):
    """
    Envuelve la búsqueda de api.py
    """
    return self.api.buscar_contactos_por_criterio(criterio, tipo_busqueda)


def extraer_fsd_desde_candidato(self, candidato_hubspot):
    """
    Extrae el FSD de un candidato HubSpot.

    Estrategia de búsqueda:
    1. Si el candidato tiene campo 'fsd' directo → usarlo
    2. Si tiene 'id_cliente' → buscar FSD en tickets por id_goformz
    3. Si nada → devolver vacío
    """
    if not isinstance(candidato_hubspot, dict):
        return ""

    # Intentar 1: FSD directo en el candidato
    fsd = (
        candidato_hubspot.get("fsd")
        or candidato_hubspot.get("fsd__", "")
        or candidato_hubspot.get("properties", {}).get("fsd__", "")
        or candidato_hubspot.get("properties", {}).get("fsd_codigo", "")
    )

    if fsd:
        return str(fsd).strip()

    # Intentar 2: Buscar FSD por id_cliente usando la función probada
    id_cliente = candidato_hubspot.get("id_cliente") or candidato_hubspot.get(
        "properties", {}
    ).get("id_de_goformz__contacto_", "")

    if id_cliente and str(id_cliente).strip():
        try:
            # ✅ CORRECCIÓN: Usar _buscar_fsd_por_id_cliente que ya existe
            # y está diseñada para esto (maneja validación y errores)
            fsd = _buscar_fsd_por_id_cliente(str(id_cliente).strip())
            if fsd:
                return fsd
        except Exception as e:
            # Log silencioso, pero no romper
            print(f"[DEBUG] Error buscando FSD por id_cliente={id_cliente}: {e}")

    return ""


def comparar_con_fsd_automatico(self, candidato_hubspot):
    """
    Versión mejorada de comparar() que extrae FSD automáticamente,
    obtiene los datos completos de HubSpot y luego busca los datos de Sunrun.
    """
    fsd = self.extraer_fsd_desde_candidato(candidato_hubspot)

    if not fsd:
        return {"error": "No se pudo extraer FSD del candidato"}

    if not isinstance(candidato_hubspot, dict):
        return {"error": "Candidato HubSpot inválido."}

    try:
        from scraping_sunrun import ScraperSunrun
    except ImportError as e:
        return {"error": f"No se pudo cargar ScraperSunrun: {e}"}

    from data.api import extraer_datos_hubspot

    # Si el candidato vino de búsqueda por contacto ya tiene los campos
    # poblados (nombre, direccion, telefono, etc.). Usarlos directamente
    # evita una segunda búsqueda que puede fallar si el FSD del ticket no
    # coincide exactamente con el extraído.
    if candidato_hubspot.get("contact_id") and not candidato_hubspot.get("ticket_id"):
        # Construir datos_hs desde el candidato que ya tenemos
        datos_hs = {
            "fsd": fsd,
            "ticket_id": None,
            "contact_id": candidato_hubspot.get("contact_id"),
            "nombre": candidato_hubspot.get("nombre", ""),
            "id_cliente": candidato_hubspot.get("id_cliente", ""),
            "direccion": candidato_hubspot.get("direccion", ""),
            "telefono": candidato_hubspot.get("telefono", ""),
            "telefono_alterno": candidato_hubspot.get("telefono_alterno", ""),
            "email": candidato_hubspot.get("email", ""),
            "estado": candidato_hubspot.get("estado", ""),
            "municipio": candidato_hubspot.get("municipio", ""),
            "zip": candidato_hubspot.get("zip", ""),
            "nota": "",
            "fuente_nombre": "",
            "fuente_id": "",
            "error": None,
        }
        # Intentar enriquecer con datos del ticket (puede añadir campos que
        # el contacto no tenía, como nota o telefono_alterno del ticket)
        try:
            datos_ticket = extraer_datos_hubspot(fsd)
            if not datos_ticket.get("error"):
                # Preferir datos del contacto (ya los tenemos) pero completar
                # campos vacíos con lo que venga del ticket
                for campo in ("telefono_alterno", "nota", "municipio", "estado", "zip"):
                    if not datos_hs.get(campo) and datos_ticket.get(campo):
                        datos_hs[campo] = datos_ticket[campo]
        except Exception:
            pass  # Si falla el enriquecimiento, seguimos con lo que tenemos
    else:
        # Búsqueda original por FSD: traer todo desde el ticket
        datos_hs = extraer_datos_hubspot(fsd)
        if datos_hs.get("error"):
            return {"error": datos_hs["error"]}

    scraper = ScraperSunrun()
    datos_sr = scraper.obtener_datos_por_fsd(fsd)

    if datos_sr.get("error"):
        return {"error": f"Sunrun: {datos_sr['error']}"}

    resultado = comparar(datos_hs, datos_sr)
    resultado["fsd"] = fsd
    resultado["_sunrun_extra"] = {
        "dispatch_state": datos_sr.get("dispatch_state", ""),
        "appointment_date": datos_sr.get("appointment_date", ""),
        "case_reason": datos_sr.get("case_reason", ""),
    }
    return resultado


def comparar_campo(campo: str, valor_hs: str, valor_sunrun: str) -> dict:
    """
    Compara un campo individual entre HubSpot y Sunrun.

    Retorna un dict con:
      · campo       : nombre del campo
      · valor_hs    : valor en HubSpot (o "—" si vacío)
      · valor_sr    : valor en Sunrun (o "—" si vacío)
      · estado      : "igual", "similar", "diferente", "solo_hs", "solo_sunrun", "ambos_vacios"
      · similitud   : float entre 0.0 y 1.0
      · nota        : mensaje descriptivo
    """
    hs_vacio = _vacio(valor_hs)
    sr_vacio = _vacio(valor_sunrun)

    # Caso: ambos vacíos
    if hs_vacio and sr_vacio:
        return {
            "campo": campo,
            "valor_hs": "—",
            "valor_sr": "—",
            "estado": "ambos_vacios",
            "similitud": 1.0,
            "nota": "Ninguna fuente tiene este dato.",
        }

    # Caso: solo HubSpot tiene el dato
    if not hs_vacio and sr_vacio:
        return {
            "campo": campo,
            "valor_hs": valor_hs,
            "valor_sr": "—",
            "estado": "solo_hs",
            "similitud": 0.0,
            "nota": "Solo disponible en HubSpot.",
        }

    # Caso: solo Sunrun tiene el dato
    if hs_vacio and not sr_vacio:
        return {
            "campo": campo,
            "valor_hs": "—",
            "valor_sr": valor_sunrun,
            "estado": "solo_sunrun",
            "similitud": 0.0,
            "nota": "Solo disponible en Sunrun.",
        }

    # Ambos tienen dato: calcular similitud
    sim = _similitud(valor_hs, valor_sunrun)

    # Para nombres, usar lógica token-based especializada (tolera
    # diferencias de mayúsculas, segundos apellidos faltantes, etc.)
    if campo == "Nombre":
        nombre_result = _comparar_nombres(valor_hs, valor_sunrun)
        sim = nombre_result["similitud"]
        estado = nombre_result["estado"]
        nota = nombre_result["nota"]
    # Para campos de teléfono, normalizar con _normalizar_telefono()
    elif campo in CAMPOS_TELEFONO:
        if _normalizar_telefono(valor_hs) == _normalizar_telefono(valor_sunrun):
            estado = "igual"
            sim = 1.0
            nota = "Coinciden exactamente."
        elif sim >= UMBRAL_SIMILAR:
            estado = "similar"
            nota = (
                f"Valores muy similares (similitud {sim:.0%}). Verificar manualmente."
            )
        else:
            estado = "diferente"
            nota = f"Valores distintos (similitud {sim:.0%})."
    else:
        if _norm(valor_hs) == _norm(valor_sunrun):
            estado = "igual"
            nota = "Coinciden exactamente."
        elif sim >= UMBRAL_SIMILAR:
            estado = "similar"
            nota = (
                f"Valores muy similares (similitud {sim:.0%}). Verificar manualmente."
            )
        else:
            estado = "diferente"
            nota = f"Valores distintos (similitud {sim:.0%})."

    return {
        "campo": campo,
        "valor_hs": valor_hs,
        "valor_sr": valor_sunrun,
        "estado": estado,
        "similitud": sim,
        "nota": nota,
    }


def comparar(datos_hubspot: dict, datos_sunrun: dict) -> dict:
    """
    Compara todos los campos disponibles entre HubSpot y Sunrun.

    Los campos se dividen en dos grupos:
      · Campos compartidos: existen en ambas fuentes y se comparan.
      · Campos exclusivos: solo existen en una fuente, se muestran como
        "solo_hs" o "solo_sunrun" directamente sin comparación.

    Parámetros
    ----------
    datos_hubspot : dict con datos de HubSpot ( api.py)
    datos_sunrun  : dict con datos de Sunrun  (scraping_sunrun.py)

    Devuelve
    --------
    dict con:
      fsd         : número FSD analizado
      campos      : lista de dicts (uno por campo), resultado de comparar_campo()
      resumen     : dict con conteos por estado
      tiene_error : bool — True si alguna fuente reportó error
      errores     : lista de mensajes de error de cada fuente
    """
    fsd = datos_hubspot.get("fsd", datos_sunrun.get("fsd", "desconocido"))

    # Recopilar errores de las fuentes
    errores = []
    if datos_hubspot.get("error"):
        errores.append(f"HubSpot: {datos_hubspot['error']}")
    if datos_sunrun.get("error"):
        errores.append(f"Sunrun: {datos_sunrun['error']}")

    # ── Campos comparables (existen en ambas fuentes) ─────────────────
    # clave_hs, clave_sr, etiqueta_visible
    CAMPOS_COMPARABLES = [
        ("nombre", "nombre", "Nombre"),
        ("id_cliente", "id_cliente", "ID Cliente"),
        ("direccion", "direccion", "Direccion"),
        ("telefono", "telefono", "Telefono"),
        ("telefono_alterno", "telefono_movil", "Telefono Alterno"),
        ("email", "email", "Email"),
        ("estado", "estado_pr", "Pais"),
        ("municipio", "ciudad", "Ciudad / Municipio"),
        ("zip", "codigo_postal", "Codigo Postal"),
    ]

    # ── Campos exclusivos de Sunrun (HubSpot no los tiene) ────────────
    # clave_sr, etiqueta_visible
    # IMPORTANTE: las claves deben coincidir exactamente con las que
    # devuelve scraping_sunrun.py en su dict de resultado:
    #   direccion, telefono, telefono_movil, email,
    #   estado_pr, condado, ciudad, codigo_postal
    CAMPOS_SOLO_SUNRUN = [
        ("condado", "Municipio"),
    ]

    resultados_campos = []
    resumen = {
        "igual": 0,
        "similar": 0,
        "diferente": 0,
        "solo_hs": 0,
        "solo_sunrun": 0,
        "ambos_vacios": 0,
    }

    # Comparar campos compartidos
    for clave_hs, clave_sr, etiqueta in CAMPOS_COMPARABLES:
        val_hs = datos_hubspot.get(clave_hs, "")
        val_sr = datos_sunrun.get(clave_sr, "")
        resultado = comparar_campo(etiqueta, val_hs, val_sr)
        resultados_campos.append(resultado)
        resumen[resultado["estado"]] = resumen.get(resultado["estado"], 0) + 1

    # Agregar campos exclusivos de Sunrun
    for clave_sr, etiqueta in CAMPOS_SOLO_SUNRUN:
        val_sr = datos_sunrun.get(clave_sr, "")
        if _vacio(val_sr):
            estado_directo = "ambos_vacios"
            nota = "Ninguna fuente tiene este dato."
            val_sr_display = "—"
        else:
            estado_directo = "solo_sunrun"
            nota = "Solo disponible en Sunrun."
            val_sr_display = val_sr

        resultado = {
            "campo": etiqueta,
            "valor_hs": "—",
            "valor_sr": val_sr_display,
            "estado": estado_directo,
            "similitud": 0.0,
            "nota": nota,
        }
        resultados_campos.append(resultado)
        resumen[estado_directo] = resumen.get(estado_directo, 0) + 1

    return {
        "fsd": fsd,
        "campos": resultados_campos,
        "resumen": resumen,
        "tiene_error": bool(errores),
        "errores": errores,
    }


# ══════════════════════════════════════════════════════════════════════
#  Helper para construir datos de HubSpot desde el resultado de  api.py
# ══════════════════════════════════════════════════════════════════════


def datos_hs_desde_ticket(ticket_dict: dict) -> dict:
    """
    Adapta el dict devuelto por  api.extraer_datos_hubspot() al formato
    interno que usa comparar(). Todas las claves se pasan directamente;
    se garantiza que existan con valor vacío si faltaran.
    """
    campos = (
        "fsd",
        "ticket_id",
        "contact_id",
        "nombre",
        "id_cliente",
        "direccion",
        "telefono",
        "telefono_alterno",
        "email",
        "estado",
        "municipio",
        "zip",
        "nota",
        "fuente_nombre",
        "fuente_id",
    )
    resultado = {c: ticket_dict.get(c, "") or "" for c in campos}
    resultado["fuente"] = "HubSpot"
    resultado["error"] = ticket_dict.get("error", None)
    return resultado


class Comparador:
    """Encapsula las operaciones de búsqueda y comparación usadas por la UI."""

    def __init__(self):
        self.api = HubSpotAPI()

    def buscar_hubspot_por_estrategia(self, criterio, tipo_busqueda):
        return self.api.buscar_contactos_por_criterio(criterio, tipo_busqueda)

    def extraer_fsd_desde_candidato(self, candidato_hubspot):
        return extraer_fsd_desde_candidato(self, candidato_hubspot)

    def comparar_con_fsd_automatico(self, candidato_hubspot):
        return comparar_con_fsd_automatico(self, candidato_hubspot)

    def comparar(self, datos_hubspot: dict, datos_sunrun: dict) -> dict:
        return comparar(datos_hubspot, datos_sunrun)
