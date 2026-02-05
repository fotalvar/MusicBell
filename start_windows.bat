@echo off
cd /d "%~dp0"

REM Crear venv
if not exist backend\venv (
    echo Creando entorno virtual...
    python -m venv backend\venv
)

REM Activar y ejecutar
cd backend
call venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
