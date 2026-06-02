"""
Módulo 3 — Captura de celdas de Google Sheets con Playwright.

Navega a una hoja de Google Sheets, localiza celdas visualmente por su
referencia A1 y captura únicamente el área de cada celda.

Usa sesión persistente (storage_state) para evitar reautenticación.
Genera screenshots de depuración ante fallos de localización.
"""

from __future__ import annotations

import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from gsheets.utils.cell_parser import col_letter_to_index

# ── Logger ────────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────

_SESSION_DIR = Path(__file__).resolve().parent.parent / "sessions"
_SCREENSHOTS_DIR = Path(__file__).resolve().parent.parent / "screenshots"
_DEBUG_DIR = Path(__file__).resolve().parent.parent / "screenshots" / "debug"

# Selectores de Google Sheets (con fallbacks)
_GRID_SELECTORS = [
    "#waffle-grid-container",
    "#grid-container",
    '[class*="waffle"]',
]
_COL_HEADER_SELECTORS = [
    "#colheaders",
    "#column-headers",
    '[id*="colheader"]',
    '[class*="column-header"]',
]
_ROW_HEADER_SELECTORS = [
    "#rowheaders",
    "#row-headers",
    '[id*="rowheader"]',
    '[class*="row-header"]',
]

# Tiempos de espera (ms)
_LOAD_TIMEOUT = 20_000  # domcontentloaded debería ser rápido
_GRID_TIMEOUT = 30_000  # tiempo máximo esperando el grid
_RENDER_DELAY = 1_500  # delay inicial para render
_RETRY_DELAY = 2_000  # entre reintentos
_RETRY_INTERVAL = 500  # sondeo del grid
_MAX_GRID_RETRIES = 20  # ~10s de sondeo del grid


# ── Clase principal ───────────────────────────────────────────────────────────


