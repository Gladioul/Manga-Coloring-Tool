@echo off
setlocal

:: --- CONFIGURACIÓN ---
set "ROOT_DIR=%~dp0"
set "COMFY_DIR=%ROOT_DIR%ComfyUI_windows_portable"
set "PYTHON_EXE=%COMFY_DIR%\python_embeded\python.exe"
set "COMFY_MAIN=%COMFY_DIR%\ComfyUI\main.py"
set "GRADIO_APP=%ROOT_DIR%app.py"
set "GRADIO_URL=http://127.0.0.1:7860"

:: --- VERIFICACIÓN DE SEGURIDAD ---
if not exist "%PYTHON_EXE%" (
    echo [ERROR] No se encuentra la carpeta 'ComfyUI_windows_portable'.
    pause
    exit /b
)

:: --- INSTALACIÓN DE LIBRERÍAS (SOLO SI FALTAN) ---
echo [INFO] Verificando entorno...
"%PYTHON_EXE%" -m pip install gradio requests websocket-client >nul 2>&1

:: --- INICIAR COMFYUI (MODO PRIVADO / OFFLINE) ---
echo.
echo [SEGURIDAD] Iniciando ComfyUI en modo LOCALHOST (Privado).
echo [INFO] Nadie en tu red Wifi podra acceder a esto.
echo.

:: --listen ELIMINADO para seguridad. --port 8188 asegurado.
start "ComfyUI Local" /min "%PYTHON_EXE%" "%COMFY_MAIN%" --port 8188

:: --- ESPERA DE CARGA DE COMFYUI ---
echo [INFO] Esperando a que ComfyUI arranque (10 seg)...
timeout /t 10 /nobreak >nul

:: --- LANZADOR AUTOMÁTICO DEL NAVEGADOR ---
:: Esto crea un mini proceso que espera 5 seg y abre el link, 
:: mientras el script principal continua cargando la app.
echo [INFO] Preparando apertura segura del navegador...
start "" /b cmd /c "timeout /t 5 /nobreak >nul & start %GRADIO_URL%"

:: --- INICIAR TU APP ---
echo.
echo [INFO] Iniciando aplicacion Gradio...
echo [INFO] Si no se abre, ve a: %GRADIO_URL%
echo.

:: Forzamos GRADIO_SERVER_NAME a 127.0.0.1 para máxima seguridad
set GRADIO_SERVER_NAME=127.0.0.1
"%PYTHON_EXE%" "%GRADIO_APP%"

pause