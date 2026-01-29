# MusicBell - Sistema de Reproducción Automática de Música

Una aplicación multiplataforma moderna para gestionar la reproducción automática de canciones en escuelas, espacios públicos y eventos. Construida con Python (Flask) en el backend y HTML5/CSS3/JavaScript vanilla en el frontend.

## 🎯 Características Principales

- ✅ **Multiplataforma**: Windows, macOS y Linux
- ✅ **Interfaz Web Responsiva**: Control total desde el navegador
- ✅ **Programación Flexible**: Por hora, fecha específica o días de la semana
- ✅ **Detección de Conflictos**: Identifica solapamientos considerando duración
- ✅ **Reproducción Rápida**: Reproducir cualquier canción al instante
- ✅ **API REST**: Integración fácil con otros sistemas
- ✅ **Persistencia**: Configuración guardada automáticamente
- ✅ **Recuperación Automática**: Se reinicia tras interrupciones
- ✅ **Código Optimizado**: Clean code, sin duplicación, rendimiento mejorado

## 📁 Estructura del Proyecto

```
MusicBell/
├── backend/
│   ├── app.py              # API REST (Flask) - Rutas principales
│   ├── music_player.py     # Motor de reproducción - Scheduler
│   ├── utils.py            # Funciones auxiliares compartidas
│   ├── cli.py              # Interfaz de línea de comandos
│   ├── requirements.txt     # Dependencias Python
│   └── venv/               # Entorno virtual (si aplica)
│
├── frontend/
│   ├── index.html          # Interfaz web responsiva
│   ├── script.js           # Lógica JavaScript optimizado
│   └── style.css           # Estilos CSS (limpio y consolidado)
│
├── config/
│   └── canciones.json      # Configuración de canciones (generado)
│
├── canciones/              # Carpeta para archivos MP3
│
├── logs/
│   └── musicbell.log       # Logs de ejecución
│
├── README.md               # Este archivo
├── GUIA_RAPIDA.md          # Guía de inicio rápido
├── INDEX.md                # Índice de documentación
├── FAQ.md                  # Preguntas frecuentes
├── ESTRUCTURA_DATOS.md     # Formato de configuración
├── DESARROLLO.md           # Guía para desarrolladores
├── OPTIMIZATION_SUMMARY.md # Resumen de optimizaciones
├── INSTALACION_WINDOWS.md  # Guía de instalación Windows
└── PALETA_COLORES.md       # Paleta de colores UI
```

## 🚀 Inicio Rápido (60 segundos)

### Requisitos Previos

- **Python 3.8+**
- **pip** (gestor de paquetes)
- **Navegador moderno** (Chrome, Firefox, Safari, Edge)

### Instalación y Ejecución

**macOS/Linux:**

```bash
# 1. Instalar dependencias
pip install -r backend/requirements.txt

# 2. Crear carpeta de canciones si no existe
mkdir -p canciones

# 3. Ejecutar la aplicación
python backend/app.py
```

**Windows:**

```powershell
# Opción 1: Doble clic en los archivos (Más fácil)
1. Ejecuta: install_requirements.bat
2. Luego: run.bat

# Opción 2: Línea de comandos
pip install -r backend\requirements.txt
mkdir canciones
python backend\app.py
```

👉 **[Guía completa de instalación Windows →](INSTALACION_WINDOWS_NUEVA.md)**

### Acceso a la Interfaz

- Abrir navegador: **http://localhost:5000**
- La aplicación estará lista inmediatamente

## 📋 Funcionalidades Principales

### 1. **Playlist** (Tab 1)

- Vista de todas las canciones programadas
- Editar fecha y hora en tiempo real
- Ordenadas automáticamente por fecha/hora
- Eliminar canciones fácilmente

### 2. **Reproducción Rápida** (Tab 2)

- Reproducir cualquier MP3 de la carpeta `canciones/`
- Instantáneamente sin programación
- Ideal para pruebas y reproducciones manuales

### 3. **Archivado** (Tab 3)

- Canciones pasadas se archivan automáticamente
- Vista histórica completa
- Poder recuperar si es necesario

### 4. **Conflictos** (Tab 4)

- Detecta múltiples canciones a la misma hora
- Considera duración del MP3
- Útil para evitar traslapes

### 5. **Estado Rápido**

- Barra de estado permanente (fuera de tabs)
- Botón STOP para detener reproducción actual
- Información en tiempo real

## 🔧 Uso Detallado

### Agregar una Canción Programada

1. Click en **"Añadir Canción"**
2. Nombre descriptivo
3. Seleccionar archivo MP3
4. Elegir tipo de planificación:
   - **Hora diaria**: Repite todos los días a la misma hora
   - **Fecha específica**: Solo una vez en esa fecha
   - **Días de la semana**: Lunes a domingo personalizados
5. Click en **"Agregar Canción"**

