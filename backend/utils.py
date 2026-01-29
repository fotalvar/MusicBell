#!/usr/bin/env python3
"""
Utilidades compartidas para MusicBell
Contiene funciones comunes para parsing y manipulación de datos
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from mutagen.mp3 import MP3
except ImportError:
    MP3 = None


def obtener_duracion_mp3(archivo_path):
    """
    Obtiene la duración de un archivo MP3 en formato MM:SS
    
    Args:
        archivo_path (str): Ruta al archivo MP3
        
    Returns:
        str: Duración en formato MM:SS o None si no se puede obtener
    """
    try:
        if MP3 is None:
            return None
        
        audio = MP3(archivo_path)
        duracion_segundos = int(audio.info.length)
        minutos = duracion_segundos // 60
        segundos = duracion_segundos % 60
        return f"{minutos:02d}:{segundos:02d}"
    except Exception as e:
        logger.warning(f"No se pudo obtener duración de {archivo_path}: {e}")
        return None


def parsear_duracion_a_segundos(duracion_str):
    """
    Convierte duración MM:SS a segundos
    
    Args:
        duracion_str (str): Duración en formato MM:SS
        
    Returns:
        int: Duración en segundos (180s por defecto si hay error)
    """
    try:
        if not duracion_str:
            return 0
        partes = duracion_str.split(':')
        minutos = int(partes[0])
        segundos = int(partes[1])
        return minutos * 60 + segundos
    except Exception:
        return 180  # Asumir 3 minutos por defecto


def parsear_hora_a_segundos(hora_str, fecha_str=None):
    """
    Convierte hora HH:MM a segundos desde medianoche
    
    Args:
        hora_str (str): Hora en formato HH:MM
        fecha_str (str): Fecha en formato YYYY-MM-DD (no utilizado actualmente)
        
    Returns:
        int: Segundos desde medianoche (0 si hay error)
    """
    try:
        if not hora_str:
            return 0
        partes = hora_str.split(':')
        horas = int(partes[0])
        minutos = int(partes[1])
        return horas * 3600 + minutos * 60
    except Exception:
        return 0
