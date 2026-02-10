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

:: --- FORZAR MODO CPU (Configuración Clave) ---
:: Esto oculta la tarjeta gráfica a Python para evitar conflictos
set CUDA_VISIBLE_DEVICES=-1

:: --- INSTALACIÓN DE LIBRERÍAS (SOLO SI FALTAN) ---
echo [INFO] Verificando entorno...
"%PYTHON_EXE%" -m pip install gradio requests websocket-client >nul 2>&1

:: --- INICIAR COMFYUI (MODO CPU + PRIVADO) ---
echo.
echo [MODO CPU] Iniciando ComfyUI usando solo el Procesador.
echo [AVISO] La generacion de imagenes sera mas lenta que con GPU.
echo.

:: Agregamos el argumento "--cpu" aqui
start "ComfyUI CPU" /min "%PYTHON_EXE%" "%COMFY_MAIN%" --cpu --port 8188

:: --- ESPERA DE CARGA ---
echo [INFO] Esperando a que ComfyUI arranque (12 seg)...
timeout /t 12 /nobreak >nul

:: --- LANZADOR AUTOMÁTICO DEL NAVEGADOR ---
echo [INFO] Preparando apertura segura del navegador...
start "" /b cmd /c "timeout /t 5 /nobreak >nul & start %GRADIO_URL%"

:: --- INICIAR TU APP ---
echo.
echo [INFO] Iniciando interfaz Gradio...
echo [INFO] Ve a: %GRADIO_URL%
echo.

:: Seguridad localhost
set GRADIO_SERVER_NAME=127.0.0.1
"%PYTHON_EXE%" "%GRADIO_APP%"

pause