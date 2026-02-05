# Solución: Reproducción de Audio con VLC

## ✅ Instalación Rápida

En terminal (macOS/Linux):

```bash
# 1. Instalar python-vlc
pip3 install python-vlc==3.0.20123

# 2. Instalar todas las dependencias
cd backend
pip3 install -r requirements.txt

# 3. Ejecutar diagnóstico
python3 diagnostico_audio.py
```

---

## 🎵 ¿Por qué VLC?

VLC es la solución definitiva:

✅ **Sin interfaz gráfica** - Solo reproduce audio, sin abrir ventanas  
✅ **Sin procesos visibles** - El sonido sale directamente por los altavoces  
✅ **Soporta todos los formatos** - MP3, FLAC, WAV, OGG, etc.  
✅ **Multiplataforma** - macOS, Linux  
✅ **Robusto** - Usado por millones de usuarios

### ✔️ 1. Verificar python-vlc

```bash
python3 -c "import vlc; print('OK')"
```

Si falla:

```bash
pip3 install --upgrade pip
pip3 install python-vlc==3.0.20123
```

### ✔️ 2. Verificar archivos MP3

- Abre la carpeta: `MusicBell/canciones/`
- Debe haber archivos `.mp3`
- Prueba reproducir manualmente un MP3

### ✔️ 3. Verificar volumen

- Usa los controles de volumen de tu sistema operativo
- Asegúrate que el volumen **NO está en 0**
- Prueba reproducir un video en YouTube

### ✔️ 4. Revisar logs

```bash
# Ver últimas líneas del log
tail -20 logs/musicbell.log
```

Busca líneas con:

- ❌ `Error` o `ERROR`
- ✅ `Reproduciendo` o `Reproducción finalizada`

---

## 🛠️ Soluciones por Error

### Error: "No module named vlc"

```bash
pip3 install --upgrade pip
pip3 install python-vlc==3.0.20123
```

### Error: "Archivo no encontrado"

- Verifica que los MP3 están en `canciones/`
- Los nombres deben ser exactos (mayúsculas/minúsculas importan)

### Error: "ModuleNotFoundError: No module named 'flask'"

Instala todas las dependencias:

```bash
cd backend
pip install -r requirements.txt
```

### No aparece error pero NO suena nada

1. Ejecuta `diagnostico_audio.py`
2. Verifica que el volumen NO está en silencio
3. Verifica que los altavoces están conectados
4. Reinicia tu sistema

---

## 🧪 Pruebas Manuales

### Test 1: Verificar VLC

```python
python
>>> import vlc
>>> instance = vlc.Instance()
# Si no da error, VLC funciona correctamente
```

### Test 2: Reproducir desde frontend

1. Abre http://localhost:5000
2. Ve a pestaña "Reproducción"
3. Haz click en "▶ Reproducir" en cualquier canción
4. Revisa logs: `logs/musicbell.log`

---

## 📋 Información para Reportar

Si ninguna solución funciona, reporta con:

```bash
# 1. Versión de Python
python3 --version

# 2. python-vlc instalado?
pip3 show python-vlc

# 3. Últimos logs
tail -50 logs/musicbell.log

# 4. Archivos en canciones/
ls -la canciones/

# 5. Test automático
python3 diagnostico_audio.py
```

---

## 🎯 Resumen Rápido

| Problema               | Solución                                    |
| ---------------------- | ------------------------------------------- |
| "python-vlc not found" | `pip3 install python-vlc==3.0.20123`        |
| "libvlc not found"     | Instala VLC Media Player desde videolan.org |
| No suena nada          | Ejecuta `diagnostico_audio.py`              |
| Volumen = 0            | Sube volumen del sistema                    |
| Archivo no existe      | Verifica `canciones/`                       |
| Aún no funciona        | Reinicia backend                            |

---

## 📞 Debugging

Si quieres ver qué está pasando en real-time:

```bash
# Terminal: Backend en modo verbose
export FLASK_DEBUG=True
python3 backend/app.py

# Otra terminal: Ver logs en tiempo real
tail -f logs/musicbell.log
```

---

**Motor de reproducción**: VLC (python-vlc 3.0.20123)  
**Última actualización**: 5 de febrero de 2026
