@echo off
REM Script de inicio para MusicBell en Windows
REM Usar setlocal para mejor manejo de errores
setlocal enabledelayedexpansion

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
    echo.
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

echo.
for /f "tokens=*" %%i in ('python --version') do echo ✓ %%i encontrado

REM Liberar puerto 5000
echo.
echo 🔍 Verificando puerto 5000...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr :5000') do (
    echo ⚠️  Encontrado proceso %%a usando puerto 5000, terminando...
    taskkill /PID %%a /F >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✓ Proceso terminado
    )
)
echo ✓ Puerto 5000 liberado
echo.

REM Crear entorno virtual si no existe
if not exist "backend\venv" (
    echo.
    echo Creando entorno virtual...
    cd backend
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
    echo ✓ Entorno virtual creado
    echo.
    
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ❌ Error activando entorno virtual
        pause
        exit /b 1
    )
    
    echo Instalando dependencias (esto puede tomar un minuto)...
    pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        echo Verifica el archivo requirements.txt
        pause
        exit /b 1
    )
    echo ✓ Dependencias instaladas
    cd ..
    echo.
) else (
    echo Entorno virtual encontrado
    cd backend
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ❌ Error activando entorno virtual
        pause
        exit /b 1
    )
    cd ..
)

REM Mostrar información
echo.
echo ================================================
echo 📂 Carpeta de trabajo: %cd%
echo 🎵 Carpeta de canciones: %cd%\canciones
echo 📝 Logs: %cd%\logs
echo ================================================
echo.
echo Iniciando servidor MusicBell...
echo Presiona Ctrl+C para detener el servidor
echo.

REM Iniciar la aplicación
cd backend
python app.py

if errorlevel 1 (
    echo.
    echo ❌ ERROR al iniciar MusicBell
    echo.
    echo Por favor, verifica:
    echo - Que Python está instalado correctamente
    echo - Que las dependencias están instaladas (requirements.txt)
    echo - Que no hay otro proceso usando el puerto 5000
    echo.
)

pause
