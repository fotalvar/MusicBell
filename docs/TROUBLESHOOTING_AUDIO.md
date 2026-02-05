# Solución: No hay sonido en Windows

## 🔍 Diagnóstico Paso a Paso

### Paso 1: Verificar que playsound está instalado

En PowerShell/CMD en Windows:

```bash
python -m pip list | findstr playsound
```

Si no aparece, **instálalo ahora**:

```bash
python -m pip install playsound==1.2.2
```

### Paso 2: Ejecutar script de diagnóstico

```bash
cd C:\ruta\a\MusicBell\backend
python diagnostico_audio.py
```

Este script te dirá exactamente dónde está el problema.

---

## ✅ Checklist de Solución

### ✔️ 1. Playsound instalado

```bash
python -c "import playsound; print('OK')"
```

Si falla:

```bash
python -m pip install --upgrade pip
python -m pip install playsound==1.2.2
```

### ✔️ 2. Verificar archivos MP3

- Abre la carpeta: `C:\ruta\a\MusicBell\canciones\`
- Debe haber archivos `.mp3`
- Prueba reproducir manualmente un MP3 en Windows

### ✔️ 3. Verificar volumen

- **Click derecho en ícono de volumen** (esquina inferior derecha)
- Asegúrate que el volumen **NO está en 0**
- Prueba sonido del sistema: Settings > Sound > Volume mixer

### ✔️ 4. Revisar logs

```bash
# Ver últimas líneas del log
cat logs\musicbell.log | tail -20

# En PowerShell:
Get-Content logs\musicbell.log -Tail 20
```

Busca líneas con:

- ❌ `Error` o `ERROR`
- ✅ `Reproduciendo` o `Reproducción finalizada`

---

## 🛠️ Soluciones por Error

### Error: "playsound is not defined"

```bash
python -m pip install playsound==1.2.2
```

### Error: "No module named playsound"

```bash
python -m pip install --upgrade pip
python -m pip install playsound==1.2.2
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
4. Reinicia Windows

---

## 🔄 Fallbacks Automáticos

Si `playsound` falla, el backend intenta automáticamente:

1. **playsound** (Python library)
2. **wmplayer.exe** (Windows Media Player)
3. Error registrado en logs

Ambos métodos deberían funcionar si Windows está bien configurado.

---

## 🧪 Pruebas Manuales

### Test 1: Verificar playsound

```python
python
>>> from playsound import playsound
>>> playsound(r"C:\ruta\a\cancion.mp3")
# Debería sonar aquí
```

### Test 2: Verificar wmplayer

```bash
"C:\Program Files\Windows Media Player\wmplayer.exe" "C:\ruta\a\cancion.mp3"
```

### Test 3: Reproducir desde frontend

1. Abre http://localhost:5000
2. Ve a pestaña "Reproducción"
3. Haz click en "▶ Reproducir" en cualquier canción
4. Revisa logs: `logs\musicbell.log`

---

## 📋 Información para Reportar

Si ninguna solución funciona, reporta con:

```bash
# 1. Versión de Python
python --version

# 2. Playsound instalado?
python -m pip show playsound

# 3. Últimos logs
cat logs\musicbell.log

# 4. Archivos en canciones/
dir canciones\

# 5. Test manual
python diagnostico_audio.py
```

---

## 🎯 Resumen Rápido

| Problema              | Solución                       |
| --------------------- | ------------------------------ |
| "playsound not found" | `pip install playsound==1.2.2` |
| No suena nada         | Ejecuta `diagnostico_audio.py` |
| Volumen = 0           | Sube volumen de Windows        |
| Archivo no existe     | Verifica `canciones/`          |
| Aún no funciona       | Reinicia backend y Windows     |

---

**Última actualización**: 5 de febrero de 2026
