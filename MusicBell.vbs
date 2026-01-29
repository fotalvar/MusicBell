REM Script VBS para lanzar MusicBell con interfaz mejorada
REM Ejecuta start_windows.bat sin mostrar ventana de comandos

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

REM Obtener la ruta del script
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

REM Ejecutar start_windows.bat
objShell.Run """" & strPath & "\start_windows.bat""", 0, False
