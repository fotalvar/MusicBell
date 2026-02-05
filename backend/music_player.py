#!/usr/bin/env python3
"""
MusicBell - Reproductor de música automático para escuelas
Script principal que se ejecuta en segundo plano
"""

import json
import os
import time
import platform
import logging
import threading
from datetime import datetime
from pathlib import Path
import signal
import subprocess
from utils import parsear_hora_a_segundos

# Configurar logging
# Obtener la ruta del proyecto (padre del backend)
project_root = Path(__file__).parent.parent
logs_dir = project_root / 'logs'
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(logs_dir / 'musicbell.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MusicScheduler:
    def __init__(self, config_path='config/canciones.json', songs_dir='canciones'):
        # Obtener rutas absolutas desde la raíz del proyecto
        project_root = Path(__file__).parent.parent
        
        self.config_path = str(project_root / config_path)
        self.songs_dir = str(project_root / songs_dir)
        self.config = None
        self.current_player = None
        self.current_player_process = None  # Track del reproductor
        self.vlc_instance = None  # Instancia de VLC
        self.running = True
        
        # Crear directorios si no existen
        Path(self.songs_dir).mkdir(parents=True, exist_ok=True)
        Path(project_root / 'logs').mkdir(parents=True, exist_ok=True)
        
        # Cargar configuración
        self.load_config()
        logger.info("MusicBell iniciado")
    
    def load_config(self):
        """Carga la configuración de canciones desde el archivo JSON"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                logger.error(f"Error cargando configuración: {e}")
                self.config = {"canciones": [], "estado_reproduccion": {"reproduciendo": False}}
        else:
            self.config = {"canciones": [], "estado_reproduccion": {"reproduciendo": False}}
    
    def save_config(self):
        """Guarda la configuración actualizada"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")
    
    def get_scheduled_songs_now(self):
        """
        Obtiene las canciones que deben sonar ahora
        Retorna lista de canciones programadas para esta hora
        """
        now = datetime.now()
        current_hour = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")
        
        songs_to_play = []
        
        for song in self.config.get('canciones', []):
            if not song.get('habilitada', True):
                continue
            
            # Verificar por hora
            if song.get('tipo_planificacion') == 'hora':
                if song.get('hora') == current_hour:
                    songs_to_play.append(song)
            
            # Verificar por día específico
            elif song.get('tipo_planificacion') == 'fecha':
                if song.get('fecha') == current_date:
                    if song.get('hora') == current_hour:
                        songs_to_play.append(song)
            
            # Verificar por día de la semana
            elif song.get('tipo_planificacion') == 'dia_semana':
                day_names = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
                current_day = day_names[now.weekday()]
                if current_day in song.get('dias', []):
                    if song.get('hora') == current_hour:
                        songs_to_play.append(song)
        
        return songs_to_play
    
    def play_song(self, song_path):
        """Reproduce una canción usando VLC sin interfaz gráfica"""
        if not os.path.exists(song_path):
            logger.error(f"Archivo no encontrado: {song_path}")
            return False
        
        # Detener canción anterior si está sonando
        self.stop_current_song()
        
        try:
            logger.info(f"Intentando reproducir: {song_path}")
            
            import vlc
            
            # Crear instancia de VLC
            # vlc_instance: instancia de VLC sin interfaz
            vlc_instance = vlc.Instance('--no-xlib')  # Sin interfaz gráfica
            
            # Crear media
            media = vlc_instance.media_list_new()
            media_item = vlc_instance.media_new(song_path)
            media.add_media(media_item)
            
            # Crear list player (reproductor de listas)
            list_player = vlc_instance.list_player_new()
            list_player.set_media_list(media)
            
            # Guardar la instancia para poder detenerla después
            self.current_player_process = list_player
            self.vlc_instance = vlc_instance
            
            # Reproducir
            list_player.play()
            
            logger.info(f"Reproduciendo (VLC): {song_path}")
            return True
                
        except ImportError:
            logger.error("python-vlc no está instalado. Instala con: pip install python-vlc==3.0.20123")
            return False
        except Exception as e:
            logger.error(f"Error reproduciendo canción: {e}")
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return False
    
    
    def stop_current_song(self):
        """Detiene la canción que está sonando actualmente"""
        try:
            # Si es un reproductor VLC
            if self.current_player_process:
                try:
                    # VLC list_player
                    self.current_player_process.stop()
                    logger.info("Música detenida (VLC)")
                except Exception as e:
                    logger.warning(f"Error deteniendo VLC: {e}")
                
                self.current_player_process = None
            
            # Liberar instancia de VLC
            if hasattr(self, 'vlc_instance'):
                try:
                    self.vlc_instance.release()
                except:
                    pass
                self.vlc_instance = None
            
            logger.info("Canción detenida")
            return True
        except Exception as e:
            logger.error(f"Error deteniendo canción: {e}")
            self.current_player_process = None
            return False
    
    def check_conflicts(self, songs):
        """
        Detecta si hay múltiples canciones programadas para el mismo momento
        Retorna información sobre conflictos
        """
        if len(songs) > 1:
            conflict_msg = f"CONFLICTO: {len(songs)} canciones programadas para este momento:"
            for song in songs:
                conflict_msg += f"\n  - {song.get('nombre', 'Sin nombre')}"
            logger.warning(conflict_msg)
            return True, songs
        return False, songs
    
    def run(self):
        """Loop principal que monitorea el reloj"""
        last_check_minute = -1
        
        while self.running:
            try:
                # Recargar configuración cada minuto
                now = datetime.now()
                current_minute = now.minute
                
                if current_minute != last_check_minute:
                    self.load_config()
                    songs = self.get_scheduled_songs_now()
                    
                    if songs:
                        has_conflict, songs_list = self.check_conflicts(songs)
                        
                        # Reproducir primera canción (en caso de conflicto, mostrar warning)
                        song_data = songs_list[0]
                        song_file = os.path.join(self.songs_dir, song_data.get('archivo'))
                        
                        if os.path.exists(song_file):
                            logger.info(f"Reproduciendo: {song_data.get('nombre')}")
                            self.play_song(song_file)
                            
                            # Actualizar estado - guardar el archivo sin la extensión .mp3
                            archivo_sin_ext = song_data.get('archivo', '').replace('.mp3', '').replace('.MP3', '')
                            self.config['estado_reproduccion'] = {
                                'reproduciendo': True,
                                'cancion_actual': archivo_sin_ext,
                                'fecha_ultima_actualizacion': datetime.now().isoformat()
                            }
                            self.save_config()
                    
                    last_check_minute = current_minute
                
                # Esperar 10 segundos antes de verificar de nuevo
                time.sleep(10)
            
            except Exception as e:
                logger.error(f"Error en loop principal: {e}")
                time.sleep(10)
    
    def stop(self):
        """Detiene el scheduler"""
        self.stop_current_song()
        self.running = False
        logger.info("MusicBell detenido")

if __name__ == '__main__':
    scheduler = MusicScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        scheduler.stop()
