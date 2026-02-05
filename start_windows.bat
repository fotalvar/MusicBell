@echo off
cd /d "%~dp0"

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python no encontrado
    pause
    exit /b 1
)

REM Crear venv solo si no existe
if not exist backend\venv (
    echo Creando entorno virtual...
    python -m venv backend\venv
    if errorlevel 1 (
        echo ❌ Error creando venv
        pause
        exit /b 1
    )
    echo ✓ Entorno virtual creado
)

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

REM Instalar dependencias (solo si no están ya)
echo Verificando dependencias...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    cd ..
    pause
    exit /b 1
)
echo ✓ Dependencias OK

REM Iniciar app
echo.
echo ✓ Iniciando MusicBell...
echo Acceso en: http://localhost:5000
echo.
python app.py

cd ..
pause
