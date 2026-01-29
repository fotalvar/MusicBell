@echo off
REM ============================================================
REM Script de Inicio para MusicBell en Windows (Versión Simple)
REM ============================================================
REM Este script inicia la aplicación MusicBell.
REM Asegúrate de haber ejecutado install_requirements.bat primero
REM ============================================================

echo.
echo ========================================
echo   MusicBell - Iniciando Servidor
echo ========================================
echo.

REM Cambiar a la carpeta del script
cd /d "%~dp0"

REM Verificar si Python está instalado
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python no está instalado o no está en PATH
    echo.
    echo Solución:
    echo 1. Instala Python desde: https://www.python.org/
    echo 2. Asegúrate de marcar "Add Python to PATH"
    echo 3. Ejecuta este script de nuevo
    echo.
    echo Alternativamente, ejecuta install_requirements.bat
    echo.
    pause
    exit /b 1
)

REM Mostrar versión de Python
for /f "tokens=*" %%i in ('python --version') do echo ✓ %%i detectado

REM Verificar si las dependencias están instaladas
echo.
echo Verificando dependencias...
python -c "import flask, flask_cors, dotenv, mutagen" 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Las dependencias no están instaladas
    echo.
    echo Por favor ejecuta primero:
    echo   install_requirements.bat
    echo.
    pause
    exit /b 1
)
echo ✓ Todas las dependencias están disponibles

REM Mostrar información
echo.
echo Carpeta de trabajo: %cd%
echo Archivo de configuración: config\canciones.json
echo Carpeta de canciones: canciones\
echo Logs: logs\musicbell.log
echo.

REM Iniciar la aplicación
echo ========================================
echo   Iniciando servidor en http://localhost:5000
echo ========================================
echo.
echo Abre tu navegador y accede a:
echo   http://localhost:5000
echo.
echo Para detener: Presiona Ctrl+C
echo.

cd backend
python app.py

pause
