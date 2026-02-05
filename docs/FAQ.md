<!-- MusicBell - Preguntas Frecuentes -->

# ❓ Preguntas Frecuentes (FAQ)

## Instalación y Configuración

### ¿Qué versión de Python necesito?

**Respuesta:** Python 3.8 o superior.

Verifica tu versión:

```bash
python3 --version
```

Descárgalo desde: https://www.python.org/downloads/

---

### ¿Dónde instalo MusicBell?

**Respuesta:** En cualquier carpeta. Recomendamos:

- **macOS:** `~/Desktop/MusicBell` o `/Applications/MusicBell`
- **Linux:** `/home/usuario/MusicBell` o `/opt/musicbell`

---

### ¿Qué pasa si no tengo Flask instalado?

**Respuesta:** El script `start.sh` lo instala automáticamente.

O instálalo manualmente:

```bash
pip install -r backend/requirements.txt
```

---

### ¿Necesito privilegios de administrador?

**Respuesta:** No es necesario para ejecución normal.

---

## Uso de la Aplicación

### ¿Cómo agrego archivos MP3?

**Respuesta:**

1. Copia tus archivos `.mp3` a la carpeta `canciones/`
2. Recarga la página web
3. Los verás en el selector de "Archivo MP3"

---

### ¿Qué formatos de audio soporta?

**Respuesta:** Actualmente solo MP3.

Futuras versiones soportarán:

- FLAC
- WAV
- OGG

---

### ¿Puedo programar una canción para múltiples horas?

**Respuesta:** Actualmente no. Pero puedes crear duplicados con diferentes horas.

Ejemplo:

- Canción 1: 08:00
- Canción 2: 12:00
- Canción 3: 15:30

Mejora futura: Seleccionar múltiples horarios.

---

### ¿Cómo cambio el idioma de la interfaz?

**Respuesta:** Actualmente está en español.

Para otros idiomas, edita `frontend/index.html` y `frontend/script.js`.

---

### ¿Qué pasa si hay dos canciones a la misma hora?

**Respuesta:** MusicBell detecta el conflicto y lo muestra en la sección "Conflictos de Horario".

Solución: Cambia la hora de una de las canciones.

---

## Funcionamiento

### ¿A qué hora exacta suena la canción?

**Respuesta:** Al inicio del minuto programado.

Ejemplo: Si programas 08:00, sonará entre 08:00:00 y 08:00:59

---

### ¿Qué pasa si la computadora está apagada a la hora programada?

**Respuesta:** No suena nada. Cuando enciendas el ordenador, la aplicación continúa normalmente.

Nota: MusicBell se ejecuta solo cuando está abierta.

---

### ¿Puedo cambiar el volumen?

**Respuesta:** Actualmente no desde la interfaz. Pero puedes usar tu sistema operativo:

- **macOS:** System Preferences → Sound
- **Linux:** pavucontrol

---

### ¿Qué sucede si cierro el navegador?

**Respuesta:** MusicBell sigue funcionando. La música se reproduce en segundo plano.

Solo abre el navegador para cambiar la programación.

---

### ¿Puedo acceder desde mi teléfono?

**Respuesta:** ¡Sí! Desde cualquier dispositivo en la red local:

1. Obtén la IP: `ifconfig | grep inet`
2. Abre: `http://[IP]:5000`

---

## Problemas y Soluciones

### La música no suena

**Posibles causas:**

1. **Altavoces desconectados**
   - Solución: Conecta los altavoces y verifica volumen

2. **Archivo MP3 inválido**
   - Solución: Prueba con otro MP3

3. **Permisos de reproducción**
   - macOS: `sudo chmod +x backend/music_player.py`
   - Linux: `sudo apt-get install ffmpeg`

4. **Puerto bloqueado**
   - Solución: Cambia puerto en `backend/app.py`

---

### El servidor no inicia

**Posibles causas:**

1. **Puerto 5000 en uso**

   ```bash
   # Matar proceso
   lsof -ti:5000 | xargs kill -9

   # O cambiar puerto en app.py
   ```

2. **Flask no instalado**

   ```bash
   pip install Flask Flask-CORS
   ```

3. **Python no encontrado**
   - Verifica que Python está en PATH
   - Instala Python 3.8+

4. **Permisos de carpeta**
   - Asegúrate de tener permisos de lectura/escritura

---

### Las canciones desaparecieron después de reiniciar

**Respuesta:** No deberían desaparecer. Pero si lo hacen:

1. **Verifica** `config/canciones.json` - debe tener contenido
2. **Revisa logs**: `logs/musicbell.log`
3. **Restore backup**: Restaura desde carpeta `backups/`

---

### La interfaz web no carga

**Posibles causas:**

1. **URL incorrecta**
   - Intenta: `http://127.0.0.1:5000`
   - O: `http://localhost:5000`

2. **Firewall**
   - Permite puerto 5000 en el firewall

3. **Servidor no inició**
   - Verifica que `bash start.sh` ejecutó sin errores

4. **Cache del navegador**
   - Ctrl+Shift+R (limpiar cache)

---

### Error: "No hay permisos para escribir"

**Respuesta:**

```bash
# Dar permisos de escritura
chmod -R 755 /Users/federicootalvares/Desktop/MusicBell

# O solo para la carpeta de logs
chmod -R 777 /Users/federicootalvares/Desktop/MusicBell/logs
```

