@echo off
setlocal enabledelayedexpansion

cls
echo.
echo ================================================
echo Iniciando MusicBell
echo ================================================
echo.

REM Cambiar a la carpeta del script
cd /d "%~dp0"

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en PATH
    echo.
    echo Soluciones:
    echo 1. Descárgalo desde https://www.python.org/downloads/
    echo 2. Marca "Add Python to PATH" durante la instalación
    echo 3. Reinicia tu ordenador
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo ✓ %%i encontrado
echo.

REM Crear venv si no existe
if not exist "backend\venv" (
    echo Creando entorno virtual...
    cd backend
    python -m venv venv
    if not exist "venv" (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
    cd ..
    echo ✓ Entorno virtual creado
    echo.
)

REM Activar venv e instalar dependencias
echo Verificando dependencias...
cd backend
call venv\Scripts\activate.bat >nul 2>&1
if errorlevel 1 (
    echo ❌ Error activando entorno virtual
    echo.
    echo Intenta eliminar la carpeta "backend\venv" y ejecuta de nuevo
    echo.
    pause
    exit /b 1
)

python -m pip install -q -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando dependencias (primera vez)...
    python -m pip install -r requirements.txt
)
echo ✓ Dependencias OK
echo.

REM Mostrar información
echo ================================================
echo 🎵 MusicBell - Sistema de Música Escolar
echo ================================================
echo.
echo 📡 URL: http://localhost:5000
echo 📂 Carpeta: %~dp0
echo.
echo Presiona Ctrl+C para detener
echo.

REM Iniciar app
python app.py

pause
