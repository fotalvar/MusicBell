@echo off
cd /d "%~dp0"

REM Crear venv
if not exist backend\venv (
    echo Creando entorno virtual...
    python -m venv backend\venv
    if errorlevel 1 (
        echo ❌ Error creando venv
        pause
        exit /b 1
    )
)

REM Activar y ejecutar
cd backend
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error activando venv
    pause
    exit /b 1
)

echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo Iniciando MusicBell...
python app.py
if errorlevel 1 (
    echo ❌ Error en app.py
    pause
    exit /b 1
)

pause
