#!/usr/bin/env python3
"""
Wrapper para ejecutar MusicBell desde un EXE
Este archivo será compilado con PyInstaller para crear MusicBell.exe
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Obtener la carpeta del script
    if getattr(sys, 'frozen', False):
        # Si está empaquetado con PyInstaller
        script_dir = Path(sys.executable).parent
    else:
        # Si se ejecuta directamente
        script_dir = Path(__file__).parent
    
    # Cambiar a la carpeta del proyecto
    project_dir = script_dir.parent if script_dir.name == 'backend' else script_dir
    os.chdir(project_dir)
    
    # Ejecutar app.py
    backend_dir = project_dir / 'backend'
    app_file = backend_dir / 'app.py'
    
    if not app_file.exists():
        print(f"❌ Error: No se encontró {app_file}")
        input("Presiona Enter para salir...")
        return 1
    
    # Cambiar a la carpeta backend y ejecutar
    os.chdir(backend_dir)
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n✓ MusicBell detenido")
        return 0
    except Exception as e:
        print(f"❌ Error ejecutando MusicBell: {e}")
        input("Presiona Enter para salir...")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
