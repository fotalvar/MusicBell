#!/usr/bin/env python3
"""
Genera iconos PNG con el mismo diseño de carita que el header del front
Usa PIL para crear los iconos
"""

from PIL import Image, ImageDraw
import os

# Crear directorio si no existe
img_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'images')
os.makedirs(img_dir, exist_ok=True)

def crear_icono_carita(tamaño, es_maskable=False):
    """
    Crea un icono PNG con una carita sonriente
    tamaño: dimensiones en píxeles (e.g., 192)
    es_maskable: si True, usa fondo transparente para iconos maskable
    """
    if es_maskable:
        # Fondo transparente para maskable
        img = Image.new('RGBA', (tamaño, tamaño), (0, 0, 0, 0))
        color_fondo = (99, 102, 241, 255)  # #6366f1 con transparencia
        color_linea = (255, 255, 255, 255)  # Blanco para líneas
    else:
        # Fondo blanco para iconos normales
        img = Image.new('RGBA', (tamaño, tamaño), (255, 255, 255, 255))
        color_fondo = (99, 102, 241, 255)  # #6366f1
        color_linea = (255, 255, 255, 255)  # Blanco para líneas
    
    draw = ImageDraw.Draw(img)
    
    # Calcular tamaños basados en la dimensión
    padding = int(tamaño * 0.1)
    centro_x = tamaño // 2
    centro_y = tamaño // 2
    radio = int((tamaño - padding * 2) // 2)
    
    # Dibujar círculo de fondo (carita)
    x0 = centro_x - radio
    y0 = centro_y - radio
    x1 = centro_x + radio
    y1 = centro_y + radio
    draw.ellipse([x0, y0, x1, y1], fill=color_fondo)
    
    # Dibujar ojo izquierdo
    ojo_radio = int(radio * 0.15)
    ojo_x_izq = centro_x - int(radio * 0.35)
    ojo_y = centro_y - int(radio * 0.2)
    draw.ellipse(
        [ojo_x_izq - ojo_radio, ojo_y - ojo_radio, ojo_x_izq + ojo_radio, ojo_y + ojo_radio],
        fill=color_linea
    )
    
    # Dibujar ojo derecho
    ojo_x_der = centro_x + int(radio * 0.35)
    draw.ellipse(
        [ojo_x_der - ojo_radio, ojo_y - ojo_radio, ojo_x_der + ojo_radio, ojo_y + ojo_radio],
        fill=color_linea
    )
    
    # Dibujar sonrisa (arco)
    sonrisa_y = centro_y + int(radio * 0.1)
    sonrisa_ancho = int(radio * 0.4)
    grosor_linea = max(2, int(tamaño * 0.02))
    
    draw.arc(
        [centro_x - sonrisa_ancho, sonrisa_y, centro_x + sonrisa_ancho, sonrisa_y + sonrisa_ancho],
        0, 180,
        fill=color_linea,
        width=grosor_linea
    )
    
    return img

# Generar iconos
tamaños = [96, 192, 512]

print("Generando iconos con carita...")

for tamaño in tamaños:
    # Icono normal
    print(f"  Creando icon-{tamaño}.png...")
    img = crear_icono_carita(tamaño, es_maskable=False)
    img.save(os.path.join(img_dir, f'icon-{tamaño}.png'))
    
    # Icono maskable
    print(f"  Creando icon-maskable-{tamaño}.png...")
    img_maskable = crear_icono_carita(tamaño, es_maskable=True)
    img_maskable.save(os.path.join(img_dir, f'icon-maskable-{tamaño}.png'))

print("✅ Iconos generados exitosamente en frontend/images/")
print("\nArchivos creados:")
for tamaño in tamaños:
    print(f"  - icon-{tamaño}.png")
    print(f"  - icon-maskable-{tamaño}.png")