class PlaywrightSheetsCapture:
    """
    Captura visual de celdas individuales de Google Sheets usando Playwright.

    Uso:
        async with PlaywrightSheetsCapture() as cap:
            await cap.capture_cell(SHEET_URL, "A3", "a3.png")
            await cap.capture_cells(SHEET_URL, ["A3", "F3", "A6", "F6"])

    Características:
        - Sesión persistente (cookies + localStorage) en gsheets/sessions/
        - Localización de celdas por columnas/filas del DOM (no hardcodeado)
        - Múltiples estrategias de fallback para selectores
        - Validación de que la pestaña correcta está cargada
        - Screenshots de depuración automáticos ante fallos
        - Soporte para headless y visible
    """

    _SESSION_FILE = _SESSION_DIR / "google_sheets_state.json"
    _PROFILE_DIR_DEFAULT = _SESSION_DIR / "chrome_profile"

    def __init__(
        self,
        headless: bool = True,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
        session_dir: str | Path | None = None,
        screenshots_dir: str | Path | None = None,
        debug_dir: str | Path | None = None,
        profile_dir: str | Path | None = None,
        log_callback: Callable[[str], None] | None = None,
    ) -> None:
        self._headless = headless
        self._viewport = {"width": viewport_width, "height": viewport_height}
        self._session_dir = Path(session_dir) if session_dir else _SESSION_DIR
        self._screenshots_dir = (
            Path(screenshots_dir) if screenshots_dir else _SCREENSHOTS_DIR
        )
        self._debug_dir = Path(debug_dir) if debug_dir else _DEBUG_DIR
        self._session_path = self._session_dir / "google_sheets_state.json"
        self._profile_dir = (
            Path(profile_dir) if profile_dir else self._session_dir / "chrome_profile"
        )
        self._use_persistent = (
            bool(profile_dir) or True
        )  # usar perfil persistente por defecto
        self._log = log_callback or (lambda msg: logger.info(msg))

        self._playwright: Any = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._auth_verified = False  # solo se verifica una vez por sesión

        # Aseguramos que existan los directorios
        self._session_dir.mkdir(parents=True, exist_ok=True)
        self._screenshots_dir.mkdir(parents=True, exist_ok=True)
        self._debug_dir.mkdir(parents=True, exist_ok=True)
        if self._use_persistent:
            self._profile_dir.mkdir(parents=True, exist_ok=True)

    # ── Context manager ───────────────────────────────────────────────────

    async def __aenter__(self) -> "PlaywrightSheetsCapture":
        await self.start()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.stop()

    # ── Start / Stop ──────────────────────────────────────────────────────

    _CDP_URL = "http://localhost:9222"

    async def start(self) -> None:
        """
        Inicia Playwright reutilizando la sesión de Chrome existente del proyecto.

        Estrategia (en orden):
          1. Conecta al Chrome con depuración remota en localhost:9222
             (el mismo que usa Selenium en core/browser.py con
              --remote-debugging-port=9222 y user-data-dir=C:\\chrome_sesion_ssauto).
             Si está corriendo, reutiliza directamente sus cookies y sesión de Google.
          2. Si no hay Chrome en el puerto 9222, lanza un nuevo navegador
             persistente usando el mismo directorio de perfil de Chrome del proyecto
             (C:\\chrome_sesion_ssauto) para heredar la sesión autenticada.
        """
        self._playwright = await async_playwright().start()

        # ── Intentar conectar al Chrome existente (estrategia 1) ────────
        try:
            self._browser = await self._playwright.chromium.connect_over_cdp(
                self._CDP_URL, timeout=5_000
            )
            self._context = self._browser.contexts[0]
            self._page = (
                self._context.pages[0]
                if self._context.pages
                else await self._context.new_page()
            )
            self._log("→ Playwright conectado al Chrome existente (puerto 9222).")
            self._log("→ Reutilizando sesión de Google autenticada del proyecto.")
            return
        except Exception:
            self._log(
                "· Chrome en puerto 9222 no detectado, abriendo nuevo navegador..."
            )

        # ── Fallback: lanzar perfil persistente con el user-data del proyecto ──
        try:
            from core.browser import CHROME_USER_DATA
        except ImportError:
            CHROME_USER_DATA = str(self._profile_dir)

        context_options = {
            "headless": self._headless,
            "viewport": self._viewport,
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        }

        self._context = await self._playwright.chromium.launch_persistent_context(
            user_data_dir=CHROME_USER_DATA,
            **context_options,
        )
        self._browser = None

        self._page = (
            self._context.pages[0]
            if self._context.pages
            else await self._context.new_page()
        )
        self._log(f"→ Playwright iniciado con perfil: {CHROME_USER_DATA}.")

    async def stop(self) -> None:
        """
        Cierra el navegador Playwright.

        Si se conectó vía CDP, solo desconecta (no cierra pestañas del usuario).
        Si se lanzó perfil persistente, cierra el contexto.
        """
        es_cdp = self._browser is not None

        if not es_cdp and self._context:
            await self._context.close()
            self._context = None

        if self._browser:
            await self._browser.close()
            self._browser = None

        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

        self._page = None
        self._log("→ Playwright detenido.")

    # ── Propiedades ───────────────────────────────────────────────────────

    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError(
                "Playwright no ha sido iniciado. Llame a start() primero."
            )
        return self._page

    # ── Captura de celda individual ───────────────────────────────────────

    async def capture_cell(
        self,
        sheet_url: str,
        cell_ref: str,
        output_path: str | None = None,
        sheet_gid: str | int = "0",
        expected_value: str | None = None,
    ) -> str:
        """
        Captura una celda individual como imagen PNG.

        Args:
            sheet_url: URL del spreadsheet (o ID).
            cell_ref: Referencia de celda (ej. "A3", "F6").
            output_path: Ruta de salida. Si no se da, se genera en screenshots/.
            sheet_gid: GID de la hoja (por defecto "0" = primera hoja).
            expected_value: Valor esperado de la celda según la API.
                            Se usa para validar que se capturó la celda correcta.

        Returns:
            Ruta absoluta de la imagen generada.

        Raises:
            RuntimeError: Si no se puede localizar la celda.
        """
        if output_path is None:
            output_path = str(self._screenshots_dir / f"{cell_ref.lower()}.png")

        output_path = str(Path(output_path).resolve())
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        spreadsheet_id = self._extract_spreadsheet_id(sheet_url)

        # ── Verificar autenticación de Google (solo una vez) ──────────
        if not self._auth_verified:
            await self._verify_google_auth()

        # ── Buscar si el spreadsheet ya está abierto, si no abrir nueva pestaña ─
        target_url = (
            f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
            f"/edit#gid={sheet_gid}&range={cell_ref}"
        )
        existing_page = await self._find_spreadsheet_page(spreadsheet_id)
        if existing_page:
            self._page = existing_page
            self._log(f"→ Spreadsheet {spreadsheet_id} ya abierto — reutilizando pestaña.")
        else:
            self._page = await self._open_new_page()
            self._log(f"→ Abriendo nueva pestaña: gid={sheet_gid}, celda {cell_ref}...")

        await self._page.bring_to_front()
        try:
            await self.page.goto(
                target_url, wait_until="domcontentloaded", timeout=_LOAD_TIMEOUT
            )
        except Exception as e:
            self._log(f"⚠ goto timeout/error: {e}")
            await self.page.goto(target_url, wait_until="load", timeout=_LOAD_TIMEOUT)

        # ── Logs de diagnóstico post-navegación ───────────────────────
        current_url = self.page.url
        title = await self.page.title()
        self._log(f"· URL actual: {current_url[:150]}")
        self._log(f"· Título: {title[:100]}")

        # ── Validar que estamos en la página correcta ─────────────────
        await self._validate_page(spreadsheet_id, sheet_gid, cell_ref)

        # ── Esperar y verificar el grid con sondeo ────────────────────
        grid_ok = await self._wait_for_grid()
        if not grid_ok:
            await self._dump_debug_info("grid_not_found", cell_ref)
            raise RuntimeError(
                f"No se detectó el grid de Google Sheets para la celda {cell_ref}. "
                f"gid={sheet_gid}. Se generó screenshot de depuración."
            )

        # ── Localizar celda ───────────────────────────────────────────
        rect = await self._locate_cell(cell_ref)

        if rect is None:
            # Reintento con recarga completa
            self._log(f"· Reintentando localizar celda {cell_ref} (recarga)...")
            await asyncio.sleep(0.001 * _RETRY_DELAY)
            await self.page.reload(wait_until="domcontentloaded")
            await self._validate_page(spreadsheet_id, sheet_gid, cell_ref)
            grid_ok = await self._wait_for_grid()
            if not grid_ok:
                await self._dump_debug_info("grid_not_found_retry", cell_ref)
                raise RuntimeError(
                    f"No se detectó el grid tras recarga para {cell_ref}. "
                    f"gid={sheet_gid}."
                )
            rect = await self._locate_cell(cell_ref)

        if rect is None:
            await self._dump_debug_info("cell_not_found", cell_ref)
            raise RuntimeError(
                f"No se pudo localizar la celda {cell_ref} en gid={sheet_gid}. "
                f"Verifique que la celda exista en la pestaña seleccionada. "
                f"Se generó screenshot de depuración."
            )

        # ── Validar y refinar rect antes de capturar ──────────────────
        clip = await self._validate_and_refine_rect(
            cell_ref, rect, output_path, expected_value
        )

        # ── Capturar ──────────────────────────────────────────────────
        await self.page.screenshot(path=output_path, clip=clip)
        self._log(f"✓ Celda {cell_ref} capturada → {output_path}")
        return output_path

    async def capture_cells(
        self,
        sheet_url: str,
        cell_refs: list[str],
        output_dir: str | None = None,
        sheet_gid: str | int = "0",
        expected_values: dict[str, str | None] | None = None,
    ) -> dict[str, str]:
        """
        Captura múltiples celdas y retorna diccionario {ref: ruta_imagen}.

        Args:
            sheet_url: URL del spreadsheet.
            cell_refs: Lista de referencias (ej. ["A3", "F3", "A6", "F6"]).
            output_dir: Directorio de salida.
            sheet_gid: GID de la hoja.
            expected_values: Dict {ref: valor} con los valores de la API
                             para validar que se captura la celda correcta.
        """
        results: dict[str, str] = {}
        for ref in cell_refs:
            path = await self.capture_cell(
                sheet_url=sheet_url,
                cell_ref=ref,
                output_path=(
                    str(Path(output_dir) / f"{ref.lower()}.png") if output_dir else None
                ),
                sheet_gid=sheet_gid,
                expected_value=(expected_values.get(ref) if expected_values else None),
            )
            results[ref] = path
        return results

    async def _find_spreadsheet_page(self, spreadsheet_id: str) -> Page | None:
        """
        Busca si el spreadsheet ya está abierto en alguna pestaña del browser.
        Retorna la página si la encuentra, None si no.
        """
        if self._browser is None and self._context is None:
            return None

        pages: list[Page] = []
        try:
            if self._browser:
                for ctx in self._browser.contexts:
                    pages.extend(ctx.pages)
            elif self._context:
                pages = self._context.pages
        except Exception:
            pass

        for page in pages:
            try:
                url = page.url
                if spreadsheet_id in url:
                    return page
            except Exception:
                continue

        return None

    async def _open_new_page(self) -> Page:
        """Abre una nueva pestaña en el browser existente o en el contexto."""
        if self._browser:
            for ctx in self._browser.contexts:
                if ctx.pages:
                    page = await ctx.new_page()
                    await page.bring_to_front()
                    return page
        if self._context:
            page = await self._context.new_page()
            await page.bring_to_front()
            return page
        raise RuntimeError("No hay browser ni contexto activo para abrir una pestaña.")

    async def _validate_page(
        self, spreadsheet_id: str, sheet_gid: str | int, cell_ref: str
    ) -> None:
        """
        Verifica que Playwright esté realmente en Google Sheets.

        Si detecta redirección al login de Google (accounts.google.com),
        lanza un error explícito para que el usuario autentique manualmente.

        Raises:
            RuntimeError: Si la página actual es el login de Google.
        """
        title = await self.page.title()
        current_url = self.page.url

        # ── Detectar login de Google ──────────────────────────────────
        is_login_url = "accounts.google.com" in current_url
        is_login_title = "sign in" in title.lower() or "iniciar sesión" in title.lower()
        is_google_com = (
            current_url.startswith("https://www.google.com")
            and "spreadsheets" not in current_url
        )

        if is_login_url or is_login_title or is_google_com:
            await self._dump_debug_info("login_redirect", cell_ref)
            raise RuntimeError(
                "✗ Playwright fue redirigido a la pantalla de login de Google.\n"
                "   La sesión no está autenticada o expiró.\n\n"
                "   Solución:\n"
                "   1. Ejecuta con headless=False\n"
                "   2. Inicia sesión manualmente en Google en la ventana del navegador\n"
                "   3. Cierra la app normalmente (la sesión se guarda en el perfil)\n"
                "   4. Vuelve a ejecutar — la sesión se reutilizará automáticamente.\n\n"
                f"   URL actual: {current_url}\n"
                f"   Título: {title}"
            )

        # ── Validar que estamos en el spreadsheet correcto ────────────
        is_sheets = "docs.google.com/spreadsheets" in current_url
        has_gid = (
            f"gid={sheet_gid}" in current_url or f"#gid={sheet_gid}" in current_url
        )

        self._log(
            f"· Página: title='{title[:80]}', "
            f"sheets={is_sheets}, gid_match={has_gid}"
        )

        if not is_sheets:
            self._log(f"⚠ URL no es Google Sheets: {current_url[:120]}")

        if not has_gid:
            self._log(
                f"⚠ El gid={sheet_gid} no aparece en la URL. "
                f"Posible redirección. URL: {current_url[:120]}"
            )

    # ── Verificación de autenticación Google ───────────────────────────────

    async def _verify_google_auth(self) -> None:
        """
        Verifica que la sesión de Google esté autenticada.

        Abre una pestaña TEMPORAL en myaccount.google.com para no
        reemplazar pestañas existentes. Si la URL se mantiene en
        myaccount, la sesión está activa. Si redirige a
        accounts.google.com, la sesión expiró o nunca se autenticó.

        Solo se ejecuta una vez por ciclo de vida del navegador.
        """
        self._log("→ Verificando autenticación de Google...")
        temp_page = None
        try:
            temp_page = await self._context.new_page()
            await temp_page.goto(
                "https://myaccount.google.com",
                wait_until="domcontentloaded",
                timeout=15_000,
            )
        except Exception:
            pass  # timeout no es crítico aquí

        current_url = temp_page.url if temp_page else ""
        self._log(f"   myaccount → {current_url[:120]}")

        if "accounts.google.com" in current_url:
            self._auth_verified = False
            if temp_page:
                await temp_page.close()
            raise RuntimeError(
                "✗ La sesión de Google no está autenticada.\n"
                "   Playwright fue redirigido a accounts.google.com.\n\n"
                "   Solución:\n"
                "   1. Ejecuta con headless=False\n"
                "   2. Inicia sesión manualmente en Google\n"
                "   3. Cierra la app normalmente (el perfil guarda la sesión)\n"
                "   4. Vuelve a ejecutar — la sesión se reutilizará.\n\n"
                f"   URL: {current_url}"
            )

        if temp_page:
            await temp_page.close()
        self._auth_verified = True
        self._log("✓ Sesión de Google autenticada.")

    # ── Espera del grid ───────────────────────────────────────────────────

    async def _wait_for_grid(self) -> bool:
        """
        Espera a que el grid de Google Sheets esté renderizado mediante sondeo.

        Google Sheets nunca llega a "networkidle" (WebSockets abiertos),
        por lo que usamos domcontentloaded + sondeo del DOM cada 500ms.

        Retorna True si se detectó el grid, False si se agotaron los reintentos.
        """
        # Delay inicial para que el canvas comience a renderizar
        await asyncio.sleep(0.001 * _RENDER_DELAY)

        # Sondeo progresivo del grid
        for attempt in range(1, _MAX_GRID_RETRIES + 1):
            found = await self.page.evaluate("""
                () => {
                    const selectors = [
                        '#waffle-grid-container', '#grid-container',
                        '[class*="waffle"]', '#colheaders', '#rowheaders',
                        '#formula-bar', '#t-formula-bar-input',
                    ];
                    const results = [];
                    for (const s of selectors) {
                        const el = document.querySelector(s);
                        if (el) results.push(s);
                    }
                    return results.length > 0 ? results.join(', ') : null;
                }
            """)
            if found:
                self._log(
                    f"· Grid detectado en intento {attempt}/{_MAX_GRID_RETRIES}: {found}"
                )
                return True

            if attempt % 5 == 0:
                self._log(f"· Esperando grid... intento {attempt}/{_MAX_GRID_RETRIES}")

            await asyncio.sleep(0.001 * _RETRY_INTERVAL)

        # Fallback final con wait_for_selector
        for selector in _GRID_SELECTORS:
            try:
                await self.page.wait_for_selector(selector, timeout=3_000)
                self._log(f"· Grid detectado vía wait_for_selector: {selector}")
                return True
            except Exception:
                continue

        self._log("✗ Grid no detectado tras agotar todos los intentos.")
        return False

    # ── Localización de celda ─────────────────────────────────────────────

    async def _locate_cell(self, cell_ref: str) -> dict[str, int] | None:
        """
        Localiza el rect exacto de la celda activa en Google Sheets (modo canvas).

        Google Sheets dibuja 4 divs .active-cell-border para los bordes de la
        celda seleccionada (top, bottom, left, right), cada uno de 2px de grosor.
        Reconstruimos el rect completo haciendo la unión de sus bounding boxes:

          top:    { x:221, y:327, w:456, h:2 }
          bottom: { x:221, y:419, w:456, h:2 }
          right:  { x:675, y:327, w:2,   h:94 }
          left:   { x:221, y:327, w:2,   h:94 }
          → rect: { x:221, y:327, w:456, h:94 }

        También intentamos el .selection-border-cover como fuente secundaria
        (cuando hay, tiene x/y/w correctos pero h puede ser solo 5px).
        """
        return await self.page.evaluate(
            """
            (cellRef) => {
                // ── Estrategia 1: reconstruir rect desde los 4 bordes active-cell-border ──
                // Google Sheets dibuja exactamente 4 divs de 2px para los lados de la celda.
                // La unión de sus bounding boxes = el rect completo de la celda.
                const activeBorders = document.querySelectorAll('.active-cell-border');
                if (activeBorders.length >= 2) {
                    let minX = Infinity, minY = Infinity;
                    let maxX = -Infinity, maxY = -Infinity;
                    let found = 0;
                    for (const el of activeBorders) {
                        const r = el.getBoundingClientRect();
                        // Ignorar bordes con area cero (ocultos/reutilizados)
                        if (r.width < 1 || r.height < 1) continue;
                        // Solo bordes dentro del viewport (descartar los que están en x>2000)
                        if (r.x > window.innerWidth * 2 || r.y > window.innerHeight * 2) continue;
                        minX = Math.min(minX, r.x);
                        minY = Math.min(minY, r.y);
                        maxX = Math.max(maxX, r.x + r.width);
                        maxY = Math.max(maxY, r.y + r.height);
                        found++;
                    }
                    if (found >= 2 && maxX > minX && maxY > minY) {
                        return {
                            x:      Math.round(minX),
                            y:      Math.round(minY),
                            width:  Math.round(maxX - minX),
                            height: Math.round(maxY - minY),
                            source: 'active-cell-border-union',
                        };
                    }
                }

                // ── Estrategia 2: selection-border-cover con dimensiones válidas ──
                // Cuando existe, tiene x/y/w correctos. El h puede ser pequeño (5px)
                // pero si es > 10 es confiable.
                for (const el of document.querySelectorAll('.selection-border-cover')) {
                    const r = el.getBoundingClientRect();
                    if (r.width > 20 && r.height > 10) {
                        return {
                            x:      Math.round(r.x),
                            y:      Math.round(r.y),
                            width:  Math.round(r.width),
                            height: Math.round(r.height),
                            source: 'selection-border-cover',
                        };
                    }
                }

                // ── Estrategia 3: canvas + offsets de headers (estimación) ────────
                const canvas      = document.querySelector('canvas');
                const colHeaderEl = document.querySelector('[class*="column-header"]');
                const rowHeaderEl = document.querySelector('[class*="row-header"]');
                if (!canvas) return null;

                const cr         = canvas.getBoundingClientRect();
                const colHeaderH = colHeaderEl ? colHeaderEl.getBoundingClientRect().height : 24;
                const rowHeaderW = rowHeaderEl ? rowHeaderEl.getBoundingClientRect().width  : 46;

                const match = cellRef.match(/^([A-Z]+)(\\d+)$/i);
                if (!match) return null;
                const colLetters = match[1].toUpperCase();
                const rowNum     = parseInt(match[2]);
                let colIdx = 0;
                for (let i = 0; i < colLetters.length; i++) {
                    colIdx = colIdx * 26 + (colLetters.charCodeAt(i) - 64);
                }
                colIdx -= 1;
                const rowIdx = rowNum - 1;

                return {
                    x:      Math.round(cr.x + rowHeaderW + colIdx * 100),
                    y:      Math.round(cr.y + colHeaderH + rowIdx * 21),
                    width:  100,
                    height: 21,
                    source: 'canvas-estimate',
                };
            }
            """,
            cell_ref,
        )

    # ── Validación y refinamiento del rect de celda ───────────────────────

    _CELL_PADDING = 0  # sin padding extra — el rect ya incluye los bordes de 2px
    _CELL_MAX_DIM = 800

    async def _validate_and_refine_rect(
        self,
        cell_ref: str,
        rect: dict[str, int],
        output_path: str,
        expected_value: str | None = None,
    ) -> dict[str, int]:
        """
        Valida el rect devuelto por _locate_cell y lo prepara como clip de screenshot.

        Con la estrategia 'active-cell-border-union', _locate_cell ya devuelve el
        rect exacto de la celda (unión de los 4 bordes de 2px). Este método:
          1. Valida dimensiones mínimas.
          2. Para 'active-cell-border-union': descuenta 2px del borde para obtener
             el interior limpio de la celda, o los mantiene para ver el borde completo.
          3. Si el rect es dudoso, reintenta los overlays.
          4. Genera debug highlight.
          5. Retorna el clip final.
        """
        ts = datetime.now().strftime("%H%M%S")
        source = rect.get("source", "unknown")
        w = rect.get("width", 0)
        h = rect.get("height", 0)

        self._log(
            f"· Celda {cell_ref} [{source}]: "
            f"({rect.get('x')},{rect.get('y')} {w}x{h}px)"
        )

        # ── Validar dimensiones ───────────────────────────────────────
        if w < 10 or h < 10:
            self._log(
                f"    ⚠ Rect demasiado pequeño ({w}x{h}). Reintentando overlays..."
            )
            retry = await self.page.evaluate("""
                () => {
                    // Reintentar unión de active-cell-border
                    const borders = document.querySelectorAll('.active-cell-border');
                    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity, n = 0;
                    for (const el of borders) {
                        const r = el.getBoundingClientRect();
                        if (r.width < 1 || r.height < 1) continue;
                        if (r.x > window.innerWidth * 2 || r.y > window.innerHeight * 2) continue;
                        minX = Math.min(minX, r.x);   minY = Math.min(minY, r.y);
                        maxX = Math.max(maxX, r.x + r.width); maxY = Math.max(maxY, r.y + r.height);
                        n++;
                    }
                    if (n >= 2 && maxX > minX && maxY > minY) {
                        return { x: Math.round(minX), y: Math.round(minY),
                                 width: Math.round(maxX-minX), height: Math.round(maxY-minY),
                                 source: 'retry-active-cell-border' };
                    }
                    return null;
                }
                """)
            if retry and retry.get("width", 0) >= 10 and retry.get("height", 0) >= 10:
                rect = retry
                source = rect["source"]
                w = rect["width"]
                h = rect["height"]
                self._log(f"    ✓ Reintento exitoso: {w}x{h}px")
            else:
                self._log(f"    ✗ Reintento falló. Usando rect original.")

        if w > self._CELL_MAX_DIM or h > self._CELL_MAX_DIM:
            self._log(f"    ⚠ Dimensiones excesivas ({w}x{h}). Recortando.")
            w = min(w, self._CELL_MAX_DIM)
            h = min(h, self._CELL_MAX_DIM)

        # ── Debug highlight ───────────────────────────────────────────
        debug_path = str(self._debug_dir / f"highlight_{cell_ref}_{ts}.png")
        try:
            await self.page.screenshot(path=debug_path, full_page=False)
            from PIL import Image, ImageDraw

            img = Image.open(debug_path)
            draw = ImageDraw.Draw(img)
            ex, ey = rect.get("x", 0), rect.get("y", 0)
            for offset in range(3):
                draw.rectangle(
                    [ex - offset, ey - offset, ex + w + offset, ey + h + offset],
                    outline="red",
                )
            img.save(debug_path)
            self._log(f"· Debug highlight: {debug_path}")
        except Exception as e:
            logger.warning("No se pudo generar highlight: %s", e)

        # ── Clip final ────────────────────────────────────────────────
        # Los bordes active-cell-border tienen 2px de grosor y ya están incluidos
        # en el rect de la unión. Los conservamos para que la captura muestre el
        # borde completo de la celda (como se ve en pantalla).
        clip = {
            "x": max(0, rect.get("x", 0)),
            "y": max(0, rect.get("y", 0)),
            "width": max(1, w),
            "height": max(1, h),
        }
        self._log(
            f"    ✓ Clip final: ({clip['x']},{clip['y']} {clip['width']}x{clip['height']})"
        )
        return clip

    # ── Depuración ─────────────────────────────────────────────────────────

    async def _dump_debug_info(self, reason: str, cell_ref: str) -> None:
        """Genera screenshot de depuración y registra contexto de la página."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = f"{reason}_{cell_ref}_{timestamp}"

        # Screenshot completo de la página
        try:
            ss_path = str(self._debug_dir / f"{prefix}_full.png")
            await self.page.screenshot(path=ss_path, full_page=False)
            self._log(f"· Debug screenshot: {ss_path}")
        except Exception as e:
            logger.warning("No se pudo generar screenshot de depuración: %s", e)

        # Contexto de la página
        try:
            title = await self.page.title()
            url = self.page.url
            self._log(f"· Debug — title: '{title[:100]}'")
            self._log(f"· Debug — url: {url[:200]}")

            # Extraer HTML relevante (contenedor del grid si existe)
            html_sample = await self.page.evaluate("""
                () => {
                    const grid = document.querySelector('#waffle-grid-container, #grid-container, [class*=\"waffle\"]');
                    if (grid) return grid.outerHTML.substring(0, 500);
                    return document.body ? document.body.innerHTML.substring(0, 500) : '(no body)';
                }
            """)
            logger.debug("Debug HTML sample: %s", html_sample)
        except Exception as e:
            logger.warning("No se pudo extraer contexto de depuración: %s", e)

    # ── Utilidades ────────────────────────────────────────────────────────

    @staticmethod
    def _extract_spreadsheet_id(url_or_id: str) -> str:
        """Extrae el spreadsheet ID de una URL o retorna el valor tal cual si ya es un ID."""
        import re

        match = re.search(r"/d/([a-zA-Z0-9_-]+)", url_or_id)
        if match:
            return match.group(1)
        return url_or_id

    # ── Wrappers síncronos ─────────────────────────────────────────────

    def capture_cells_sync(
        self,
        sheet_url: str,
        cell_refs: list[str],
        output_dir: str | None = None,
        sheet_gid: str | int = "0",
        expected_values: dict[str, str | None] | None = None,
    ) -> dict[str, str]:
        """
        Versión síncrona de capture_cells (para usar desde threads/tkinter).

        Abre el navegador, captura todas las celdas, y cierra el navegador
        en una sola llamada bloqueante. Ideal para entornos sin asyncio.
        """
        return asyncio.run(
            self._capture_cells_managed(
                sheet_url=sheet_url,
                cell_refs=cell_refs,
                output_dir=output_dir,
                sheet_gid=sheet_gid,
                expected_values=expected_values,
            )
        )

    async def _capture_cells_managed(
        self,
        sheet_url: str,
        cell_refs: list[str],
        output_dir: str | None = None,
        sheet_gid: str | int = "0",
        expected_values: dict[str, str | None] | None = None,
    ) -> dict[str, str]:
        """Start → capture → stop en un solo ciclo de vida."""
        await self.start()
        try:
            return await self.capture_cells(
                sheet_url=sheet_url,
                cell_refs=cell_refs,
                output_dir=output_dir,
                sheet_gid=sheet_gid,
                expected_values=expected_values,
            )
        finally:
            await self.stop()

    # ── Helpers públicos ──────────────────────────────────────────────────

    def clear_session(self) -> None:
        """
        Elimina el perfil persistente de Chrome.

        Borra cookies, localStorage y toda la sesión de Google.
        La próxima ejecución requerirá autenticación manual.
        """
        import shutil

        if self._profile_dir.exists():
            shutil.rmtree(str(self._profile_dir))
            self._log(f"→ Perfil eliminado: {self._profile_dir}")
        if self._session_path.exists():
            self._session_path.unlink()
            self._log("→ Sesión eliminada.")
