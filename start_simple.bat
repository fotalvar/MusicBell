@echo off
REM Script simple de prueba para MusicBell
cd /d "%~dp0"

echo Activando entorno virtual...
cd backend
call venv\Scripts\activate.bat

echo.
echo Verificando que app.py es válido...
python -m py_compile app.py
if errorlevel 1 (
    echo ❌ Error en app.py
    pause
    exit /b 1
)
echo ✓ app.py es válido

echo.
echo Verificando que music_player.py es válido...
python -m py_compile music_player.py
if errorlevel 1 (
    echo ❌ Error en music_player.py
    pause
    exit /b 1
)
echo ✓ music_player.py es válido

echo.
echo Intentando importar módulos...
python -c "from flask import Flask; from flask_cors import CORS; from pathlib import Path; print('✓ Importaciones base OK')"
if errorlevel 1 (
    echo ❌ Error en importaciones
    pause
    exit /b 1
)

echo.
echo Iniciando MusicBell...
echo Acceso en: http://localhost:5000
echo.

python app.py
pause
