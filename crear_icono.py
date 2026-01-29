#!/usr/bin/env python3
"""
Script para generar un icono para MusicBell
Crea un archivo icon.ico que puede usarse para el acceso directo
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def crear_icono_musicbell():
    """Crea un icono .ico para MusicBell"""
    
    # Tamaños de icono estándar para Windows
    tamanos = [256, 128, 64, 48, 32, 16]
    imagenes = []
    
    for tamano in tamanos:
        # Crear imagen con fondo degradado (azul-púrpura)
        img = Image.new('RGB', (tamano, tamano), color=(20, 20, 60))
        draw = ImageDraw.Draw(img)
        
        # Dibujar degradado simple (cuadrados de colores)
        for i in range(tamano):
            # Gradiente de azul a púrpura
            r = int(20 + (100 - 20) * (i / tamano))
            g = int(20 + (40 - 20) * (i / tamano))
            b = int(60 + (120 - 60) * (i / tamano))
            draw.line([(0, i), (tamano, i)], fill=(r, g, b))
        
        # Dibujar símbolo de nota musical (♪)
        # Centro del icono
        cx, cy = tamano // 2, tamano // 2
        radio = int(tamano * 0.25)
        
        # Círculo central (cabeza de la nota)
        draw.ellipse(
            [(cx - radio, cy - radio), (cx + radio, cy + radio)],
            fill=(255, 215, 0),  # Oro
            outline=(255, 200, 0)
        )
        
        # Línea vertical (tallo de la nota)
        tail_top = cy - int(tamano * 0.4)
        draw.rectangle(
            [(cx + radio - 2, tail_top), (cx + radio + 2, cy - radio)],
            fill=(255, 215, 0)
        )
        
        # Bandera (corchea decorativa)
        draw.polygon(
            [
                (cx + radio + 2, tail_top),
                (cx + int(radio * 1.8), tail_top + int(radio * 0.6)),
                (cx + radio + 2, tail_top + int(radio * 0.8))
            ],
            fill=(255, 215, 0)
        )
        
        imagenes.append(img)
    
    # Guardar como .ico
    ruta_ico = os.path.join(os.path.dirname(__file__), 'icon.ico')
    imagenes[0].save(ruta_ico, format='ICO', sizes=[(img.width, img.height) for img in imagenes])
    
    print(f"✓ Icono creado: {ruta_ico}")
    return ruta_ico

if __name__ == '__main__':
    try:
        # Verificar si PIL está disponible
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            print("Instalando Pillow para generar icono...")
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow'])
            from PIL import Image, ImageDraw
        
        crear_icono_musicbell()
        print("Icono generado exitosamente")
        
    except Exception as e:
        print(f"Error al crear el icono: {e}")
        sys.exit(1)