### Programación Rápida

1. Click en **"Programación Rápida"**
2. Seleccionar rango de fechas
3. Elegir hora de reproducción
4. Activar "Incluir fines de semana" si es necesario
5. Preview automático de fechas
6. Click en **"Generar Programación"**

### Reproducción Manual

1. Ir a tab **"Reproducción"**
2. Seleccionar canción de la lista
3. Click en **"Reproducir"**
4. Se reproduce inmediatamente

## 📊 Estructura de Datos

### Archivo `config/canciones.json`

```json
{
  "canciones": [
    {
      "id": 1,
      "nombre": "Himno Nacional",
      "archivo": "himno.mp3",
      "tipo_planificacion": "hora",
      "hora": "08:00",
      "duracion": "03:45",
      "habilitada": true,
      "archivado": false
    }
  ],
  "estado_reproduccion": {
    "reproduciendo": false,
    "cancion_actual": null,
    "fecha_ultima_actualizacion": "2026-01-29T10:30:00"
  }
}
```

## 🔌 API REST

Documentación completa en [DESARROLLO.md](DESARROLLO.md)

### Endpoints Principales

| Método   | Endpoint                    | Descripción                 |
| -------- | --------------------------- | --------------------------- |
| `GET`    | `/api/canciones`            | Obtener todas las canciones |
| `POST`   | `/api/canciones`            | Crear nueva canción         |
| `PUT`    | `/api/canciones/{id}`       | Actualizar canción          |
| `DELETE` | `/api/canciones/{id}`       | Eliminar canción            |
| `GET`    | `/api/archivos`             | Listar MP3 disponibles      |
| `POST`   | `/api/reproducir/{archivo}` | Reproducir archivo          |
| `POST`   | `/api/detener`              | Detener reproducción        |
| `GET`    | `/api/detectar-conflictos`  | Verificar solapamientos     |

## 🎨 Optimizaciones Realizadas

### Frontend (JavaScript)

- **-37% líneas de código** - Eliminación de duplicación
- **Caching de archivos** (30s TTL) - Menos llamadas API
- **Debounce en funciones** - Mejor rendimiento
- **Polling optimizado** - 10s vs 5s anteriores
- **DOM cacheado** - Acceso más rápido

### Frontend (CSS)

- **-48% líneas de código** - Consolidación de estilos
- **Variables CSS centralizadas** - Mantenimiento más fácil
- **Sin especificidad conflictiva** - CSS más limpio

### Backend (Python)

- **Modularización** - `utils.py` para funciones compartidas
- **Documentación mejorada** - Docstrings completos
- **Gestión de importaciones** - Sin dependencias innecesarias

Ver [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md) para detalles técnicos.

## ❓ Preguntas Frecuentes

**P: ¿Qué formatos de audio soporta?**
R: MP3 (.mp3) - Extensión requerida. Ver [FAQ.md](FAQ.md) para más detalles.

**P: ¿Puedo usar en producción?**
R: Sí, está completamente funcional. Ver [DESARROLLO.md](DESARROLLO.md) para consideraciones.

**P: ¿Funciona sin conexión a internet?**
R: Sí, es local. Solo necesita navegador. Ver [FAQ.md](FAQ.md).

**P: ¿Cómo cambiar el puerto?**
R: Modificar en `app.py` la línea `app.run(host='0.0.0.0', port=5000)`

Más preguntas en [FAQ.md](FAQ.md).

## 🛠️ Desarrollo

Para desarrolladores, ver:

- [DESARROLLO.md](DESARROLLO.md) - Arquitectura y guía de desarrollo
- [ESTRUCTURA_DATOS.md](ESTRUCTURA_DATOS.md) - Formato de configuración
- [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md) - Detalles de optimizaciones

## 📝 Documentación

| Documento                                              | Propósito                 |
| ------------------------------------------------------ | ------------------------- |
| **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)**                   | Inicio en 60 segundos     |
| **[INDEX.md](INDEX.md)**                               | Índice completo de docs   |
| **[FAQ.md](FAQ.md)**                                   | Preguntas frecuentes      |
| **[INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md)**   | Instalación Windows       |
| **[ESTRUCTURA_DATOS.md](ESTRUCTURA_DATOS.md)**         | Formato JSON              |
| **[DESARROLLO.md](DESARROLLO.md)**                     | Arquitectura técnica      |
| **[OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)** | Optimizaciones realizadas |
| **[PALETA_COLORES.md](PALETA_COLORES.md)**             | Colores de UI             |

## 🔒 Consideraciones de Seguridad

- La aplicación está diseñada para redes locales/privadas
- No exponer a internet sin autenticación adicional
- Los archivos MP3 deben copiarse manualmente a `canciones/`
- La configuración se guarda localmente en JSON

## 📦 Dependencias

### Backend

```
Flask==2.3.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
mutagen==1.46.0
```

