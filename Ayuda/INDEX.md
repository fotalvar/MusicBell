# 📚 Índice de MusicBell

Este archivo es un índice de navegación rápida. Consulta los documentos específicos según tus necesidades.

## 📖 Documentación

| Documento | Propósito |
|-----------|-----------|
| **[README.md](README.md)** | 📖 Guía completa del proyecto |
| **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** | ⚡ Empezar en 60 segundos |
| **[INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md)** | 🪟 Instalación en Windows |
| **[DESARROLLO.md](DESARROLLO.md)** | 🔧 Para desarrolladores |
| **[ESTRUCTURA_DATOS.md](ESTRUCTURA_DATOS.md)** | 📊 Formato JSON y datos |
| **[CHANGELOG.md](CHANGELOG.md)** | 📝 Cambios y versiones |
| **[FAQ.md](FAQ.md)** | ❓ Preguntas frecuentes |
| **[OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)** | ⚙️ Mejoras de rendimiento |

## 🎯 Acceso Rápido

- **¿Primer uso?** → [GUIA_RAPIDA.md](GUIA_RAPIDA.md)
- **¿Instalación?** → [README.md](README.md)
- **¿Windows?** → [INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md)
- **¿Problemas?** → [FAQ.md](FAQ.md)
- **¿Desarrollo?** → [DESARROLLO.md](DESARROLLO.md)

### 3. Instalar Dependencias
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 4. Agregar Canciones
Coloca archivos `.mp3` en la carpeta `canciones/`

### 5. Ejecutar
```bash
bash start.sh          # macOS/Linux
start_windows.bat      # Windows
```

---

## 🌐 Acceso Remoto

Desde cualquier dispositivo en tu red:

1. Obtén la IP de la máquina:
   ```bash
   # macOS/Linux
   ifconfig | grep "inet " | grep -v 127
   
   # Windows
   ipconfig
   ```

2. Abre en tu navegador:
   ```
   http://[IP]:5000
   ```

---

## 🛠️ API REST

### Endpoints Disponibles

```
GET    /api/canciones              # Listar canciones
POST   /api/canciones              # Agregar canción
PUT    /api/canciones/<id>         # Actualizar canción
DELETE /api/canciones/<id>         # Eliminar canción

GET    /api/estado                 # Estado actual
GET    /api/archivos               # Listar MP3 disponibles
GET    /api/detectar-conflictos    # Detectar solapamientos
```

### Ejemplo: Agregar Canción
```bash
curl -X POST http://localhost:5000/api/canciones \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Himno",
    "archivo": "himno.mp3",
    "tipo_planificacion": "hora",
    "hora": "08:00"
  }'
```

---

## 📊 Base de Datos (JSON)

Estructura de `config/canciones.json`:

```json
{
  "canciones": [
    {
      "id": 1,
      "nombre": "Himno",
      "archivo": "himno.mp3",
      "tipo_planificacion": "hora",
      "hora": "08:00",
      "habilitada": true
    }
  ],
  "estado_reproduccion": {
    "reproduciendo": false,
    "cancion_actual": null,
    "fecha_ultima_actualizacion": "2026-01-29T14:30:00"
  }
}
```

---

## ⚙️ Configuración Avanzada

### Variables de Entorno
Copia `.env.example` a `.env` y ajusta:

```bash
FLASK_PORT=5000
FLASK_HOST=0.0.0.0
FLASK_DEBUG=False
CHECK_INTERVAL=10
LOG_LEVEL=INFO
```

### Cambiar Puerto
Edita `backend/app.py`:
```python
app.run(host='0.0.0.0', port=8080)  # Cambiar 5000 a 8080
```

---

## 🐛 Solución de Problemas

| Problema | Solución |
|----------|----------|
| "Port 5000 in use" | `lsof -ti:5000 \| xargs kill -9` |
| No se escucha sonido | Verifica altavoces y permisos |
| No encuentra archivos | Asegúrate que están en `canciones/` con `.mp3` |
| Python no encontrado | Instala Python 3.8+ y añádelo al PATH |
| Error de CORS | Actualiza Flask-CORS: `pip install --upgrade Flask-CORS` |

---

## 🚀 Despliegue en Producción

### Windows como Servicio
Ver: [INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md)

### Docker (futuro)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r backend/requirements.txt
CMD ["python", "backend/app.py"]
```

---

## 📚 Documentación Completa

- **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** - Comienza aquí
- **[PRUEBAS_MAC.md](PRUEBAS_MAC.md)** - Testing detallado
- **[INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md)** - Windows 7/8/10/11
- **[ESTRUCTURA_DATOS.md](ESTRUCTURA_DATOS.md)** - Formato de datos
- **[DESARROLLO.md](DESARROLLO.md)** - Para developers

---

## 🤝 Contribuciones

¿Tienes ideas para mejorar MusicBell?

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -am 'Añade mejora'`)
4. Push (`git push origin feature/mejora`)
5. Abre un Pull Request

---

## 📋 Roadmap

### v1.0 (Actual) ✅
- [x] Reproducción automática
- [x] Interfaz web
- [x] Programación flexible
- [x] Persistencia

### v1.1 (Próximo)
- [ ] Control de volumen
- [ ] Previsualización de audio
- [ ] Autenticación de usuario
- [ ] Estadísticas

### v2.0 (Futuro)
- [ ] Integración con Spotify
- [ ] App móvil
- [ ] Grabación automática
- [ ] Sincronización NTP

---

## 📞 Soporte

- 📧 Email: [tu-email]
- 💬 Issues: GitHub Issues
- 📖 Wiki: [Próximamente]

---

## 📄 Licencia

Este proyecto es de **código abierto** y disponible bajo licencia MIT.

Eres libre de:
- ✅ Usar en producción
- ✅ Modificar el código
- ✅ Distribuir
- ✅ Usar comercialmente

Con la única condición de mantener la atribución.

---

## 🙏 Agradecimientos

Gracias por usar MusicBell. Fue diseñado pensando en las escuelas y espacios públicos.

---

<div align="center">

**[⬆ Arriba](#-musicbell)**

Hecho con ❤️ para escuelas 🎵

</div>
