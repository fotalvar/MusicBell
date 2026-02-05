@echo off
REM Script para generar MusicBell.exe con PyInstaller
REM Este script crea un archivo EXE ejecutable con icono

echo.
echo ================================================
echo Generador de EXE para MusicBell
echo ================================================
echo.

REM Cambiar a la carpeta del script
cd /d "%~dp0"

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado
    pause
    exit /b 1
)

echo ✓ Python encontrado
echo.

REM Verificar/crear venv
if not exist "backend\venv" (
    echo Creando entorno virtual...
    cd backend
    python -m venv venv
    cd ..
)

REM Activar venv
echo Activando entorno virtual...
cd backend
call venv\Scripts\activate.bat
cd ..

REM Instalar PyInstaller si no está
echo Verificando PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Error instalando PyInstaller
        pause
        exit /b 1
    )
)
echo ✓ PyInstaller OK
echo.

REM Verificar icono
if not exist "icon.ico" (
    echo ⚠️  No se encontró icon.ico, generando...
    python crear_icono.py
    if errorlevel 1 (
        echo ⚠️  Error generando icono, continuando sin icono...
    )
)

REM Mostrar información
echo.
echo ================================================
echo Generando MusicBell.exe...
echo ================================================
echo.

REM Generar EXE
pyinstaller --onefile ^
    --windowed ^
    --name "MusicBell" ^
    --icon "icon.ico" ^
    --add-data "frontend;frontend" ^
    --add-data "canciones;canciones" ^
    --add-data "config;config" ^
    --add-data "logs;logs" ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
    --hidden-import=pygame ^
    --hidden-import=mutagen ^
    --distpath "dist" ^
    musicbell_launcher.py

if errorlevel 1 (
    echo ❌ Error generando EXE
    pause
    exit /b 1
)

echo.
echo ================================================
echo ✓ EXE generado exitosamente
echo ================================================
echo.
echo Ubicación: %cd%\dist\MusicBell.exe
echo.
echo Próximos pasos:
echo 1. Abre la carpeta "dist"
echo 2. Haz clic derecho en "MusicBell.exe"
echo 3. Selecciona "Enviar a" > "Escritorio (crear acceso directo)"
echo 4. Ya puedes ejecutar desde el escritorio
echo.

pause