### Frontend

- Vanilla JavaScript (sin frameworks)
- CSS3 (sin preprocesadores)
- HTML5 semántico

## 🚀 Mejoras Futuras Sugeridas

1. **Base de datos**: Migrar de JSON a SQLite/PostgreSQL
2. **Autenticación**: Agregar login de usuarios
3. **Service Worker**: Soporte offline con PWA
4. **Testing**: Tests unitarios e integración
5. **Logging avanzado**: Análisis detallado de reproducción
6. **Múltiples dispositivos**: Sincronización entre clientes

## 📄 Licencia

Proyecto de código abierto. Libre para usar, modificar y distribuir.

## 👨‍💻 Contacto y Soporte

Para reportar bugs o sugerencias, revisar la sección de [FAQ.md](FAQ.md) primero.

---

**Última actualización:** 29 de enero de 2026  
**Versión:** 2.0 (Optimizada)  
**Estado:** ✅ Completamente funcional y optimizado

```bash
# Navegar a la carpeta del proyecto
cd MusicBell
```

### 2. Instalar dependencias Python

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Añadir canciones

1. Coloca archivos MP3 en la carpeta `canciones/`
2. Asegúrate de que tengan extensión `.mp3`

## Uso

### Iniciar en macOS/Linux

```bash
# Desde la raíz del proyecto
cd backend
python app.py
```

Luego abre tu navegador en: `http://localhost:5000`

### Iniciar en Windows

```bash
cd backend
python app.py
```

O haz doble clic en `start_windows.bat` (próximamente disponible)

## Uso de la Aplicación

### 1. Interfaz Web

- Accede a `http://localhost:5000` desde cualquier dispositivo en la red
- Verás 4 secciones principales:

#### Estado Actual

- Muestra si se está reproduciendo alguna canción
- Canción actualmente en reprodución
- Última actualización

#### Añadir Nueva Canción

1. Ingresa un nombre descriptivo
2. Selecciona el archivo MP3
3. Elige el tipo de planificación:
   - **Hora diaria**: Suena a la misma hora todos los días
   - **Fecha específica**: Suena una sola vez en esa fecha y hora
   - **Días de la semana**: Suena en días específicos a una hora fija
4. Establece la hora de reproducción
5. Haz clic en "Agregar Canción"

#### Canciones Programadas

- Lista todas las canciones guardadas
- Muestra detalles de cada canción
- Permite editar o eliminar canciones
- Indica si está habilitada o deshabilitada

#### Verificar Conflictos

- Detecta si hay múltiples canciones programadas para el mismo momento
- Muestra agrupadas por hora
- Útil para resolver solapamientos

## Configuración Avanzada

### Archivo de Configuración

El archivo `config/canciones.json` contiene:

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
      "nombre": "Recreo Viernes",
      "archivo": "musica_recreo.mp3",
      "tipo_planificacion": "dia_semana",
      "dias": ["viernes"],
      "hora": "12:00",
      "habilitada": true
    }
  ],
  "estado_reproduccion": {
    "reproduciendo": false,
    "cancion_actual": null,
    "fecha_ultima_actualizacion": "2026-01-29T12:30:45"
  }
}
```

### Log de Actividad

Los logs se guardan en `logs/musicbell.log` con toda la actividad:

- Canciones reproducidas
- Errores
- Conflictos detectados

## Comportamiento Tras Reinicios

Si la computadora se apaga o reinicia:

1. MusicBell carga automáticamente la configuración guardada
2. Recupera el último estado conocido
3. Continúa con la programación normal
4. Los archivos de log se conservan para auditoría

## Resolución de Problemas

### Los archivos MP3 no se muestran

- Asegúrate de que están en la carpeta `canciones/`
- Verifica que la extensión sea `.mp3` (minúscula)
- Reinicia la aplicación

### No se reproduce sonido

**Windows**: Asegúrate de que `winsound` esté disponible
**macOS**: Verifica permisos de audio, ejecuta: `sudo chmod +x backend/music_player.py`
**Linux**: Instala ffplay: `sudo apt-get install ffmpeg`

### La aplicación se detiene

- Revisa `logs/musicbell.log` para errores
- Asegúrate de que Python tiene permisos de ejecución

## Cambios Pendientes/Mejoras

- [ ] Interfaz de edición modal mejorada
- [ ] Soporte para múltiples volúmenes
- [ ] Previsualización de audio
- [ ] Exportar/importar configuración
- [ ] Panel de estadísticas

## Soporte Técnico

Para reportar problemas:

1. Revisa los logs en `logs/musicbell.log`
2. Verifica que tengas Python 3.8+ instalado
3. Asegúrate de que los archivos MP3 sean válidos

## Licencia

Este proyecto es de uso libre y abierto.

---

**MusicBell © 2026** - Hecho para escuelas y espacios públicos 🎵
