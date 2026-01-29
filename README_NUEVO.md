# 🎵 MusicBell - Aplicación de Reproducción de Música para Escuelas

## ¿Qué es MusicBell?

MusicBell es una **aplicación de reproducción de música automática** diseñada específicamente para escuelas. Permite programar la reproducción de canciones en horarios específicos con detección automática de conflictos.

**Características:**
✅ Reproducción automática de canciones en horarios programados  
✅ Programación por hora diaria, fecha específica o días de la semana  
✅ Detección automática de conflictos (múltiples canciones al mismo tiempo)  
✅ Persistencia de datos (sobrevive reincios)  
✅ Interfaz web intuitiva con navegación por tabs  
✅ Carga automática de canciones disponibles  
✅ Generador automático de programación rápida  
✅ Compatible con Windows, macOS y Linux  

---

## 📋 Interfaz - Navegación por Tabs

La aplicación ahora utiliza un **sistema de tabs** para una mejor organización:

### 📊 Tab 1: Estado
Muestra el estado actual de la aplicación:
- Canción en reproducción ahora mismo
- Próximas canciones programadas
- Hora del servidor

### ➕ Tab 2: Agregar Canción
Formulario para agregar nuevas canciones manualmente:
- Nombre de la canción
- Seleccionar archivo MP3
- Tipo de planificación (hora diaria, fecha específica, días de la semana)
- Hora de reproducción
- Configuración específica según tipo

### ⚡ Tab 3: Programación Rápida
**Generador automático inteligente:**
1. Especificar rango de fechas
2. Seleccionar hora
3. Opción de incluir fines de semana
4. El sistema automáticamente:
   - Cuenta días dentro del rango
   - Muestra canciones disponibles
   - Calcula distribución automática
   - Recicla canciones si hay más días que canciones

**Ejemplo:**
- Rango: 5 días laborales
- Canciones disponibles: 3
- Resultado: Se programarán 5 canciones (reciclando la lista)

### 🎵 Tab 4: Mis Canciones
Lista completa de todas las canciones programadas:
- Ver detalles de cada canción
- Editar hora y fecha rápidamente
- Ver estado (habilitada/deshabilitada)
- Eliminar canciones

### ⚠️ Tab 5: Conflictos
Detector automático de conflictos:
- Muestra todas las canciones que suenan al mismo tiempo
- Fácil de identificar para resolver problemas
- Se actualiza automáticamente

---

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Instalación de Dependencias
```bash
# Ir a la carpeta del proyecto
cd /ruta/a/MusicBell

# Instalar dependencias
pip install -r requirements.txt
# O manualmente:
pip install flask==2.3.0 flask-cors==4.0.0 python-dotenv==1.0.0
```

### Paso 2: Agregar Canciones MP3
1. Copiar archivos MP3 a la carpeta `canciones/`
2. Los archivos deben tener extensión `.mp3`

### Paso 3: Iniciar la Aplicación

**En macOS/Linux:**
```bash
bash start.sh
```

**En Windows:**
```bash
start.bat
```

O manualmente:
```bash
cd backend
python app.py
```

### Paso 4: Acceder a la Interfaz
Abrir navegador y ir a: **http://localhost:5000**

---

## 📁 Estructura del Proyecto

```
MusicBell/
│
├── frontend/                    # Interfaz web
│   ├── index.html             # HTML principal (5 tabs)
│   ├── style.css              # Estilos y animaciones
│   └── script.js              # Lógica JavaScript
│
├── backend/                    # Servidor y programador
│   ├── app.py                 # Servidor Flask
│   ├── music_player.py        # Motor de reproducción
│   └── cli.py                 # Herramienta CLI
│
├── config/                     # Configuración
│   └── canciones.json         # Base de datos de canciones
│
├── canciones/                  # Carpeta de archivos MP3
│   └── (tus canciones.mp3)
│
├── logs/                       # Archivos de log
│   └── musicbell.log
│
├── start.sh                    # Script de inicio (macOS/Linux)
├── start_windows.bat           # Script de inicio (Windows)
│
└── Documentación/
    ├── README.md              # Este archivo
    ├── GUIA_RAPIDA.md
    ├── INSTALACION_WINDOWS.md
    ├── ESTRUCTURA_DATOS.md
    └── (más archivos de documentación)
```

---

## 🎯 Casos de Uso Típicos

### Caso 1: Himno Nacional Diariamente
1. Agregar canción "Himno Nacional"
2. Tipo: Hora diaria
3. Hora: 08:00
4. Resultado: Suena todos los días a las 8 AM

