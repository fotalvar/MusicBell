# Debugging: Sin Sonido en Windows

## 🚨 Pasos para Diagnosticar (En orden)

### PASO 1: Verifica VLC Básico

En PowerShell/CMD:

```bash
cd C:\ruta\a\MusicBell\backend
python test_vlc_simple.py
```

**Resultado esperado:**

```
✅ Test ultra simple de reproducción
✅ VLC importado
✅ ¡Prueba exitosa!
```

Si falla aquí, VLC no está correctamente instalado.

---

### PASO 2: Verifica los Archivos MP3

```bash
# Ver archivos
dir ..\canciones\

# Probar si un archivo MP3 es válido
cd ..\canciones
# Intenta reproducir manualmente un MP3 en Windows
# (Haz doble clic en un archivo .mp3)
```

**Si no suena**: El archivo MP3 está corrupto.

---

### PASO 3: Verifica Python VLC

```bash
python -c "import vlc; print('VLC:', vlc.__version__)"
```

**Si falla:** Instala VLC:

```bash
python -m pip install --upgrade python-vlc==3.0.20123
```

---

### PASO 4: Verifica Flask recibe la orden

1. En PowerShell, ejecuta el backend en modo verbose:

```bash
cd C:\ruta\a\MusicBell
set FLASK_DEBUG=True
python backend\app.py
```

2. Abre en Chrome: `http://localhost:5000`

3. Ve a "Reproducción" y haz clic en "▶ Reproducir"

4. **Revisa la salida de Flask** - Debe mostrar:

```
POST /api/reproducir/cancion.mp3
Intentando reproducir: C:\ruta\a\canciones\cancion.mp3
✅ REPRODUCCIÓN EXITOSA
```

Si ves este mensaje pero NO suena, continúa...

---

### PASO 5: Revisa los Logs

```bash
# Ver últimas líneas del log
Get-Content logs\musicbell.log -Tail 50  # PowerShell

# O en CMD:
type logs\musicbell.log
```

**Busca líneas con:**

- ❌ `ERROR`
- ✅ `REPRODUCCIÓN EXITOSA`
- ❌ `No está instalado`

---

### PASO 6: Verifica Permisos de Carpeta

```bash
# En PowerShell (como admin):
icacls "C:\ruta\a\MusicBell\canciones" /grant:r "%USERNAME%":F

# En CMD (como admin):
cacls "C:\ruta\a\MusicBell\canciones" /G Everyone:F
```

---

### PASO 7: Verifica Volumen de Windows

1. **Click derecho en ícono de volumen** (esquina inferior derecha)
2. **Volume mixer** → Verifica que:
   - Sistema NO está en silencio
   - No hay muteado ningún dispositivo
3. **Prueba sonido del sistema**:
   - Settings > Sound > Volume > Test sound

---

## 🔍 Tabla de Síntomas

| Síntoma                            | Causa Probable          | Solución                            |
| ---------------------------------- | ----------------------- | ----------------------------------- |
| `test_vlc_simple.py` falla         | VLC no instalado        | `pip install python-vlc==3.0.20123` |
| Flask dice "EXITOSO" pero no suena | Volumen = 0             | Sube volumen de Windows             |
| "❌ python-vlc not found"          | Librería no instalada   | `pip install python-vlc==3.0.20123` |
| Archivo MP3 no reproduce           | Archivo corrupto        | Descarga otro MP3 de prueba         |
| Logs vacíos                        | Backend no ejecutándose | Inicia el backend                   |
| "Permiso denegado"                 | Permisos carpeta        | Ejecuta como admin                  |

---

## 📝 Información para Reportar

Si nada funciona, comparte:

```bash
# 1. Versión Python
python --version

# 2. VLC instalado?
python -m pip show python-vlc

# 3. Resultado del test simple
python backend\test_vlc_simple.py

# 4. Últimos logs
type logs\musicbell.log

# 5. Contenido de canciones/
dir canciones\

# 6. Intentar reproducir manualmente
python
>>> import vlc
>>> instance = vlc.Instance()
>>> # Si no da error, VLC funciona
```

---

## 💡 Soluciones Rápidas

### "No suena pero Flask dice que funciona"

- Sube volumen de Windows
- Verifica que los altavoces están conectados
- Prueba reproducir un video en YouTube

### "Error: python-vlc not found"

```bash
python -m pip install --upgrade pip
python -m pip install python-vlc==3.0.20123
```

### "Permisos denegados"

- Ejecuta PowerShell **como administrador**
- Intenta de nuevo

### "Archivo no encontrado"

- Verifica que los MP3 están en `C:\ruta\a\MusicBell\canciones\`
- Las mayúsculas/minúsculas importan

---

## 🔧 Testing Manual de VLC

Copia esto en Python para probar directamente:

```python
import vlc
import time

# Ruta del archivo
audio_file = r"C:\ruta\a\tu\archivo.mp3"

# Crear instancia
instance = vlc.Instance()

# Crear lista
media_list = instance.media_list_new()
media = instance.media_new(audio_file)
media_list.add_media(media)

# Reproducir
player = instance.list_player_new()
player.set_media_list(media_list)
player.play()

print("Reproduciendo...")
time.sleep(5)

player.stop()
print("Detenido")
```

Si esto funciona, VLC está bien instalado.

---

## 📞 Cuando Nada Funciona

1. Desinstala y reinstala VLC Media Player: https://www.videolan.org/vlc/
2. Desinstala python-vlc:
   ```bash
   python -m pip uninstall python-vlc
   ```
3. Reinstala python-vlc:
   ```bash
   python -m pip install python-vlc==3.0.20123
   ```
4. Reinicia Windows
5. Intenta de nuevo

---

**Última actualización**: 5 de febrero de 2026
