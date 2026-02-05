@echo off
cd /d "%~dp0"

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python no encontrado
    pause
    exit /b 1
)

REM Limpiar venv antiguo si existe
if exist backend\venv (
    echo Limpiando entorno virtual antiguo...
    rmdir /s /q backend\venv >nul 2>&1
)

REM Crear venv nuevo
echo Creando entorno virtual...
python -m venv backend\venv
if errorlevel 1 (
    echo ❌ Error creando venv
    pause
    exit /b 1
)
echo ✓ Entorno virtual creado

REM Activar
echo Activando entorno virtual...
cd backend
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error activando venv
    cd ..
    pause
    exit /b 1
)
echo ✓ Activado

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    cd ..
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas

REM Iniciar app
echo.
echo ✓ Iniciando MusicBell...
echo Acceso en: http://localhost:5000
echo.
python app.py

cd ..
pause
