# Estructura de Datos del Proyecto MusicBell

## Formato JSON de Canciones

### Ejemplo completo de `config/canciones.json`

```json
{
  "canciones": [
    {
      "id": 1,
      "nombre": "Himno Nacional",
      "archivo": "himno.mp3",
      "tipo_planificacion": "hora",
      "hora": "08:00",
      "habilitada": true
    },
    {
      "id": 2,
      "nombre": "Desayuno Lunes",
      "archivo": "desayuno.mp3",
      "tipo_planificacion": "dia_semana",
      "dias": ["lunes", "miércoles", "viernes"],
      "hora": "07:45",
      "habilitada": true
    },
    {
      "id": 3,
      "nombre": "Concierto 15 de febrero",
      "archivo": "concierto.mp3",
      "tipo_planificacion": "fecha",
      "fecha": "2026-02-15",
      "hora": "18:00",
      "habilitada": false
    }
  ],
  "estado_reproduccion": {
    "reproduciendo": false,
    "cancion_actual": null,
    "fecha_ultima_actualizacion": "2026-01-29T14:30:00"
  }
}
```

## Tipos de Planificación

### 1. Hora Diaria (`tipo_planificacion: "hora"`)
La canción suena todos los días a la misma hora.

```json
{
  "id": 1,
  "nombre": "Himno Mañana",
  "archivo": "himno.mp3",
  "tipo_planificacion": "hora",
  "hora": "08:00",
  "habilitada": true
}
```

### 2. Fecha Específica (`tipo_planificacion: "fecha"`)
La canción suena una sola vez en esa fecha.

```json
{
  "id": 2,
  "nombre": "Evento Especial",
  "archivo": "evento.mp3",
  "tipo_planificacion": "fecha",
  "fecha": "2026-03-21",
  "hora": "15:30",
  "habilitada": true
}
```

### 3. Días de la Semana (`tipo_planificacion: "dia_semana"`)
La canción suena en días específicos cada semana.

```json
{
  "id": 3,
  "nombre": "Viernes Cine",
  "archivo": "musica_cine.mp3",
  "tipo_planificacion": "dia_semana",
  "dias": ["viernes"],
  "hora": "16:00",
  "habilitada": true
}
```

## Campos

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `id` | integer | Sí | Identificador único de la canción |
| `nombre` | string | Sí | Nombre descriptivo de la canción |
| `archivo` | string | Sí | Nombre del archivo MP3 |
| `tipo_planificacion` | string | Sí | `"hora"`, `"fecha"` o `"dia_semana"` |
| `hora` | string (HH:MM) | Sí | Hora de reproducción |
| `fecha` | string (YYYY-MM-DD) | Condicional | Requerido si `tipo_planificacion == "fecha"` |
| `dias` | array | Condicional | Requerido si `tipo_planificacion == "dia_semana"` |
| `habilitada` | boolean | No (default: true) | Si la canción está activa |

## Valores de Días

```
"lunes"
"martes"
"miércoles"
"jueves"
"viernes"
"sábado"
"domingo"
```

## Estado de Reproducción

```json
{
  "reproduciendo": false,
  "cancion_actual": null,
  "fecha_ultima_actualizacion": "2026-01-29T14:30:00"
}
```

- `reproduciendo`: `true` si está sonando una canción
- `cancion_actual`: Nombre de la canción en reproducción o `null`
- `fecha_ultima_actualizacion`: ISO 8601 timestamp de la última actualización
