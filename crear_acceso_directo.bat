@echo off
REM ============================================================
REM Script para crear acceso directo a MusicBell en el Escritorio
REM Se ejecuta una sola vez después de la instalación
REM ============================================================

setlocal enabledelayedexpansion

REM Obtener rutas
set "SCRIPT_DIR=%~dp0"
set "DESKTOP_PATH=%USERPROFILE%\Desktop"
set "ICON_PATH=%SCRIPT_DIR%icon.ico"
set "SHORTCUT_PATH=%DESKTOP_PATH%\MusicBell.lnk"

REM Crear el acceso directo
echo Creando acceso directo en el Escritorio...

REM Usar PowerShell para crear el acceso directo con icono
powershell -NoProfile -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; " ^
    "$Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); " ^
    "$Shortcut.TargetPath = '%SCRIPT_DIR%start_windows.bat'; " ^
    "$Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; " ^
    "$Shortcut.IconLocation = '%ICON_PATH%'; " ^
    "$Shortcut.Description = 'MusicBell - Sistema de Música Escolar'; " ^
    "$Shortcut.Save()"

if errorlevel 1 (
    echo ERROR: No se pudo crear el acceso directo
    echo Intenta ejecutar este script como Administrador
    pause
    exit /b 1
) else (
    echo ✓ Acceso directo creado exitosamente en: %SHORTCUT_PATH%
)

endlocal
pause
