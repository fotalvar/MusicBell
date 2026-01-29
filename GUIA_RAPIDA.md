# Guía Rápida - MusicBell

## ¿Qué es MusicBell?

MusicBell es un sistema automático para reproducir música en escuelas. Perfecto para:
- Himno al inicio del día
- Señales de recreo
- Eventos especiales programados
- Música ambiental en horarios específicos

## Inicio Rápido (60 segundos)

### En macOS o Linux:
```bash
cd MusicBell
bash start.sh
```

### En Windows:
```bash
cd MusicBell
start_windows.bat
```

Luego abre tu navegador: **http://localhost:5000**

## Pasos Básicos

### 1️⃣ Añade archivos MP3
- Copia tus canciones a la carpeta `canciones/`
- Los archivos deben ser `.mp3`

### 2️⃣ Crea una programación
- Nombre: Dale un nombre descriptivo
- Archivo: Elige el MP3
- Tipo: Elige cómo programar (diaria, fecha o días específicos)
- Hora: A qué hora debe sonar
- Agregar

### 3️⃣ Listo
- La canción sonará automáticamente a la hora programada
- Si la computadora se apaga y enciende, continuará funcionando

## Ejemplos

**Himno a las 8:00 AM todos los días:**
- Nombre: Himno
- Archivo: himno.mp3
- Tipo: Hora diaria
- Hora: 08:00

**Música de recreo cada viernes a las 12:00:**
- Nombre: Recreo Viernes
- Archivo: musica_recreo.mp3
- Tipo: Días de la semana
- Días: Viernes
- Hora: 12:00

**Evento único el 14 de febrero:**
- Nombre: Concierto
- Archivo: concierto.mp3
- Tipo: Fecha específica
- Fecha: 2026-02-14
- Hora: 15:30

## Cambios para Windows (en el futuro)

MusicBell será un servicio de Windows que:
- Se inicia automáticamente al encender
- Se ejecuta en segundo plano
- Se controla desde la interfaz web
- Se puede hacer "Iniciar sesión" opcional

## Ayuda

- **¿No se escucha nada?** Verifica que los archivos MP3 sean válidos
- **¿Se apagó la app?** Reinicia desde la terminal
- **¿Dudas?** Revisa `README.md` para más detalles

---

¡Listo! Tu escuela ya tiene música automática 🎵
