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
correspondientes (api2.py y scraping_sunrun.py).
"""

import re
from difflib import SequenceMatcher

# ══════════════════════════════════════════════════════════════════════
#  Helpers de normalización
# ══════════════════════════════════════════════════════════════════════


def _norm(texto: str) -> str:
    """
    Normaliza un texto para comparación:
      - minúsculas
      - sin tildes
      - sin espacios dobles
      - sin puntuación extra

    Así "María" y "Maria" o "SAN JUAN" y "San Juan" se consideran iguales.
    """
    if not texto or texto.strip() in ("No encontrado", "No detectado", ""):
        return ""

    reemplazos = str.maketrans("áéíóúüñàèìòùÁÉÍÓÚÜÑ", "aeiouunaeioaAEIOUUN")
    texto = texto.translate(reemplazos)
    texto = texto.lower().strip()
    texto = re.sub(r"\s{2,}", " ", texto)
    texto = re.sub(r"[.,;:'\"]", "", texto)
    return texto


def _similitud(a: str, b: str) -> float:
    """
    Devuelve un valor entre 0.0 y 1.0 indicando qué tan similares son
    dos strings (1.0 = idénticos, 0.0 = completamente distintos).

    Útil para detectar errores tipográficos leves (ej: "Cruz" vs "Gruz").
    """
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _vacio(valor: str) -> bool:
    """Devuelve True si el valor es vacío, None o un placeholder de error."""
    return not valor or _norm(valor) == ""


# ══════════════════════════════════════════════════════════════════════
#  Lógica de comparación
# ══════════════════════════════════════════════════════════════════════

# Umbral de similitud para considerar dos valores como "similares" en vez de
# "iguales". Por ejemplo 0.85 permite pequeñas diferencias tipográficas.
UMBRAL_SIMILAR = 0.85


def comparar_campo(campo: str, valor_hs: str, valor_sunrun: str) -> dict:
    """
    Compara el valor de un campo entre HubSpot y Sunrun.

    Parámetros
    ----------
    campo       : nombre del campo (ej: "nombre", "id_cliente", "municipio")
    valor_hs    : valor obtenido desde HubSpot
    valor_sunrun: valor obtenido desde Sunrun

    Devuelve
    --------
    dict con:
      campo      : nombre del campo
      valor_hs   : valor de HubSpot (original, sin normalizar)
      valor_sr   : valor de Sunrun (original)
      estado     : "igual" | "similar" | "diferente" | "solo_hs" | "solo_sunrun" | "ambos_vacios"
      similitud  : float entre 0.0 y 1.0
      nota       : string descriptivo para mostrar en la UI
    """
    hs_vacio = _vacio(valor_hs)
    sr_vacio = _vacio(valor_sunrun)

    # Caso: ambos vacíos
    if hs_vacio and sr_vacio:
        return {
            "campo": campo,
            "valor_hs": valor_hs or "—",
            "valor_sr": valor_sunrun or "—",
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

    if _norm(valor_hs) == _norm(valor_sunrun):
        estado = "igual"
        nota = "Coinciden exactamente."
    elif sim >= UMBRAL_SIMILAR:
        estado = "similar"
        nota = f"Valores muy similares (similitud {sim:.0%}). Verificar manualmente."
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
    datos_hubspot : dict con datos de HubSpot (api2.py)
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
        ("nombre", "nombre", "Nombre del cliente"),
        (
            "id_cliente",
            "id_cliente",
            "ID del cliente",
        ),  # Sunrun → siempre "No encontrado"
        ("municipio", "municipio", "Ciudad / Municipio"),
    ]

    # ── Campos exclusivos de Sunrun (HubSpot no los tiene) ────────────
    # clave_sr, etiqueta_visible
    CAMPOS_SOLO_SUNRUN = [
        ("direccion", "Dirección"),
        ("telefono", "Teléfono principal"),
        ("movil", "Teléfono móvil"),
        ("email", "Email"),
        ("estado", "Estado (State)"),
        ("county", "County"),
        ("zip_code", "Zip Code"),
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
#  Helper para construir datos de HubSpot desde el resultado de api2.py
# ══════════════════════════════════════════════════════════════════════


def datos_hs_desde_ticket(ticket_dict: dict) -> dict:
    """
    Adapta el formato de salida de api2.py al formato que espera comparar().

    api2.py devuelve:
      {"fsd": "983316", "nombre": "David Cruz", "id_cliente": "250630",
       "municipio": "San Juan", "ticket_id": "..."}

    Esta función lo normaliza y agrega la clave 'error' si no está.
    """
    return {
        "fsd": ticket_dict.get("fsd", ""),
        "nombre": ticket_dict.get("nombre", ""),
        "id_cliente": ticket_dict.get("id_cliente", ""),
        "municipio": ticket_dict.get("municipio", ""),
        "fuente": "HubSpot",
        "error": ticket_dict.get("error", None),
    }
