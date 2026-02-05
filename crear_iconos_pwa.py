#!/usr/bin/env python3
"""
Script para generar iconos PNG para PWA
Crea iconos de diferentes tamaños para la Progressive Web App
"""

from PIL import Image, ImageDraw
import os
from pathlib import Path

# Tamaños a generar
SIZES = {
    96: 'icon-96.png',
    192: 'icon-192.png',
    512: 'icon-512.png',
}

# Color del fondo (indigo)
BACKGROUND_COLOR = '#6366f1'
# Color de la cara (amarillo)
FACE_COLOR = '#fbbf24'
# Color de los ojos y boca (negro)
EXPRESSION_COLOR = '#000000'

def create_smiley_icon(size):
    """Crea un icono de cara sonriente"""
    
    # Crear imagen con fondo
    img = Image.new('RGBA', (size, size), BACKGROUND_COLOR + 'FF')
    draw = ImageDraw.Draw(img)
    
    # Margen
    margin = size * 0.1
    face_x = margin
    face_y = margin
    face_size = size - (margin * 2)
    
    # Dibujar cara (círculo amarillo)
    draw.ellipse(
        [face_x, face_y, face_x + face_size, face_y + face_size],
        fill=FACE_COLOR
    )
    
    # Tamaño de los ojos
    eye_radius = size * 0.08
    eye_distance = face_size * 0.3
    
    # Posición de los ojos
    center_x = face_x + face_size / 2
    center_y = face_y + face_size / 2.5
    
    # Dibujar ojo izquierdo
    left_eye_x = center_x - eye_distance
    draw.ellipse(
        [left_eye_x - eye_radius, center_y - eye_radius,
         left_eye_x + eye_radius, center_y + eye_radius],
        fill=EXPRESSION_COLOR
    )
    
    # Dibujar ojo derecho
    right_eye_x = center_x + eye_distance
    draw.ellipse(
        [right_eye_x - eye_radius, center_y - eye_radius,
         right_eye_x + eye_radius, center_y + eye_radius],
        fill=EXPRESSION_COLOR
    )
    
    # Dibujar boca (sonrisa)
    mouth_y = center_y + face_size * 0.25
    mouth_width = face_size * 0.3
    mouth_height = face_size * 0.15
    
    # Línea de sonrisa (arco)
    for i in range(int(mouth_width * 2)):
        x = center_x - mouth_width + i
        # Fórmula para arco parabólico
        y = mouth_y + (mouth_height * (1 - (2 * i / (mouth_width * 2) - 1) ** 2))
        draw.ellipse(
            [x - 2, y - 2, x + 2, y + 2],
            fill=EXPRESSION_COLOR
        )
    
    return img

def create_maskable_icon(size):
    """Crea un icono maskable para PWA (sin márgenes)"""
    
    # Crear imagen con transparencia
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Margen mínimo para maskable
    margin = size * 0.05
    face_x = margin
    face_y = margin
    face_size = size - (margin * 2)
    
    # Dibujar cara (círculo amarillo)
    draw.ellipse(
        [face_x, face_y, face_x + face_size, face_y + face_size],
        fill=FACE_COLOR
    )
    
    # Tamaño de los ojos
    eye_radius = size * 0.08
    eye_distance = face_size * 0.3
    
    # Posición de los ojos
    center_x = face_x + face_size / 2
    center_y = face_y + face_size / 2.5
    
    # Dibujar ojo izquierdo
    left_eye_x = center_x - eye_distance
    draw.ellipse(
        [left_eye_x - eye_radius, center_y - eye_radius,
         left_eye_x + eye_radius, center_y + eye_radius],
        fill=EXPRESSION_COLOR
    )
    
    # Dibujar ojo derecho
    right_eye_x = center_x + eye_distance
    draw.ellipse(
        [right_eye_x - eye_radius, center_y - eye_radius,
         right_eye_x + eye_radius, center_y + eye_radius],
        fill=EXPRESSION_COLOR
    )
    
    # Dibujar boca (sonrisa)
    mouth_y = center_y + face_size * 0.25
    mouth_width = face_size * 0.3
    mouth_height = face_size * 0.15
    
    # Línea de sonrisa (arco)
    for i in range(int(mouth_width * 2)):
        x = center_x - mouth_width + i
        # Fórmula para arco parabólico
        y = mouth_y + (mouth_height * (1 - (2 * i / (mouth_width * 2) - 1) ** 2))
        draw.ellipse(
            [x - 2, y - 2, x + 2, y + 2],
            fill=EXPRESSION_COLOR
        )
    
    return img

def main():
    # Crear carpeta images si no existe
    script_dir = Path(__file__).parent
    images_dir = script_dir / 'frontend' / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎨 Generando iconos para PWA...\n")
    
    # Generar iconos normales
    print("📱 Iconos normales:")
    for size, filename in SIZES.items():
        img = create_smiley_icon(size)
        path = images_dir / filename
        img.save(path)
        print(f"   ✅ {filename} ({size}x{size})")
    
    # Generar iconos maskable
    print("\n🎭 Iconos maskable:")
    for size in SIZES.keys():
        img = create_maskable_icon(size)
        path = images_dir / f'icon-maskable-{size}.png'
        img.save(path)
        print(f"   ✅ icon-maskable-{size}.png ({size}x{size})")
    
    print("\n✅ Iconos generados correctamente en: frontend/images/")
    print("\n📁 Archivos creados:")
    for file in sorted(images_dir.glob('*.png')):
        size_kb = file.stat().st_size / 1024
        print(f"   - {file.name} ({size_kb:.1f} KB)")

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("❌ PIL (Pillow) no está instalado")
        print("   Instala con: pip install pillow")
    except Exception as e:
        print(f"❌ Error: {e}")
