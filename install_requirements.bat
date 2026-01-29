@echo off
REM ============================================================
REM Script de Instalación de Requisitos para MusicBell (Windows)
REM ============================================================

echo.
echo ========================================
echo   MusicBell - Instalador de Requisitos
echo ========================================
echo.

REM Verificar si Python está instalado
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    echo.
    echo Por favor, instala Python desde: https://www.python.org/
    echo Asegúrate de marcar "Add Python to PATH" durante la instalación
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ %PYTHON_VERSION% detectado

REM Verificar si pip está disponible
echo.
echo [2/4] Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no está disponible
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('pip --version') do set PIP_VERSION=%%i
echo ✓ %PIP_VERSION% detectado

REM Instalar dependencias
echo.
echo [3/4] Instalando dependencias Python...
echo.
pip install -r backend\requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo.
echo ✓ Dependencias instaladas correctamente

REM Crear carpeta de canciones
echo.
echo [4/4] Creando estructura de carpetas...
if not exist "canciones" (
    mkdir canciones
    echo ✓ Carpeta 'canciones' creada
) else (
    echo ✓ Carpeta 'canciones' ya existe
)

REM Verificar que todo está instalado
echo.
echo ========================================
echo   VERIFICACIÓN FINAL
echo ========================================
echo.

python -c "import flask, flask_cors, dotenv, mutagen; print('✓ Todas las dependencias están instaladas correctamente')" 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Hay problemas con las dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ INSTALACIÓN COMPLETADA
echo ========================================
echo.
echo Próximo paso: Ejecutar la aplicación
echo.
echo Opción 1: Ejecutar start_windows.bat
echo Opción 2: Abrir PowerShell/CMD y ejecutar:
echo   python backend\app.py
echo.
echo Luego abre tu navegador en:
echo   http://localhost:5000
echo.
pause
