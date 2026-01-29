@echo off
REM Script de inicio para MusicBell en Windows

echo.
echo ================================================
echo Iniciando MusicBell - Sistema de Música Escolar
echo ================================================
echo.

REM Cambiar a la carpeta del script
cd /d "%~dp0"

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    echo Descárgalo desde: https://www.python.org/downloads/
    echo Recuerda marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

echo.
for /f "tokens=*" %%i in ('python --version') do echo ✓ %%i encontrado

REM Instalar dependencias si es necesario
if not exist "backend\venv" (
    echo.
    echo Creando entorno virtual...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
)

REM Activar entorno virtual
call backend\venv\Scripts\activate.bat

REM Mostrar información
echo.
echo Folder de trabajo: %cd%
echo Carpeta de canciones: %cd%\canciones
echo Logs: %cd%\logs
echo.
echo Iniciando servidor...
echo.

REM Iniciar la aplicación
cd backend
python app.py

pause
