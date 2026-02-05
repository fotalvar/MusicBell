@echo off
REM Script de inicio para MusicBell en Windows
setlocal enabledelayedexpansion

cls
echo.
echo ================================================
echo Iniciando MusicBell - Sistema de Música Escolar
echo ================================================
echo.

REM Cambiar a la carpeta del script
cd /d "%~dp0"

if not exist "backend" (
    echo ❌ ERROR: Carpeta 'backend' no encontrada
    echo Verifica que start_windows.bat está en la carpeta correcta
    pause
    exit /b 1
)

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo.
    echo Soluciones:
    echo 1. Descárgalo desde: https://www.python.org/downloads/
    echo 2. Durante la instalación, marca "Add Python to PATH"
    echo 3. Reinicia tu ordenador después de instalar Python
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ %PYTHON_VERSION% encontrado
echo.

REM Crear entorno virtual si no existe
if not exist "backend\venv" (
    echo Creando entorno virtual...
    cd backend
    python -m venv venv
    cd ..
    if not exist "backend\venv" (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
    echo ✓ Entorno virtual creado
)

REM Activar entorno virtual
echo Activando entorno virtual...
cd backend
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error activando entorno virtual
    pause
    exit /b 1
)
echo ✓ Entorno virtual activado
cd ..
echo.

REM Instalar dependencias
echo Verificando dependencias...
python -m pip install -r backend/requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Error instalando dependencias, intentando de nuevo...
    python -m pip install --upgrade pip
    python -m pip install -r backend/requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
)
echo ✓ Dependencias OK
echo.

REM Liberar puerto 5000 (opcional, si algo ya está usando puerto)
echo Verificando puerto 5000...
netstat -ano 2>nul | findstr :5000 >nul
if not errorlevel 1 (
    echo ⚠️  Puerto 5000 en uso, intentando liberar...
    for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr :5000') do (
        taskkill /PID %%a /F >nul 2>&1
    )
)
echo ✓ Puerto 5000 disponible
echo.

REM Mostrar información
echo ================================================
echo 📂 Carpeta de trabajo: %cd%
echo 🎵 Carpeta de canciones: %cd%\canciones
echo 📝 Logs: %cd%\logs
echo ================================================
echo.
echo 🚀 Iniciando servidor MusicBell...
echo 📡 Acceso local: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Iniciar la aplicación
cd backend
python app.py

if errorlevel 1 (
    echo.
    echo ❌ ERROR al iniciar MusicBell
    echo Revisa si hay errores arriba ↑
    echo.
)

pause
