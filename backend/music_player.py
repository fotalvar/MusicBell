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
        self.current_player_process = None  # Track del proceso actual
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
        """Reproduce una canción usando el reproductor del sistema"""
        if not os.path.exists(song_path):
            logger.error(f"Archivo no encontrado: {song_path}")
            return False
        
        # Detener canción anterior si está sonando
        self.stop_current_song()
        
        try:
            system = platform.system()
            
            if system == 'Darwin':  # macOS
                self.current_player_process = subprocess.Popen(['afplay', song_path])
            elif system == 'Windows':
                self.current_player_process = subprocess.Popen(['powershell', '-Command', f'(New-Object Media.SoundPlayer "{song_path}").PlaySync()'])
            elif system == 'Linux':
                self.current_player_process = subprocess.Popen(['paplay', song_path])
            
            logger.info(f"Reproduciendo: {song_path}")
            return True
        except Exception as e:
            logger.error(f"Error reproduciendo canción: {e}")
            return False
    
    def stop_current_song(self):
        """Detiene la canción que está sonando actualmente"""
        if self.current_player_process and self.current_player_process.poll() is None:
            try:
                # Intentar terminar el proceso de manera segura
                if platform.system() == 'Windows':
                    self.current_player_process.terminate()
                else:
                    os.kill(self.current_player_process.pid, signal.SIGTERM)
                    
                # Esperar a que se termine
                try:
                    self.current_player_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    # Si no se termina, matar forzadamente
                    if platform.system() == 'Windows':
                        self.current_player_process.kill()
                    else:
                        os.kill(self.current_player_process.pid, signal.SIGKILL)
                
                logger.info("Canción detenida")
                self.current_player_process = None
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
                            
                            # Actualizar estado
                            self.config['estado_reproduccion'] = {
                                'reproduciendo': True,
                                'cancion_actual': song_data.get('nombre'),
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
