#!/usr/bin/env python3
"""
MusicBell - Reproductor de música automático para escuelas
Script principal que se ejecuta en segundo plano
"""

import json
import os
import time
import logging
import threading
from datetime import datetime
from pathlib import Path
import signal
import subprocess
from utils import parsear_hora_a_segundos

# Obtener la ruta del proyecto (padre del backend)
project_root = Path(__file__).parent.parent
logs_dir = project_root / 'logs'
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(logs_dir / 'musicbell.log'), encoding='utf-8'),
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
        self.current_player_process = None  # Reproductor VLC
        self.vlc_instance = None  # Instancia de VLC
        self.vlc_media_list = None  # Lista de media de VLC
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
        """Reproduce una canción usando VLC (compatible con macOS y Linux)"""
        if not os.path.exists(song_path):
            logger.error(f"Archivo no encontrado: {song_path}")
            return False
        
        # Detener canción anterior si está sonando
        self.stop_current_song()
        
        try:
            logger.info("=== INICIANDO REPRODUCCION ===")
            logger.info(f"Archivo: {song_path}")
            logger.info(f"Tamaño: {os.path.getsize(song_path)} bytes")
            logger.info(f"Existe: {os.path.exists(song_path)}")
            logger.info(f"Lectura: {os.access(song_path, os.R_OK)}")
            
            # Verificar que el archivo es válido
            if os.path.getsize(song_path) == 0:
                logger.error("El archivo está vacío")
                return False
            
            if os.path.getsize(song_path) < 5000:  # Menos de 5KB
                logger.error("El archivo es muy pequeño, probablemente corrupto")
                return False
            
            # Usar VLC para reproducir (compatible con macOS y Linux)
            try:
                import vlc
            except ImportError:
                logger.error("[ERROR] python-vlc NO DISPONIBLE. Instala: pip install python-vlc")
                return False
            
            logger.info("[OK] VLC importado correctamente")
            
            # Reproducir música usando VLC
            try:
                # Crear instancia de VLC
                instance = vlc.Instance()
                media = instance.media_new(song_path)
                player = instance.media_list_player_new()
                media_list = instance.media_list_new()
                media_list.add_media(media)
                player.set_media_list(media_list)
                
                # Reproducir
                player.play()
                
                # Guardar referencias
                self.current_player_process = player
                self.current_player = instance
                
                logger.info(f"[OK] REPRODUCCION INICIADA: {song_path}")
                return True
                
            except Exception as e:
                logger.error(f"[ERROR] Error usando VLC: {e}")
                import traceback
                logger.error(traceback.format_exc())
                return False
            
        except Exception as e:
            logger.error(f"[ERROR] ERROR CRÍTICO EN REPRODUCCION: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    
    def stop_current_song(self):
        """Detiene la cancion que esta sonando actualmente"""
        try:ón que está sonando actualmente"""
        try:
            logger.info("Deteniendo reproducción...")
            
            if self.current_player_process:
                try:
                    # Detener el reproductor VLC
                    self.current_player_process.stop()
                    logger.info("[OK] Música detenida")
                except Exception as e:
                    logger.warning(f"Error deteniendo música: {e}")
            
            self.current_player_process = None
            self.current_player = None
            
            logger.info("[OK] Reproducción detenida")
            return True
            
        except Exception as e:
            logger.error(f"Error deteniendo canció
            self.current_player = None
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
