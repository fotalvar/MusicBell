# Guía de Desarrollo

## Requisitos de Desarrollo

- Python 3.8+
- pip (gestor de paquetes)
- Git
- Navegador web moderno

## Configuración del Entorno

### 1. Clonar el repositorio

```bash
git clone <repositorio>
cd MusicBell
```

### 2. Crear entorno virtual

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 4. Ejecutar en modo desarrollo

```bash
export FLASK_DEBUG=True
python backend/app.py
```

---

## Arquitectura del Proyecto

```
MusicBell/
├── backend/
│   ├── app.py              # Servidor Flask + rutas API
│   ├── music_player.py     # Motor de reproducción
│   ├── utils.py            # Funciones auxiliares
│   ├── cli.py              # CLI para administración
│   ├── requirements.txt     # Dependencias Python
│   └── venv/               # Entorno virtual
│
├── frontend/
│   ├── index.html          # Estructura HTML
│   ├── style.css           # Estilos CSS
│   └── script.js           # Lógica JavaScript
│
├── config/
│   └── canciones.json      # Configuración persistente
│
├── canciones/              # Archivos MP3
├── logs/                   # Logs de la aplicación
└── docs/                   # Documentación
```

---

## Componentes Principales

### Backend

#### `music_player.py`

- **MusicScheduler**: Clase principal para gestionar reproducción
  - `load_config()`: Carga configuración desde JSON
  - `get_scheduled_songs_now()`: Obtiene canciones programadas
  - `play_song()`: Reproduce un archivo MP3
  - `stop_current_song()`: Detiene la reproducción
  - `run()`: Loop principal que monitorea el reloj

#### `app.py`

Rutas API disponibles:

- `GET /api/canciones` - Listar canciones programadas
- `POST /api/canciones` - Crear nueva canción
- `PUT /api/canciones/<id>` - Actualizar canción
- `DELETE /api/canciones/<id>` - Eliminar canción
- `GET /api/estado` - Estado actual del sistema
- `POST /api/reproducir/<archivo>` - Reproducir manualmente
- `POST /api/detener` - Detener reproducción
- `POST /api/cargar-archivo` - Subir MP3
- `GET /api/archivos` - Listar archivos disponibles

### Frontend

#### `script.js`

Funciones principales:

- `reproducirCancion()` - Envía orden al backend
- `detenerCancion()` - Detiene reproducción
- `cargarCanciones()` - Carga lista de canciones
- `cargarEstado()` - Consulta estado actual

---

## Flujo de Reproducción

```
Usuario (Frontend)
    ↓
Click "Reproducir" o esperar hora programada
    ↓
POST /api/reproducir/cancion.mp3
    ↓
Backend (music_player.py)
    ↓
play_song() con VLC
    ↓
Altavoces (macOS/Linux)
```

---

## Depuración

### Ver logs en tiempo real

```bash
tail -f logs/musicbell.log
```

### Probar CLI

```bash
cd backend
python cli.py listar
python cli.py reproducir nombre_archivo.mp3
python cli.py detener
```

### Probar API manualmente

```bash
# Listar canciones
curl http://localhost:5000/api/canciones

# Estado
curl http://localhost:5000/api/estado

# Reproducir
curl -X POST http://localhost:5000/api/reproducir/cancion.mp3

# Detener
curl -X POST http://localhost:5000/api/detener
```

---

## Decisiones de Diseño

1. **Backend Python**: Portabilidad y facilidad
2. **Frontend web**: Accesible desde cualquier dispositivo
3. **JSON para datos**: Simple, sin base de datos
4. **VLC para audio**: Motor robusto y multiplataforma
5. **Threads para reproducción**: No bloquea interfaz

---

## Mejoras Futuras

- [ ] Autenticación de usuario
- [ ] HTTPS para conexiones seguras
- [ ] Soporte para FLAC/WAV
- [ ] Control de volumen
- [ ] Estadísticas de reproducción
- [ ] API REST mejorada
- [ ] App móvil
- [ ] Sincronización con NTP

---

## Comandos Útiles

```bash
# Iniciar en modo desarrollo
FLASK_DEBUG=True python backend/app.py

# Instalar nueva dependencia
pip install paquete_nuevo
pip freeze > backend/requirements.txt

# Ejecutar tests (futuro)
python -m pytest

# Formatear código
black backend/
flake8 backend/
```

---

## Convenciones de Código

- Nombres en snake_case (Python)
- Nombres en camelCase (JavaScript)
- Docstrings en funciones Python
- Comentarios en español
- PEP 8 para Python
- 2 espacios de indentación en JavaScript

---

## Git Workflow

```bash
# Crear rama
git checkout -b feature/nueva-caracteristica

# Hacer cambios
git add .
git commit -m "Descripción del cambio"

# Subir cambios
git push origin feature/nueva-caracteristica

# Hacer merge en main
# (a través de pull request)
```

---

Para más información, consulta la documentación específica en la carpeta `docs/`.
