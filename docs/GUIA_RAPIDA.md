# Guía Rápida - MusicBell

## ¿Qué es MusicBell?

Sistema automático para reproducir música en escuelas, oficinas y espacios públicos.

**Casos de uso:**

- Himno al inicio del día
- Señales de recreo
- Eventos especiales programados
- Música ambiental en horarios específicos

## Inicio Rápido (60 segundos)

```bash
cd MusicBell
bash start.sh
```

Luego abre: **http://localhost:5000**

---

## Pasos Básicos

### 1️⃣ Agrega archivos MP3

Copia tus canciones a `canciones/`

### 2️⃣ Crea una programación

- **Nombre**: Descripción de la canción
- **Archivo**: Selecciona el MP3
- **Tipo**: Hora diaria, fecha específica, o días de la semana
- **Hora**: A qué hora debe sonar
- **Habilitar**: Marca para activar

### 3️⃣ Listo

La canción sonará automáticamente a la hora programada

---

## Ejemplos Prácticos

### Himno diario a las 8:00 AM

- Nombre: `Himno`
- Archivo: `himno.mp3`
- Tipo: `Hora diaria`
- Hora: `08:00`

### Música de recreo todos los viernes a las 12:00

- Nombre: `Recreo Viernes`
- Archivo: `musica_recreo.mp3`
- Tipo: `Días de la semana`
- Días: `Viernes`
- Hora: `12:00`

### Evento especial - 14 de febrero a las 15:30

- Nombre: `Concierto`
- Archivo: `concierto.mp3`
- Tipo: `Fecha específica`
- Fecha: `2026-02-14`
- Hora: `15:30`

---

## Reproducción Manual

En la pestaña **Reproducción**, puedes reproducir cualquier canción al instante haciendo clic en el botón "▶ Reproducir".

---

## Solución Rápida de Problemas

| Problema                  | Solución                                           |
| ------------------------- | -------------------------------------------------- |
| No se escucha nada        | Revisa `logs/musicbell.log`                        |
| La app se cerró           | Reinicia desde terminal                            |
| No aparecen mis canciones | Comprueba que están en `canciones/` en formato MP3 |
| Puerto 5000 en uso        | Cambia el puerto en `backend/app.py`               |

---

## Próximos Pasos

- Lee [INSTALACION.md](INSTALARzada
- Consulta [FAQ.md](FAQ.md) para preguntas frecuentes
- Ver [ESTRUCTURA_DATOS.md](ESTRUCTURA_DATOS.md) para entender los datos

---

¡Listo! Tu sistema está configurado 🎵
