#!/usr/bin/env python3
"""
Script auxiliar para gestionar MusicBell desde línea de comandos
Útil para automatización y administración
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

CONFIG_PATH = 'config/canciones.json'
SONGS_DIR = 'canciones'

def cargar_config():
    """Carga la configuración actual"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'canciones': [], 'estado_reproduccion': {}}

def guardar_config(config):
    """Guarda la configuración"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def listar_canciones():
    """Lista todas las canciones"""
    config = cargar_config()
    canciones = config.get('canciones', [])
    
    if not canciones:
        print("No hay canciones programadas")
        return
    
    print(f"\n{'ID':<5} {'Nombre':<20} {'Hora':<8} {'Tipo':<15} {'Habilitada':<10}")
    print("-" * 70)
    
    for cancion in canciones:
        print(f"{cancion['id']:<5} {cancion['nombre']:<20} {cancion['hora']:<8} "
              f"{cancion['tipo_planificacion']:<15} {'✓' if cancion.get('habilitada', True) else '✗':<10}")

def agregar_cancion(nombre, archivo, tipo, hora, **kwargs):
    """Agrega una nueva canción"""
    config = cargar_config()
    
    # Validar que el archivo existe
    ruta_archivo = os.path.join(SONGS_DIR, archivo)
    if not os.path.exists(ruta_archivo):
        print(f"Error: Archivo no encontrado: {ruta_archivo}")
        return False
    
    # Crear nueva canción
    nuevo_id = max([c['id'] for c in config.get('canciones', [])], default=0) + 1
    
    nueva_cancion = {
        'id': nuevo_id,
        'nombre': nombre,
        'archivo': archivo,
        'tipo_planificacion': tipo,
        'hora': hora,
        'habilitada': True
    }
    
    # Añadir parámetros opcionales
    if tipo == 'fecha' and 'fecha' in kwargs:
        nueva_cancion['fecha'] = kwargs['fecha']
    elif tipo == 'dia_semana' and 'dias' in kwargs:
        nueva_cancion['dias'] = kwargs['dias']
    
    config['canciones'].append(nueva_cancion)
    guardar_config(config)
    
    print(f"✓ Canción agregada: {nombre} (ID: {nuevo_id})")
    return True

def eliminar_cancion(cancion_id):
    """Elimina una canción por ID"""
    config = cargar_config()
    
    original_len = len(config['canciones'])
    config['canciones'] = [c for c in config['canciones'] if c['id'] != cancion_id]
    
    if len(config['canciones']) < original_len:
        guardar_config(config)
        print(f"✓ Canción eliminada (ID: {cancion_id})")
        return True
    else:
        print(f"Error: Canción no encontrada (ID: {cancion_id})")
        return False

def listar_archivos():
    """Lista archivos MP3 disponibles"""
    if not os.path.exists(SONGS_DIR):
        print("No existe la carpeta 'canciones'")
        return
    
    archivos = [f for f in os.listdir(SONGS_DIR) if f.endswith('.mp3')]
    
    if not archivos:
        print("No hay archivos MP3 en la carpeta 'canciones'")
        return
    
    print(f"\nArchivos MP3 disponibles ({len(archivos)}):")
    print("-" * 50)
    
    for archivo in sorted(archivos):
        ruta = os.path.join(SONGS_DIR, archivo)
        tamaño = os.path.getsize(ruta) / (1024 * 1024)  # MB
        print(f"  • {archivo:<40} ({tamaño:.1f} MB)")

def detectar_conflictos():
    """Detecta conflictos de horarios"""
    config = cargar_config()
    conflictos = {}
    
    for cancion in config.get('canciones', []):
        if not cancion.get('habilitada', True):
            continue
        
        clave = cancion['hora']
        if clave not in conflictos:
            conflictos[clave] = []
        conflictos[clave].append(cancion['nombre'])
    
    conflictos_reales = {k: v for k, v in conflictos.items() if len(v) > 1}
    
    if not conflictos_reales:
        print("\n✓ No hay conflictos de horario")
        return
    
    print("\n⚠️  Conflictos encontrados:")
    print("-" * 50)
    
    for hora, canciones in sorted(conflictos_reales.items()):
        print(f"\n  {hora}: {len(canciones)} canciones")
        for cancion in canciones:
            print(f"    • {cancion}")

def mostrar_estado():
    """Muestra el estado actual"""
    config = cargar_config()
    estado = config.get('estado_reproduccion', {})
    
    print("\nEstado Actual:")
    print("-" * 50)
    print(f"Reproduciendo: {'Sí ✓' if estado.get('reproduciendo') else 'No'}")
    print(f"Canción actual: {estado.get('cancion_actual', 'Ninguna')}")
    print(f"Última actualización: {estado.get('fecha_ultima_actualizacion', 'N/A')}")

def main():
    """Interfaz de línea de comandos"""
    
    if len(sys.argv) < 2:
        print("""
MusicBell - Gestor de Línea de Comandos

Uso:
  python cli.py listar                    # Listar todas las canciones
  python cli.py archivos                  # Listar archivos MP3 disponibles
  python cli.py agregar <nombre> <archivo> <tipo> <hora> [extras]
                                          # Agregar canción
  python cli.py eliminar <id>             # Eliminar canción
  python cli.py conflictos                # Detectar conflictos
  python cli.py estado                    # Ver estado actual

Tipos de planificación:
  - hora        : Todos los días a una hora
  - fecha       : Un día específico (requiere --fecha YYYY-MM-DD)
  - dia_semana  : Días específicos (requiere --dias lunes,viernes)

Ejemplos:
  python cli.py agregar "Himno" "himno.mp3" "hora" "08:00"
  python cli.py agregar "Evento" "evento.mp3" "fecha" "15:30" --fecha 2026-02-14
  python cli.py agregar "Recreo" "musica.mp3" "dia_semana" "12:00" --dias viernes
""")
        return
    
    comando = sys.argv[1]
    
    if comando == 'listar':
        listar_canciones()
    
    elif comando == 'archivos':
        listar_archivos()
    
    elif comando == 'conflictos':
        detectar_conflictos()
    
    elif comando == 'estado':
        mostrar_estado()
    
    elif comando == 'agregar' and len(sys.argv) >= 6:
        nombre = sys.argv[2]
        archivo = sys.argv[3]
        tipo = sys.argv[4]
        hora = sys.argv[5]
        
        kwargs = {}
        for i in range(6, len(sys.argv), 2):
            if sys.argv[i].startswith('--'):
                key = sys.argv[i][2:]
                if i + 1 < len(sys.argv):
                    kwargs[key] = sys.argv[i + 1]
        
        agregar_cancion(nombre, archivo, tipo, hora, **kwargs)
    
    elif comando == 'eliminar' and len(sys.argv) >= 3:
        try:
            cancion_id = int(sys.argv[2])
            eliminar_cancion(cancion_id)
        except ValueError:
            print("Error: El ID debe ser un número")
    
    else:
        print(f"Comando no reconocido: {comando}")

if __name__ == '__main__':
    main()
