def subir(
    sitio,
    ruta_imagen,
    headless,
    log,
    credenciales_sesion=None,
    usar_chrome_existente=False,
):
    """
    Sube `ruta_imagen` al `sitio`.

    Flujo para sitios con login:
      A) usar_chrome_existente=True
         → Se conecta al Chrome del usuario (puerto 9222).
         → Verifica si ya hay sesión activa navegando a url_upload.
         → Si hay sesión  → sube directamente.
         → Si no la hay  → avisa al usuario para que inicie sesión manualmente
                           (no intenta login automático para no interferir con su sesión).
      B) usar_chrome_existente=False
         → Abre Chrome nuevo.
         → Intenta restaurar sesión con cookies.
         → Si las cookies son válidas → sube.
         → Si no                      → hace login automático, guarda cookies y sube.
    """
    driver = crear_driver(headless, usar_chrome_existente)
    wait = WebDriverWait(driver, 15)
    # sesion_activa = True  # asume sesión activa, se validará más adelante
    nombre = sitio.get("nombre", "sitio")

    try:
        if sitio["necesita_login"]:
            # url_base = sitio["url_login"]
            # sesion_activa = False

            if usar_chrome_existente:
                # ── Reutilizar la pestaña activa en lugar de abrir una nueva ──
                # pestaña_original = driver.current_window_handle
                # driver.switch_to.window(pestaña_original)
                # Verificar si ya hay sesión activa en el Chrome abierto
                log(
                    f"  → Verificando sesión activa en Chrome abierto para {sitio['nombre']}..."
                )
                driver.get(sitio["url_upload"])
                time.sleep(
                    1.5
                )  # pequeña pausa para que cargue y redirija si no hay sesión

                if "login" not in driver.current_url.lower():
                    log(f"  ✓ Sesión activa detectada en Chrome: {sitio['nombre']}")
                    sesion_activa = True
                else:
                    log(
                        f"  ✗ Chrome abierto pero sin sesión activa en {sitio['nombre']}"
                    )
                    log(
                        f"  → Inicia sesión manualmente en el navegador y vuelve a intentar"
                    )
                    return  # no intenta login automático
            else:
                # 1. Intentar cargar cookies para restaurar sesión
                cargar_cookies(driver, sitio, url_base)
                # Navegar a pagina protegida para verificar si la sesión es válida
                driver.get(sitio["url_upload"])
                time.sleep(1)  # pequeña pausa para que cargue
                if "login" not in driver.current_url:
                    log(f"  ✓ Sesión restaurada con cookies para {nombre}")
                    sesion_activa = True
                else:
                    log(f"  ✗ Cookies expiradas, haciendo login...")

        if not sesion_activa:
            if credenciales_sesion and nombre in credenciales_sesion:
                usuario = credenciales_sesion[nombre]["usuario"]
                clave = credenciales_sesion[nombre]["clave"]

            # ── LOGIN ─────────────────────────────
            else:
                usuario, clave = cargar_credenciales(sitio["nombre"])

            if not usuario or not clave:
                log(f"  ✗ No hay credenciales para {sitio['nombre']}")
                return

            driver.get(sitio["url_login"])
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, sitio["selector_user"])
                )
            )
            driver.find_element(By.CSS_SELECTOR, sitio["selector_user"]).send_keys(
                usuario
            )
            driver.find_element(By.CSS_SELECTOR, sitio["selector_pass"]).send_keys(
                clave
            )
            driver.find_element(By.CSS_SELECTOR, sitio["selector_btn_login"]).click()
            wait.until(EC.url_contains("secure"))

            guardar_cookies(driver, nombre)
            log(f"  ✓ Login exitoso, cookies guardadas: {nombre}")

        # ── SUBIDA ────────────────────────────
        driver.get(sitio["url_upload"])

        input_file = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, sitio["selector_input_file"]))
        )

        input_file.send_keys(os.path.abspath(ruta_imagen))

        driver.find_element(By.CSS_SELECTOR, sitio["selector_submit"]).click()

        # DEBUG (opcional)
        driver.save_screenshot("debug.png")

        resultado = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))
        ).text

        if "Uploaded" in resultado:
            log(f"  ✓ {sitio['nombre']}: subida exitosa")
        else:
            log(f"  ✗ {sitio['nombre']}: no se confirmó subida")

    except Exception as e:
        log(f"  ✗ Error en {sitio['nombre']}: {e}")

    finally:
        if usar_chrome_existente:
            pass  # no cerrar el Chrome que el usuario tiene abierto
        else:
            driver.quit()

    usuario, clave = cargar_credenciales(
        sitio["nombre"]
    )  # Esto hay que comentarlo despues
    print("DEBUG CREDENCIALES:", usuario, clave)  # Esto hay que comentarlo despues