### Caso 2: Concierto de Fin de Semana
1. Agregar canción "Clásicos del Concierto"
2. Tipo: Fecha específica
3. Fecha: 2025-02-15
4. Hora: 14:30
5. Resultado: Suena una sola vez el 15 de febrero a las 14:30

### Caso 3: Descansos Lunes-Viernes
1. Agregar canción "Música de Descanso"
2. Tipo: Días de la semana
3. Seleccionar: Lunes, Miércoles, Viernes
4. Hora: 11:00
5. Resultado: Suena 3 veces por semana

### Caso 4: Programación Automática Rápida
1. Ir a tab "Programación Rápida"
2. Seleccionar: 1-31 de enero 2025
3. Hora: 09:00
4. No incluir fines de semana
5. Presionar "Programar Canciones"
6. Resultado: Se generan automáticamente ~21 canciones (días laborales)

---

## 🛠️ API REST

La aplicación incluye una REST API para integración:

### Endpoints

**GET /api/canciones**
- Obtener lista de todas las canciones
- Respuesta: `[{id, nombre, archivo, tipo_planificacion, hora, ...}, ...]`

**POST /api/canciones**
- Agregar nueva canción
- Body: `{nombre, archivo, tipo_planificacion, hora, ...}`

**PUT /api/canciones/{id}**
- Actualizar canción
- Body: `{campo: nuevo_valor}`

**DELETE /api/canciones/{id}**
- Eliminar canción

**GET /api/estado**
- Obtener estado actual
- Respuesta: `{ahora_sonando, proximas_canciones, ...}`

**GET /api/archivos**
- Listar archivos MP3 disponibles
- Respuesta: `[{nombre, tamaño}, ...]`

**GET /api/detectar-conflictos**
- Detectar horarios en conflicto
- Respuesta: `[{hora, canciones: [...]}, ...]`

---

## 📊 Formato de Datos

### Estructura de Canción (JSON)
```json
{
  "id": 1,
  "nombre": "Himno Nacional",
  "archivo": "himno.mp3",
  "tipo_planificacion": "hora",
  "hora": "08:00",
  "fecha": null,
  "dias": null,
  "habilitada": true
}
```

### Tipos de Planificación
- **hora**: Reproduce a la misma hora todos los días
- **fecha**: Reproduce una sola vez en fecha específica
- **dia_semana**: Reproduce en días específicos de la semana

---

## ⌨️ Características Técnicas

### Frontend
- HTML5 semántico
- CSS3 con variables y animaciones
- JavaScript vanilla (sin dependencias externas)
- Responsive design (mobile-first)
- Fetch API para comunicación

### Backend
- Python 3.8+
- Flask 2.3.0 para servidor web
- JSON para persistencia
- Threading para scheduler background
- Cross-platform audio playback

### Persistencia
- Los datos se guardan automáticamente en `config/canciones.json`
- Sobreviven reinicio de la aplicación
- Copias de seguridad automáticas (opcional)

---

## 🐛 Troubleshooting

### "Puerto 5000 ya está en uso"
```bash
# Encontrar proceso usando puerto 5000
lsof -i :5000

# Matar el proceso
kill -9 <PID>

# O cambiar puerto en app.py
# Buscar: app.run(debug=True)
# Cambiar a: app.run(debug=True, port=5001)
```

### "No se puede encontrar archivo MP3"
- Verificar que los archivos están en carpeta `canciones/`
- Verificar que la extensión es `.mp3` (sensible a mayúsculas)
- Verificar permisos de lectura en la carpeta

### "Canción no suena"
- Verificar que está habilitada (check verde)
- Verificar hora del servidor (en tab Estado)
- Revisar logs: `tail logs/musicbell.log`

---

## 📝 Cambios Recientes

### Versión 2.0 - Interfaz con Tabs
✨ **Nuevas características:**
- ✅ Navegación por 5 tabs principales
- ✅ Carga automática de canciones en programación rápida
- ✅ Mejor organización visual
- ✅ Resumen detallado con lista de canciones
- ✅ Animaciones suaves de transición

📄 Ver más detalles en [CAMBIOS_INTERFAZ_TABS.md](CAMBIOS_INTERFAZ_TABS.md)

---

## 📞 Soporte

Si encuentras problemas:
1. Revisar los logs: `logs/musicbell.log`
2. Verificar que el servidor está corriendo: `http://localhost:5000`
3. Consultar documentación específica en la carpeta `/`

---

## 📄 Licencia

MusicBell © 2026 - Sistema de reproducción automática para escuelas

---

## 🎉 ¡Gracias por usar MusicBell!

Para más información, consulta la documentación en la carpeta del proyecto.
