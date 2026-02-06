#!/usr/bin/env python3
"""API REST para MusicBell v2.0"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os, socket, threading, logging, subprocess, time
from pathlib import Path
from datetime import datetime
from music_player import MusicScheduler
from utils import obtener_duracion_mp3, parsear_duracion_a_segundos, parsear_hora_a_segundos

project_root = Path(__file__).parent.parent
frontend_dir = str(project_root / 'frontend')
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
CORS(app)

app.config['UPLOAD_FOLDER'] = project_root / 'canciones'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = None
server_ip = None
server_port = None


def liberar_puerto_5000():
    """
    Libera el puerto 5000 matando cualquier proceso que lo esté usando
    Compatible con macOS y Linux
    """
    PORT = 5000
    try:
        # Usar lsof y kill (disponible en macOS y Linux)
        try:
            result = subprocess.run(
                f'lsof -i :{PORT}',
                shell=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                # Procesar output de lsof
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip():
                        pid = line.split()[1]
                        try:
                            os.kill(int(pid), 9)
                            logger.info(f"Proceso {pid} en puerto {PORT} terminado")
                        except:
                            pass
        except Exception as e:
            logger.warning(f"No se pudo liberar puerto: {e}")
        
        # Esperar un momento para asegurar que el puerto se libere
        time.sleep(1)
        logger.info(f"Puerto {PORT} liberado correctamente")
        return True
        
    except Exception as e:
        logger.error(f"Error liberando puerto {PORT}: {e}")
        return False

@app.route('/api/canciones', methods=['GET'])
def get_canciones():
    try:
        scheduler.load_config()
        canciones = scheduler.config.get('canciones', [])
        duraciones_actualizadas = False
        for cancion in canciones:
            if 'duracion' not in cancion or not cancion['duracion']:
                archivo_path = project_root / 'canciones' / cancion.get('archivo', '')
                if archivo_path.exists():
                    duracion = obtener_duracion_mp3(str(archivo_path))
                    cancion['duracion'] = duracion if duracion else 'N/A'
                    duraciones_actualizadas = True
                else:
                    cancion['duracion'] = 'N/A'
                    duraciones_actualizadas = True
        if duraciones_actualizadas:
            scheduler.save_config()
        return jsonify(canciones)
    except Exception as e:
        logger.error(f"Error obteniendo canciones: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/canciones', methods=['POST'])
def add_cancion():
    try:
        data = request.json
        scheduler.load_config()
        required_fields = ['nombre', 'archivo', 'tipo_planificacion']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        if data['tipo_planificacion'] != 'ninguno' and 'hora' not in data:
            return jsonify({'error': 'La hora es requerida'}), 400
        
        nueva_cancion = {
            'id': len(scheduler.config.get('canciones', [])) + 1,
            'nombre': data['nombre'],
            'archivo': data['archivo'],
            'tipo_planificacion': data['tipo_planificacion'],
            'habilitada': data.get('habilitada', True),
            'archivado': False
        }
        
        archivo_path = project_root / 'canciones' / data['archivo']
        if archivo_path.exists():
            duracion = obtener_duracion_mp3(str(archivo_path))
            nueva_cancion['duracion'] = duracion if duracion else 'N/A'
        else:
            nueva_cancion['duracion'] = 'N/A'
        
        if 'hora' in data:
            nueva_cancion['hora'] = data['hora']
        if 'fecha' in data:
            nueva_cancion['fecha'] = data['fecha']
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
    try:
        scheduler.load_config()
        return jsonify(scheduler.config.get('estado_reproduccion', {}))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/archivos', methods=['GET'])
def get_archivos():
    try:
        songs_dir = project_root / 'canciones'
        archivos = []
        if songs_dir.exists():
            for file in songs_dir.iterdir():
                if file.suffix.lower() == '.mp3':
                    archivos.append({'nombre': file.name, 'tamaño': file.stat().st_size})
        return jsonify(archivos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/archivos-detalle', methods=['GET'])
def get_archivos_detalle():
    """Obtiene lista detallada de archivos MP3 con información extendida"""
    try:
        songs_dir = project_root / 'canciones'
        archivos = []
        if songs_dir.exists():
            for file in songs_dir.iterdir():
                if file.suffix.lower() == '.mp3':
                    try:
                        duracion = obtener_duracion_mp3(str(file))
                        archivos.append({
                            'nombre': file.name,
                            'tamaño': file.stat().st_size,
                            'duracion': duracion if duracion else 'N/A',
                            'fecha_modificacion': file.stat().st_mtime
                        })
                    except:
                        archivos.append({
                            'nombre': file.name,
                            'tamaño': file.stat().st_size,
                            'duracion': 'N/A',
                            'fecha_modificacion': file.stat().st_mtime
                        })
        # Ordenar por nombre
        archivos.sort(key=lambda x: x['nombre'])
        return jsonify(archivos)
    except Exception as e:
        logger.error(f"Error obteniendo archivos detalle: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/archivos/<archivo_actual>', methods=['PUT'])
def renombrar_archivo(archivo_actual):
    """Renombra un archivo MP3"""
    try:
        data = request.json
        if 'nombre_nuevo' not in data:
            return jsonify({'error': 'Campo nombre_nuevo requerido'}), 400
        
        # Validar nombres
        archivo_actual_name = secure_filename(archivo_actual)
        nombre_nuevo = secure_filename(data['nombre_nuevo'])
        
        if not archivo_actual_name.lower().endswith('.mp3'):
            nombre_nuevo = nombre_nuevo + '.mp3' if not nombre_nuevo.lower().endswith('.mp3') else nombre_nuevo
        
        if not nombre_nuevo.lower().endswith('.mp3'):
            return jsonify({'error': 'El archivo debe ser MP3'}), 400
        
        songs_dir = project_root / 'canciones'
        archivo_path = songs_dir / archivo_actual_name
        archivo_nuevo_path = songs_dir / nombre_nuevo
        
        # Validar que el archivo actual existe
        if not archivo_path.exists():
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        # Validar que el nuevo nombre no existe
        if archivo_nuevo_path.exists():
            return jsonify({'error': 'Ya existe un archivo con ese nombre'}), 409
        
        # Renombrar archivo
        archivo_path.rename(archivo_nuevo_path)
        
        logger.info(f"Archivo renombrado: {archivo_actual_name} -> {nombre_nuevo}")
        return jsonify({
            'mensaje': 'Archivo renombrado exitosamente',
            'nombre_anterior': archivo_actual_name,
            'nombre_nuevo': nombre_nuevo
        }), 200
    except Exception as e:
        logger.error(f"Error renombrando archivo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/archivos/<archivo>', methods=['DELETE'])
def eliminar_archivo(archivo):
    """Elimina un archivo MP3 de la carpeta canciones"""
    try:
        archivo_name = secure_filename(archivo)
        songs_dir = project_root / 'canciones'
        archivo_path = songs_dir / archivo_name
        
        # Validar que el archivo existe
        if not archivo_path.exists():
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        # Validar que es un archivo MP3
        if not archivo_name.lower().endswith('.mp3'):
            return jsonify({'error': 'Solo se pueden eliminar archivos MP3'}), 400
        
        # Eliminar archivo
        archivo_path.unlink()
        
        logger.info(f"Archivo eliminado: {archivo_name}")
        return jsonify({
            'mensaje': 'Archivo eliminado exitosamente',
            'archivo': archivo_name
        }), 200
    except Exception as e:
        logger.error(f"Error eliminando archivo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/detectar-conflictos', methods=['GET'])
def detectar_conflictos():
    try:
        scheduler.load_config()
        conflictos = {}
        canciones = scheduler.config.get('canciones', [])
        canciones_filtradas = [c for c in canciones if c.get('habilitada', True) and not c.get('archivado', False)]
        
        por_fecha = {}
        for cancion in canciones_filtradas:
            fecha = cancion.get('fecha', '2099-12-31')
            if fecha not in por_fecha:
                por_fecha[fecha] = []
            
            hora_inicio = parsear_hora_a_segundos(cancion.get('hora', '00:00'))
            duracion = parsear_duracion_a_segundos(cancion.get('duracion'))
            hora_fin = hora_inicio + duracion
            
            por_fecha[fecha].append({
                'nombre': cancion.get('nombre'),
                'hora_inicio': hora_inicio,
                'hora_fin': hora_fin,
                'hora_str': cancion.get('hora')
            })
        
        for fecha, canciones_dia in por_fecha.items():
            for i, cancion1 in enumerate(canciones_dia):
                for cancion2 in canciones_dia[i+1:]:
                    if (cancion1['hora_inicio'] < cancion2['hora_fin'] and 
                        cancion1['hora_fin'] > cancion2['hora_inicio']):
                        clave = f"{fecha} {cancion1['hora_str']}"
                        if clave not in conflictos:
                            conflictos[clave] = []
                        conflictos[clave].append(cancion1['nombre'])
                        conflictos[clave].append(cancion2['nombre'])
        
        for clave in conflictos:
            conflictos[clave] = list(set(conflictos[clave]))
        
        conflictos_reales = {k: v for k, v in conflictos.items() if len(v) > 1}
        return jsonify({'conflictos': conflictos_reales if conflictos_reales else None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/detener', methods=['POST'])
def detener_cancion():
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
    try:
        song_path = project_root / 'canciones' / nombre_archivo
        if not song_path.exists():
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        scheduler.play_song(str(song_path))
        scheduler.load_config()
        # Guardar el archivo sin la extensión .mp3
        archivo_sin_ext = nombre_archivo.replace('.mp3', '').replace('.MP3', '')
        scheduler.config['estado_reproduccion']['reproduciendo'] = True
        scheduler.config['estado_reproduccion']['cancion_actual'] = archivo_sin_ext
        scheduler.config['estado_reproduccion']['fecha_ultima_actualizacion'] = datetime.now().isoformat()
        scheduler.save_config()
        
        logger.info(f"Reproducción manual: {nombre_archivo}")
        return jsonify({'mensaje': 'Reproduciendo...', 'cancion': nombre_archivo})
    except Exception as e:
        logger.error(f"Error reproduciendo canción: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/datos-remoto', methods=['GET'])
def get_datos_remoto():
    global server_ip, server_port
    try:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
        except:
            ip_local = socket.gethostbyname(socket.gethostname())
        
        return jsonify({
            'ip': ip_local,
            'puerto': server_port or 5000,
            'url_remota': f'http://{ip_local}:{server_port or 5000}'
        })
    except Exception as e:
        logger.error(f"Error obteniendo datos remoto: {e}")
        return jsonify({
            'ip': '127.0.0.1',
            'puerto': server_port or 5000,
            'error': str(e)
        }), 500

@app.route('/api/cargar-archivo', methods=['POST'])
def cargar_archivo():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        if not file.filename.lower().endswith('.mp3'):
            return jsonify({'error': 'Solo se permiten archivos MP3'}), 400
        
        filename = secure_filename(file.filename)
        UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
        UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        
        filepath = UPLOAD_FOLDER / filename
        file.save(str(filepath))
        
        logger.info(f"Archivo cargado: {filename}")
        duracion = obtener_duracion_mp3(str(filepath))
        
        return jsonify({
            'mensaje': 'Archivo cargado exitosamente',
            'nombre': filename,
            'tamaño': filepath.stat().st_size,
            'duracion': duracion
        }), 201
    
    except Exception as e:
        logger.error(f"Error cargando archivo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/apagar', methods=['POST'])
def apagar_aplicacion():
    try:
        scheduler.stop_current_song()
        scheduler.stop()
        import signal
        import threading
        # Apagar en un thread para que el response se envíe correctamente
        def shutdown():
            import time
            time.sleep(0.5)
            os.kill(os.getpid(), signal.SIGTERM)
        threading.Thread(target=shutdown, daemon=True).start()
        return jsonify({'mensaje': 'Aplicación apagada'})
    except Exception as e:
        logger.error(f"Error apagando aplicación: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/canciones/<nombre_archivo>')
def descargar_cancion(nombre_archivo):
    try:
        return send_from_directory(str(project_root / 'canciones'), nombre_archivo)
    except Exception as e:
        logger.error(f"Error descargando canción: {e}")
        return jsonify({'error': str(e)}), 404

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

def init_scheduler():
    global scheduler
    scheduler = MusicScheduler()
    scheduler.run()

if __name__ == '__main__':
    # Liberar puerto 5000 antes de iniciar
    logger.info("Verificando instancias anteriores...")
    liberar_puerto_5000()
    
    (project_root / 'canciones').mkdir(parents=True, exist_ok=True)
    (project_root / 'config').mkdir(parents=True, exist_ok=True)
    (project_root / 'logs').mkdir(parents=True, exist_ok=True)
    
    scheduler_thread = threading.Thread(target=init_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Usar siempre puerto 5000
    server_port = 5000
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        server_ip = s.getsockname()[0]
        s.close()
    except:
        server_ip = '127.0.0.1'
    
    print(f"\n{'='*50}")
    print(f"🎵 MusicBell - Sistema de Reproducción Automática")
    print(f"{'='*50}")
    print(f"📡 Servidor en: http://localhost:{server_port}")
    print(f"🌐 Acceso remoto: http://{server_ip}:{server_port}")
    print(f"{'='*50}\n")
    
    app.run(host='0.0.0.0', port=server_port, debug=False)
