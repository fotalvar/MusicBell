#!/usr/bin/env python3
"""
API REST para gestionar MusicBell desde interfaz web
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from pathlib import Path
import threading
import logging
from datetime import datetime
from music_player import MusicScheduler
from utils import obtener_duracion_mp3, parsear_duracion_a_segundos, parsear_hora_a_segundos

try:
    from mutagen.mp3 import MP3
except ImportError:
    MP3 = None

# Obtener rutas del proyecto
project_root = Path(__file__).parent.parent
frontend_dir = str(project_root / 'frontend')

# Configurar Flask
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
CORS(app)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Scheduler global
scheduler = None

# ============= RUTAS DE CONFIGURACIÓN =============

@app.route('/api/canciones', methods=['GET'])
def get_canciones():
    """Obtiene lista de canciones"""
    try:
        scheduler.load_config()
        canciones = scheduler.config.get('canciones', [])
        
        # Asegurar que cada canción tiene duración - SIEMPRE intentar cargarla
        duraciones_actualizadas = False
        for cancion in canciones:
            # Si no existe duración o está vacía, intentar cargarla
            if 'duracion' not in cancion or not cancion['duracion']:
                archivo_path = project_root / 'canciones' / cancion.get('archivo', '')
                if archivo_path.exists():
                    duracion = obtener_duracion_mp3(str(archivo_path))
                    if duracion:
                        cancion['duracion'] = duracion
                        duraciones_actualizadas = True
                    else:
                        # Si no se puede obtener duración, asignar N/A
                        cancion['duracion'] = 'N/A'
                        duraciones_actualizadas = True
                else:
                    cancion['duracion'] = 'N/A'
                    duraciones_actualizadas = True
        
        # Si se actualizaron duraciones, guardar en archivo
        if duraciones_actualizadas:
            scheduler.save_config()
                    
        return jsonify(canciones)
    except Exception as e:
        logger.error(f"Error obteniendo canciones: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/canciones', methods=['POST'])
def add_cancion():
    """Añade una nueva canción"""
    try:
        data = request.json
        scheduler.load_config()
        
        # Validar datos requeridos
        required_fields = ['nombre', 'archivo', 'tipo_planificacion']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # La hora es requerida solo si no es "ninguno"
        if data['tipo_planificacion'] != 'ninguno' and 'hora' not in data:
            return jsonify({'error': 'La hora es requerida para este tipo de planificación'}), 400
        
        # Crear nueva canción
        nueva_cancion = {
            'id': len(scheduler.config.get('canciones', [])) + 1,
            'nombre': data['nombre'],
            'archivo': data['archivo'],
            'tipo_planificacion': data['tipo_planificacion'],
            'habilitada': data.get('habilitada', True),
            'archivado': False
        }
        
        # Obtener duración del archivo MP3 - SIEMPRE intentar
        archivo_path = project_root / 'canciones' / data['archivo']
        if archivo_path.exists():
            duracion = obtener_duracion_mp3(str(archivo_path))
            nueva_cancion['duracion'] = duracion if duracion else 'N/A'
        else:
            nueva_cancion['duracion'] = 'N/A'
            logger.warning(f"Archivo no encontrado: {archivo_path}")
        
        # Añadir hora si está disponible
        if 'hora' in data:
            nueva_cancion['hora'] = data['hora']
        
        # Añadir fecha si está disponible
        if 'fecha' in data:
            nueva_cancion['fecha'] = data['fecha']
        
        # Añadir campos opcionales según tipo de planificación
        if data['tipo_planificacion'] == 'fecha':
            nueva_cancion['fecha'] = data.get('fecha')
        elif data['tipo_planificacion'] == 'dia_semana':
            nueva_cancion['dias'] = data.get('dias', [])
        
        scheduler.config['canciones'].append(nueva_cancion)
        scheduler.save_config()
        
        logger.info(f"Canción añadida: {data['nombre']}")
        return jsonify(nueva_cancion), 201
    except Exception as e:
        logger.error(f"Error añadiendo canción: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/canciones/<int:cancion_id>', methods=['PUT'])
def update_cancion(cancion_id):
    """Actualiza una canción existente"""
    try:
        data = request.json
        scheduler.load_config()
        
        canciones = scheduler.config.get('canciones', [])
        for i, cancion in enumerate(canciones):
            if cancion.get('id') == cancion_id:
                canciones[i].update(data)
                scheduler.save_config()
                logger.info(f"Canción actualizada: {cancion_id}")
                return jsonify(canciones[i]), 200
        
        return jsonify({'error': 'Canción no encontrada'}), 404
    except Exception as e:
        logger.error(f"Error actualizando canción: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/canciones/<int:cancion_id>', methods=['DELETE'])
def delete_cancion(cancion_id):
    """Elimina una canción"""
    try:
        scheduler.load_config()
        
        canciones = scheduler.config.get('canciones', [])
        scheduler.config['canciones'] = [c for c in canciones if c.get('id') != cancion_id]
        scheduler.save_config()
        
        logger.info(f"Canción eliminada: {cancion_id}")
        return jsonify({'mensaje': 'Canción eliminada'}), 200
    except Exception as e:
        logger.error(f"Error eliminando canción: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/estado', methods=['GET'])
def get_estado():
    """Obtiene estado actual del reproductor"""
    try:
        scheduler.load_config()
        return jsonify(scheduler.config.get('estado_reproduccion', {}))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/archivos', methods=['GET'])
def get_archivos():
    """Lista archivos de música disponibles"""
    try:
        songs_dir = project_root / 'canciones'
        archivos = []
        
        if songs_dir.exists():
            for file in songs_dir.iterdir():
                if file.suffix.lower() == '.mp3':
                    archivos.append({
                        'nombre': file.name,
                        'tamaño': file.stat().st_size
                    })
        
        return jsonify(archivos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/detectar-conflictos', methods=['GET'])
def detectar_conflictos():
    """Detecta conflictos de horarios considerando la duración"""
    try:
        scheduler.load_config()
        conflictos = {}
        
        canciones = scheduler.config.get('canciones', [])
        canciones_filtradas = [c for c in canciones if c.get('habilitada', True) and not c.get('archivado', False)]
        
        # Agrupar por fecha y crear timeline
        por_fecha = {}
        for cancion in canciones_filtradas:
            fecha = cancion.get('fecha', '2099-12-31')
            if fecha not in por_fecha:
                por_fecha[fecha] = []
            
            hora_inicio = parsear_hora_a_segundos(cancion.get('hora', '00:00'))
            duracion = parsear_duracion_a_segundos(cancion.get('duracion'))
            hora_fin = hora_inicio + duracion
            
            logger.info(f"Canción: {cancion.get('nombre')}, Inicio: {hora_inicio}s, Duracion: {duracion}s, Fin: {hora_fin}s")
            
            por_fecha[fecha].append({
                'nombre': cancion.get('nombre'),
                'hora_inicio': hora_inicio,
                'hora_fin': hora_fin,
                'hora_str': cancion.get('hora')
            })
        
        # Detectar conflictos en cada fecha
        for fecha, canciones_dia in por_fecha.items():
            logger.info(f"Procesando fecha: {fecha}")
            for i, cancion1 in enumerate(canciones_dia):
                for cancion2 in canciones_dia[i+1:]:
                    # Verificar si hay solapamiento
                    if (cancion1['hora_inicio'] < cancion2['hora_fin'] and 
                        cancion1['hora_fin'] > cancion2['hora_inicio']):
                        logger.warning(f"CONFLICTO: {cancion1['nombre']} ({cancion1['hora_inicio']}-{cancion1['hora_fin']}) con {cancion2['nombre']} ({cancion2['hora_inicio']}-{cancion2['hora_fin']})")
                        
                        clave = f"{fecha} {cancion1['hora_str']}"
                        if clave not in conflictos:
                            conflictos[clave] = []
                        conflictos[clave].append(cancion1['nombre'])
                        conflictos[clave].append(cancion2['nombre'])
        
        # Eliminar duplicados y retornar solo conflictos reales
        for clave in conflictos:
            conflictos[clave] = list(set(conflictos[clave]))
        
        conflictos_reales = {k: v for k, v in conflictos.items() if len(v) > 1}
        
        return jsonify({'conflictos': conflictos_reales if conflictos_reales else None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/detener', methods=['POST'])
def detener_cancion():
    """Detiene la canción que está sonando actualmente"""
    try:
        scheduler.stop_current_song()
        scheduler.load_config()
        scheduler.config['estado_reproduccion']['reproduciendo'] = False
        scheduler.config['estado_reproduccion']['cancion_actual'] = None
        scheduler.save_config()
        return jsonify({'mensaje': 'Canción detenida'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reproducir/<nombre_archivo>', methods=['POST'])
def reproducir_cancion(nombre_archivo):
    """Reproduce una canción manualmente por su nombre de archivo"""
    try:
        song_path = project_root / 'canciones' / nombre_archivo
        
        if not song_path.exists():
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        # Reproducir la canción
        scheduler.play_song(str(song_path))
        
        # Actualizar estado
        scheduler.load_config()
        scheduler.config['estado_reproduccion']['reproduciendo'] = True
        scheduler.config['estado_reproduccion']['cancion_actual'] = nombre_archivo
        scheduler.config['estado_reproduccion']['fecha_ultima_actualizacion'] = datetime.now().isoformat()
        scheduler.save_config()
        
        logger.info(f"Reproducción manual: {nombre_archivo}")
        return jsonify({'mensaje': 'Reproduciendo...', 'cancion': nombre_archivo})
    except Exception as e:
        logger.error(f"Error reproduciendo canción: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/apagar', methods=['POST'])
def apagar_aplicacion():
    """Apaga la aplicación completamente"""
    try:
        scheduler.stop_current_song()
        scheduler.stop()
        import os
        import signal
        os.kill(os.getpid(), signal.SIGTERM)
        return jsonify({'mensaje': 'Aplicación apagada'})
    except Exception as e:
        logger.error(f"Error apagando aplicación: {e}")
        return jsonify({'error': str(e)}), 500

# ============= RUTAS FRONTEND =============

@app.route('/')
def index():
    """Sirve la interfaz web"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Sirve archivos estáticos"""
    return send_from_directory('../frontend', path)

# ============= INICIACIÓN =============

def init_scheduler():
    """Inicializa el scheduler en un thread separado"""
    global scheduler
    scheduler = MusicScheduler()
    scheduler.run()

if __name__ == '__main__':
    # Crear directorios si no existen
    (project_root / 'canciones').mkdir(parents=True, exist_ok=True)
    (project_root / 'config').mkdir(parents=True, exist_ok=True)
    (project_root / 'logs').mkdir(parents=True, exist_ok=True)
    
    # Inicializar scheduler en thread separado
    scheduler_thread = threading.Thread(target=init_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Iniciar servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=False)
