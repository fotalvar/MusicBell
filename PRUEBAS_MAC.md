# 🚀 Instrucciones de Prueba en macOS

## Inicio Rápido

```bash
# Navega a la carpeta del proyecto
cd /Users/federicootalvares/Desktop/MusicBell

# Ejecuta el script de inicio
bash start.sh
```

La aplicación se iniciará en el puerto 5000.

## Acceso a la Interfaz

Abre tu navegador y ve a: **http://localhost:5000**

## Pasos de Prueba Recomendados

### 1. Verificar que funciona

1. Abre http://localhost:5000
2. Deberías ver la interfaz con las secciones:
   - Estado Actual
   - Añadir Nueva Canción
   - Canciones Programadas (vacío al inicio)
   - Conflictos de Horario

### 2. Probar carga de archivos

1. Ve a la sección "Añadir Nueva Canción"
2. Haz clic en "Archivo MP3"
3. Deberías ver la carpeta `canciones/` vacía

### 3. Agregar archivos de prueba

Opción A: Copiar archivos existentes
```bash
# Buscar MP3 en tu Mac
find ~ -name "*.mp3" -type f | head -5

# Copiar a la carpeta de MusicBell
cp /ruta/a/cancion.mp3 /Users/federicootalvares/Desktop/MusicBell/canciones/
```

Opción B: Crear tonos de prueba (requiere ffmpeg)
```bash
# Instalar ffmpeg si no lo tienes
brew install ffmpeg

# Crear un tono de prueba (3 segundos)
ffmpeg -f lavfi -i sine=f=440:d=3 -q:a 9 -acodec libmp3lame \
  /Users/federicootalvares/Desktop/MusicBell/canciones/prueba.mp3
```

### 4. Crear una programación de prueba

1. Nombre: "Prueba"
2. Archivo: selecciona tu MP3
3. Tipo: "Hora diaria"
4. Hora: establécela 2 minutos en el futuro (ej: si son las 14:30, pon 14:32)
5. Haz clic en "Agregar Canción"

### 5. Observar reproducción

- Espera a que llegue la hora programada
- Deberías escuchar la canción
- El estado cambiarará a "Reproduciendo"

### 6. Probar detección de conflictos

1. Crea una segunda canción con la misma hora que la primera
2. Haz clic en "Verificar Conflictos"
3. Deberías ver que ambas canciones aparecen como conflicto

### 7. Probar persistencia

1. Cierra la ventana del navegador
2. Detén la app (Ctrl+C en terminal)
3. Vuelve a ejecutar `bash start.sh`
4. Abre http://localhost:5000
5. Las canciones que agregaste seguirán ahí

### 8. Editar y eliminar

1. En la tarjeta de una canción, haz clic en "Editar"
2. Cambia el nombre y confirma
3. Haz clic en "Eliminar" para remover una canción

## Prueba de Línea de Comandos

También puedes gestionar canciones desde terminal:

```bash
cd /Users/federicootalvares/Desktop/MusicBell/backend

# Listar todas las canciones
python3 cli.py listar

# Listar archivos disponibles
python3 cli.py archivos

# Agregar canción (hora diaria)
python3 cli.py agregar "Himno" "prueba.mp3" "hora" "08:00"

# Agregar canción (día de la semana)
python3 cli.py agregar "Viernes" "prueba.mp3" "dia_semana" "12:00" --dias viernes

# Agregar canción (fecha específica)
python3 cli.py agregar "Evento" "prueba.mp3" "fecha" "15:30" --fecha 2026-02-14

# Detectar conflictos
python3 cli.py conflictos

# Eliminar canción
python3 cli.py eliminar 1

# Ver estado
python3 cli.py estado
```

## Verificar Logs

```bash
# Ver los últimos logs
tail -f /Users/federicootalvares/Desktop/MusicBell/logs/musicbell.log

# O abrir el archivo completo
cat /Users/federicootalvares/Desktop/MusicBell/logs/musicbell.log
```

## Acceso desde Otro Dispositivo

1. Obtén la IP de tu Mac:
   ```bash
   ifconfig | grep "inet " | grep -v 127
   ```
   Verás algo como `192.168.1.100`

2. Desde otro dispositivo (teléfono, tablet, PC):
   Abre: `http://192.168.1.100:5000`

3. Deberías poder controlar MusicBell desde cualquier dispositivo en tu red

## Solución de Problemas Rápida

### Error: "Port 5000 in use"
```bash
# Matar el proceso que usa el puerto
lsof -ti:5000 | xargs kill -9

# O cambiar puerto en backend/app.py
# Busca: app.run(host='0.0.0.0', port=5000)
# Cambia a: app.run(host='0.0.0.0', port=8080)
```

### No funciona Flask-CORS
```bash
python3 -m pip install --upgrade Flask-CORS
```

### Permisos de ejecución
```bash
chmod +x /Users/federicootalvares/Desktop/MusicBell/start.sh
```

### Ver errores de Python
```bash
cd /Users/federicootalvares/Desktop/MusicBell/backend
python3 -m py_compile music_player.py app.py
```

## Cambios Recomendados para Windows

Cuando estés listo para Windows:

1. Prueba `start_windows.bat` en una máquina virtual con Windows
2. O proporciona los archivos a alguien con Windows para testing
3. Considera crear un instalador (NSIS)

## Próximos Pasos

- [ ] Crear archivos de audio de prueba
- [ ] Probar con múltiples dispositivos en la red
- [ ] Verificar comportamiento con reboots
- [ ] Optimizar interfaz según feedback
- [ ] Empaquetar para Windows
- [ ] Crear servicio de Windows automatizado

---

¡Listo! Ahora tienes un sistema completo de reproducción de música automática 🎵
