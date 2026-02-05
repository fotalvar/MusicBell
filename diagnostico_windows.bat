@echo off
REM Script de diagnóstico para MusicBell en Windows
setlocal enabledelayedexpansion

echo.
echo ================================================
echo Diagnóstico de MusicBell
echo ================================================
echo.

REM Cambiar a la carpeta del script
cd /d "%~dp0"

echo [1/5] Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python no encontrado
    pause
    exit /b 1
)
echo ✓ Python OK
echo.

echo [2/5] Verificando pip...
python -m pip --version
if errorlevel 1 (
    echo ❌ pip no encontrado
    pause
    exit /b 1
)
echo ✓ pip OK
echo.

echo [3/5] Creando/actualizando entorno virtual...
if not exist "backend\venv" (
    echo Creando venv...
    cd backend
    python -m venv venv
    cd ..
)
echo ✓ venv existe
echo.

echo [4/5] Instalando/actualizando dependencias...
cd backend
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    echo Revisa requirements.txt
    pause
    exit /b 1
)
echo ✓ Dependencias OK
echo.

echo [5/5] Probando importaciones...
python -c "import flask; print('✓ Flask OK')"
if errorlevel 1 (
    echo ❌ Error con Flask
    pause
    exit /b 1
)

python -c "import pygame; print('✓ pygame OK')"
if errorlevel 1 (
    echo ⚠️  pygame no disponible (se necesita para Windows)
    echo Instalando pygame...
    pip install pygame
    if errorlevel 1 (
        echo ❌ Error instalando pygame
        pause
        exit /b 1
    )
)

echo.
echo ================================================
echo ✓ Todas las verificaciones pasaron
echo ================================================
echo.
echo Intentando iniciar la aplicación...
echo.

python app.py
if errorlevel 1 (
    echo.
    echo ❌ Error iniciando app.py
    echo.
    echo Intenta ejecutar esto en la consola para ver el error:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   python app.py
    echo.
)

pause
