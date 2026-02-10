@echo off
setlocal

:: --- CONFIGURATION ---
set "ROOT_DIR=%~dp0"
set "COMFY_DIR=%ROOT_DIR%ComfyUI_windows_portable"
set "PYTHON_EXE=%COMFY_DIR%\python_embeded\python.exe"
set "COMFY_MAIN=%COMFY_DIR%\ComfyUI\main.py"
set "GRADIO_APP=%ROOT_DIR%app.py"
set "GRADIO_URL=http://127.0.0.1:7860"

:: --- CHECK ---
if not exist "%PYTHON_EXE%" (
    echo [ERROR] No se encuentra la carpeta 'ComfyUI_windows_portable'.
    pause
    exit /b
)

:: --- LIBRARY INSTALL  ---
echo [INFO] Checking enviroment...
"%PYTHON_EXE%" -m pip install gradio requests websocket-client >nul 2>&1

:: --- STARTING COMFYUI ---
echo.
echo [SEGURIDAD] Starting ComfyUI in LOCALHOST mode .
echo.

:: --listen removed. --port 8188 safe.
start "ComfyUI Local" /min "%PYTHON_EXE%" "%COMFY_MAIN%" --port 8188

:: --- WAITING FOR ComfyUI ---
echo [INFO] Waiting ComfyUI to start (10 seg)...
timeout /t 10 /nobreak >nul

:: --- NAVIGATOR LAUNCH ---
:: waits 5 seg and open the link, 
:: while the script is running the explorer opens
echo [INFO] Preparando apertura segura del navegador...
start "" /b cmd /c "timeout /t 5 /nobreak >nul & start %GRADIO_URL%"

:: --- STARTING APP ---
echo.
echo [INFO] Starting Gradio app...
echo [INFO] If don't launches go to: %GRADIO_URL%
echo.

:: Force GRADIO_SERVER_NAME a 127.0.0.1 to be safe
set GRADIO_SERVER_NAME=127.0.0.1
"%PYTHON_EXE%" "%GRADIO_APP%"

pause