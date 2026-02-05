#!/usr/bin/env python3
"""
Script de prueba ULTRA SIMPLE para VLC en Windows
Esto es lo más básico posible para aislar el problema
"""

import sys
import os
from pathlib import Path

print("=" * 70)
print("🔧 TEST ULTRA SIMPLE DE REPRODUCCIÓN DE AUDIO")
print("=" * 70)

# 1. Verificar Python
print("\n1️⃣  PYTHON")
print(f"   Versión: {sys.version}")
print(f"   Ejecutable: {sys.executable}")

# 2. Buscar archivos MP3
print("\n2️⃣  BUSCANDO ARCHIVOS MP3")
project_root = Path(__file__).parent.parent
songs_dir = project_root / 'canciones'
print(f"   Carpeta: {songs_dir}")
print(f"   Existe: {songs_dir.exists()}")

mp3_files = list(songs_dir.glob('*.mp3'))
print(f"   Archivos MP3: {len(mp3_files)}")

if mp3_files:
    test_file = mp3_files[0]
    print(f"   Primer archivo: {test_file.name}")
    print(f"   Ruta absoluta: {test_file.absolute()}")
    print(f"   Existe: {test_file.exists()}")
    print(f"   Tamaño: {test_file.stat().st_size} bytes")
else:
    print("   ❌ NO HAY ARCHIVOS MP3")
    sys.exit(1)

# 3. Probar VLC
print("\n3️⃣  PROBANDO VLC")
try:
    import vlc
    print(f"   ✅ VLC importado")
    print(f"   Versión: {vlc.__version__}")
except ImportError as e:
    print(f"   ❌ VLC NO DISPONIBLE: {e}")
    print("   Instala: python -m pip install python-vlc==3.0.20123")
    sys.exit(1)

# 4. Test de reproducción ultra simple
print("\n4️⃣  TEST DE REPRODUCCIÓN")
print("   ⚠️  REPRODUCE DURANTE 3 SEGUNDOS...")

try:
    # Crear instancia VLC mínima
    instance = vlc.Instance()
    print(f"   ✅ Instancia VLC creada")
    
    # Crear media list
    media_list = instance.media_list_new()
    print(f"   ✅ Media list creada")
    
    # Agregar archivo
    test_file_str = str(test_file.absolute())
    print(f"   Reproduciendo: {test_file_str}")
    
    media = instance.media_new(test_file_str)
    media_list.add_media(media)
    print(f"   ✅ Media agregada")
    
    # Crear reproductor
    player = instance.list_player_new()
    player.set_media_list(media_list)
    print(f"   ✅ Reproductor creado")
    
    # Reproducir
    result = player.play()
    print(f"   ✅ Reproducción iniciada (resultado: {result})")
    
    # Esperar
    import time
    print(f"   ⏳ Esperando 3 segundos...")
    time.sleep(3)
    
    # Detener
    player.stop()
    print(f"   ✅ Reproducción detenida")
    
    print("\n✅ ¡PRUEBA EXITOSA! VLC funciona correctamente")
    
except vlc.libvlc_exception as e:
    print(f"   ❌ ERROR DE VLC: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("💡 Si llegaste aquí, VLC funciona")
print("   El problema está en la integración con Flask/API")
print("=" * 70)
