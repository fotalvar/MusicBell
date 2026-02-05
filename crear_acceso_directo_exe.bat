@echo off
REM Script para crear acceso directo de MusicBell en el escritorio
REM Con icono personalizado

echo.
echo ================================================
echo Creador de Acceso Directo - MusicBell
echo ================================================
echo.

REM Cambiar a la carpeta del script
cd /d "%~dp0"

REM Crear archivo VBS para crear el acceso directo
(
echo Set objShell = CreateObject("WScript.Shell"^)
echo strDesktop = objShell.SpecialFolders("Desktop"^)
echo strPath = WScript.Arguments(0^)
echo strWorkingDir = WScript.Arguments(1^)
echo.
echo Set objLink = objShell.CreateShortCut(strDesktop ^& "\MusicBell.lnk"^)
echo objLink.TargetPath = strPath
echo objLink.WorkingDirectory = strWorkingDir
echo objLink.IconLocation = strWorkingDir ^& "\icon.ico"
echo objLink.Description = "Sistema de Música Escolar - MusicBell"
echo objLink.Save
echo.
echo WScript.Echo "✓ Acceso directo creado en el escritorio"
) > crear_acceso.vbs

REM Ejecutar el script VBS
cscript crear_acceso.vbs "%~dp0dist\MusicBell.exe" "%~dp0"

REM Limpiar
del crear_acceso.vbs

echo.
echo ✓ Acceso directo creado en tu escritorio
echo.
pause
