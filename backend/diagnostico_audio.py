#!/usr/bin/env python3
"""
Script de diagnóstico para MusicBell - Audio en Windows
Ayuda a identificar por qué no suena la música
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("🔧 DIAGNÓSTICO DE REPRODUCCIÓN DE AUDIO - MusicBell")
print("=" * 60)

# 1. Verificar Python
print("\n1️⃣  PYTHON")
print(f"   Versión: {sys.version}")
print(f"   Ejecutable: {sys.executable}")

# 2. Verificar playsound
print("\n2️⃣  PLAYSOUND")
try:
    import playsound
    print(f"   ✅ Instalado: {playsound.__file__}")
except ImportError as e:
    print(f"   ❌ NO INSTALADO: {e}")
    print("   Instala con: python -m pip install playsound==1.2.2")
    sys.exit(1)

# 3. Verificar carpeta de canciones
print("\n3️⃣  CARPETA DE CANCIONES")
project_root = Path(__file__).parent.parent
songs_dir = project_root / 'canciones'
print(f"   Ruta: {songs_dir}")

if songs_dir.exists():
    print(f"   ✅ Carpeta existe")
    mp3_files = list(songs_dir.glob('*.mp3'))
    if mp3_files:
        print(f"   ✅ {len(mp3_files)} archivo(s) MP3 encontrado(s):")
        for f in mp3_files:
            size_kb = f.stat().st_size / 1024
            print(f"      - {f.name} ({size_kb:.1f} KB)")
    else:
        print(f"   ⚠️  No hay archivos MP3 en {songs_dir}")
else:
    print(f"   ❌ Carpeta NO EXISTE: {songs_dir}")
    sys.exit(1)

# 4. Verificar si el primer MP3 es válido
print("\n4️⃣  VALIDACIÓN DE ARCHIVO MP3")
mp3_files = list(songs_dir.glob('*.mp3'))
if mp3_files:
    test_file = mp3_files[0]
    print(f"   Probando: {test_file.name}")
    
    if os.path.exists(test_file):
        print(f"   ✅ Archivo existe")
        size = os.path.getsize(test_file)
        print(f"   ✅ Tamaño: {size} bytes")
        
        # Verificar que no está vacío
        if size > 10000:  # Al menos 10KB
            print(f"   ✅ Archivo parece válido (>10KB)")
        else:
            print(f"   ⚠️  Archivo muy pequeño, podría estar corrupto")
    else:
        print(f"   ❌ Archivo no encontrado")
else:
    print(f"   ❌ No hay archivos MP3 para probar")

# 5. Probar reproducción manual
print("\n5️⃣  PRUEBA DE REPRODUCCIÓN")
if mp3_files:
    test_file = str(mp3_files[0].absolute())
    print(f"   Intentando reproducir: {test_file}")
    
    try:
        print("   ⏳ Reproduciendo... (espera 2-3 segundos)")
        from playsound import playsound
        playsound(test_file)
        print("   ✅ ¡REPRODUCCIÓN EXITOSA! El audio funcionó.")
    except Exception as e:
        print(f"   ❌ ERROR EN REPRODUCCIÓN: {e}")
        print(f"      Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()

# 6. Verificar volumen del sistema
print("\n6️⃣  VOLUMEN DEL SISTEMA")
print("   ⚠️  Verifica manualmente:")
print("      - Volumen de Windows no está en 0")
print("      - Los altavoces están conectados")
print("      - Prueba sonido del sistema (Settings > Sound)")

# 7. Información de logs
print("\n7️⃣  LOGS")
logs_file = project_root / 'logs' / 'musicbell.log'
if logs_file.exists():
    print(f"   ✅ Archivo de log existe: {logs_file}")
    print("   Últimas líneas:")
    with open(logs_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[-10:]:
            print(f"      {line.rstrip()}")
else:
    print(f"   ℹ️  Aún no hay logs (la app no ha corrido)")

print("\n" + "=" * 60)
print("✅ DIAGNÓSTICO COMPLETADO")
print("=" * 60)
print("\n💡 Si el paso 5 funcionó, el problema está en la API/Frontend")
print("   Si el paso 5 falló, el problema está en playsound o el archivo")
