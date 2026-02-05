# Instalación de Pygame para reproducción de audio en Windows

## Problema resuelto

Se ha actualizado la aplicación para usar **pygame** en lugar de `winsound`, porque `winsound` no soporta archivos MP3.

## Instrucciones de instalación

### En Windows (PowerShell o CMD):

```bash
# Navega a la carpeta del proyecto
cd C:\ruta\a\MusicBell

# Instala pygame
python -m pip install pygame==2.5.2

# O si tienes Python 3 explícitamente:
python3 -m pip install pygame==2.5.2
```

### Alternativa: Actualizar requirements.txt

```bash
# Instala todas las dependencias actualizadas
python -m pip install -r backend/requirements.txt
```

## Verificar que pygame está instalado

```bash
python -c "import pygame; print('Pygame versión:', pygame.__version__)"
```

## Cómo funciona ahora

1. El frontend envía la orden de reproducción al backend
2. El backend usa **pygame.mixer** para reproducir el archivo MP3
3. El audio sale por los altavoces del ordenador donde está el servidor backend en Windows

## Ventajas de pygame

✅ Soporta MP3, OGG, FLAC y otros formatos  
✅ Reproducción sin bloqueos (asincrónica)  
✅ Funciona en Windows, macOS y Linux  
✅ Mejor control sobre la reproducción  
✅ Permite pausar, reanudar y detener

## Si aún no hay sonido

1. Verifica que el volumen de Windows no está en silencio
2. Revisa los logs en `logs/musicbell.log`
3. Comprueba que los archivos MP3 existen en la carpeta `canciones/`
4. Intenta reproducir un MP3 manualmente desde Windows para verificar que funciona

## Logs disponibles

Después de instalar pygame y ejecutar la aplicación, podrás ver en `logs/musicbell.log`:

```
2026-02-05 16:05:00 - INFO - Pygame mixer inicializado
2026-02-05 16:05:01 - INFO - Reproduciendo (pygame): /ruta/cancion.mp3 (duración: 234.50s)
```