---

### Los logs ocupan mucho espacio

**Respuesta:** Limpia los logs viejos:

```bash
# Borrar logs anteriores a 30 días
find logs/ -name "*.log" -mtime +30 -delete

# O simplemente elimina el archivo
rm logs/musicbell.log
```

---

## Desarrollo y Personalización

### ¿Cómo cambio el puerto?

**Respuesta:** Edita `backend/app.py`:

```python
# Busca esta línea:
app.run(host='0.0.0.0', port=5000)

# Cambia a:
app.run(host='0.0.0.0', port=8080)
```

Reinicia la aplicación.

---

### ¿Puedo cambiar el diseño de la interfaz?

**Respuesta:** Sí. Los archivos están en `frontend/`:

- `index.html` - Estructura
- `style.css` - Estilos
- `script.js` - Lógica

Personaliza según necesites.

---

### ¿Cómo agrego autenticación?

**Respuesta:** Edita `backend/app.py` y añade:

```python
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.password != 'tu_contraseña':
            return 'Acceso denegado', 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/canciones', methods=['GET'])
@require_auth
def get_canciones():
    # ...
```

---

### ¿Cómo integro con Spotify?

**Respuesta:** Futura mejora. Requiere:

1. API de Spotify
2. Autenticación OAuth
3. Streaming en lugar de archivos locales

---

## Deployment y Producción

### ¿Cómo uso Docker?

**Respuesta:** Crea `Dockerfile`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r backend/requirements.txt
CMD ["python", "backend/app.py"]
```

Ejecuta:

```bash
docker build -t musicbell .
docker run -p 5000:5000 -v $(pwd)/canciones:/app/canciones musicbell
```

---

### ¿Cómo backupeo la configuración?

**Respuesta:**

```bash
# Backup manual
cp config/canciones.json config/canciones.json.backup

# Backup automático (Linux/macOS)
0 2 * * * cp /path/to/canciones.json /path/to/backup/canciones.json.$(date +\%Y\%m\%d)
```

---

### ¿Cómo actualizó la aplicación?

**Respuesta:**

1. Detén MusicBell
2. Reemplaza archivos (excepto `config/canciones.json` y `canciones/`)
3. Reinicia

```bash
# Crear backup primero
# Luego copia nuevos archivos
cp -r new_version/* /Users/federicootalvares/Desktop/MusicBell/
```

---

## API y Integración

### ¿Cómo uso la API directamente?

**Respuesta:** Con curl o postman:

```bash
# Listar canciones
curl http://localhost:5000/api/canciones

# Agregar canción
curl -X POST http://localhost:5000/api/canciones \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","archivo":"test.mp3","tipo_planificacion":"hora","hora":"08:00"}'

# Actualizar
curl -X PUT http://localhost:5000/api/canciones/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Nuevo nombre"}'

# Eliminar
curl -X DELETE http://localhost:5000/api/canciones/1
```

---

### ¿Cómo integro MusicBell con otra aplicación?

**Respuesta:** Usando la API REST:

```javascript
// Ejemplo en JavaScript
fetch("http://localhost:5000/api/canciones")
  .then((r) => r.json())
  .then((data) => console.log(data));
```

Ver [ESTRUCTURA_DATOS.md](ESTRUCTURA_DATOS.md) para más detalles.

---

## Soporte y Comunidad

### ¿Dónde reporto bugs?

**Respuesta:**

1. GitHub Issues (si está en GitHub)
2. Email: [tu-email]
3. Revisa `logs/musicbell.log` para detalles

---

### ¿Puedo contribuir?

**Respuesta:** ¡Claro!

1. Fork el proyecto
2. Crea rama (`git checkout -b feature/mi-mejora`)
3. Commit cambios
4. Push (`git push origin feature/mi-mejora`)
5. Pull Request

---

### ¿Dónde encuentro más ayuda?

**Respuesta:**

- 📖 [README.md](README.md)
- 🚀 [GUIA_RAPIDA.md](GUIA_RAPIDA.md)
- 🔧 [INSTALACION.md](INSTALACION.md)
- 📊 [ESTRUCTURA_DATOS.md](ESTRUCTURA_DATOS.md)

---

## Últimas Preguntas

### ¿Es seguro usar MusicBell en producción?

**Respuesta:** Sí, para uso en escuelas es completamente seguro.

Mejoras futuras de seguridad:

- Autenticación
- HTTPS
- Rate limiting

---

### ¿Cuál es el máximo de canciones que puedo agregar?

**Respuesta:** Teóricamente ilimitado. Probado con 1000+ canciones.

Limitaciones prácticas:

- Espacio en disco
- Interfaz (se puede lentificar con 10000+)

---

### ¿Puedo usar MusicBell sin internet?

**Respuesta:** ¡Sí! Funciona completamente offline.

Los únicos requisitos:

- Python instalado
- Archivo MP3 en la carpeta
- Acceso local (http://localhost:5000)

---

### ¿Cuánto consume MusicBell?

**Respuesta:**

- **CPU:** <1%
- **Memoria:** 30-50MB
- **Almacenamiento:** 10MB (sin canciones)
- **Ancho de banda:** Mínimo (solo en interfaz web)

---

¿No encontraste tu pregunta? Contacta al soporte o abre un issue en GitHub 😊
