# 🪟 Guía de Instalación para Windows

## Requisitos Previos

- **Windows 7 o superior**
- **Python 3.8 o superior**
- **Navegador moderno** (Chrome, Firefox, Edge, Safari)

## 🚀 Instalación Rápida (3 pasos)

### Paso 1: Instalar Python

Si aún no tienes Python instalado:

1. Descarga desde: https://www.python.org/downloads/
2. Ejecuta el instalador
3. **⚠️ IMPORTANTE**: Marca la opción **"Add Python to PATH"**
4. Click en "Install Now"

**Verificar que Python está instalado:**

- Abre `PowerShell` o `CMD`
- Ejecuta: `python --version`
- Deberías ver algo como: `Python 3.10.5`

### Paso 2: Ejecutar el Instalador de Requisitos

**Opción A: Doble clic (Más fácil)**

1. Navega a la carpeta `MusicBell`
2. Haz doble clic en: **`install_requirements.bat`**
3. Espera a que termine (mostrará "✅ INSTALACIÓN COMPLETADA")

**Opción B: Línea de comandos**

1. Abre `PowerShell` o `CMD`
2. Navega a la carpeta: `cd C:\ruta\a\MusicBell`
3. Ejecuta: `install_requirements.bat`

### Paso 3: Ejecutar la Aplicación

**Opción A: Doble clic (Más fácil)**

1. En la carpeta `MusicBell`, haz doble clic en: **`run.bat`**
2. Se abrirá una ventana del terminal
3. Abre tu navegador en: **http://localhost:5000**

**Opción B: Línea de comandos**

1. Abre `PowerShell` o `CMD`
2. Navega a: `cd C:\ruta\a\MusicBell`
3. Ejecuta: `python backend\app.py`
4. Abre: **http://localhost:5000**

## ✅ Verificación

Después de ejecutar `install_requirements.bat`, deberías ver:

```
✓ Python 3.x.x detectado
✓ pip x.x.x detectado
✓ Dependencias instaladas correctamente
✓ Carpeta 'canciones' creada
✓ Todas las dependencias están instaladas correctamente

========================================
   ✅ INSTALACIÓN COMPLETADA
========================================
```

## 📁 Estructura de Carpetas

Después de la instalación:

```
MusicBell/
├── backend/
│   ├── app.py
│   ├── music_player.py
│   ├── utils.py
│   ├── cli.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── config/
│   └── canciones.json (se crea automáticamente)
├── canciones/          ← Aquí van tus archivos MP3
├── logs/
│   └── musicbell.log
├── install_requirements.bat  ← Ejecuta primero
├── run.bat                  ← Ejecuta para iniciar
└── README.md
```

## 🎵 Añadir Canciones

1. Coloca tus archivos MP3 en la carpeta: `canciones/`
2. Los archivos deben tener extensión: `.mp3` (minúscula)
3. Ejemplos válidos:
   - `himno.mp3`
   - `recreo_escolar.mp3`
   - `musica_fondo.mp3`

## ❓ Solución de Problemas

### Error: "Python no está instalado"

**Solución:**

1. Descarga Python: https://www.python.org/downloads/
2. Asegúrate de marcar "Add Python to PATH"
3. Reinicia tu computadora
4. Vuelve a ejecutar `install_requirements.bat`

### Error: "Las dependencias no están instaladas"

**Solución:**

1. Abre `PowerShell` como administrador
2. Navega a la carpeta: `cd C:\ruta\a\MusicBell`
3. Ejecuta: `pip install -r backend\requirements.txt`
4. Espera a que termine

### No se reproduce sonido

**Solución:**

1. Verifica que los archivos MP3 sean válidos
2. Asegúrate de que están en `canciones/`
3. Revisa los logs: `logs\musicbell.log`

### La aplicación se inicia pero no se conecta

**Solución:**

1. Verifica que no hay otra aplicación usando el puerto 5000
2. Intenta abrir: `http://127.0.0.1:5000`
3. Si aún no funciona, reinicia tu computadora

### Error al ejecutar los scripts .bat

Si los scripts no se ejecutan:

1. Abre `PowerShell` como administrador
2. Ejecuta:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Presiona `Y` cuando te pida confirmación
4. Vuelve a intentar ejecutar los scripts

## 🔧 Cambiar el Puerto

Si el puerto 5000 está en uso:

1. Abre: `backend\app.py`
2. Busca la línea: `app.run(host='0.0.0.0', port=5000)`
3. Cambia `5000` por otro número, ej: `5001`
4. Guarda el archivo
5. Inicia la aplicación de nuevo
6. Accede a: `http://localhost:5001`

## 📊 Monitoreo

Para ver lo que está sucediendo:

1. Logs en tiempo real: `logs\musicbell.log`
2. Abre el archivo con Notepad o VSCode
3. Presiona `F5` para actualizar

## 🆘 Obtener Ayuda

Si experimentas problemas:

1. Revisa los logs: `logs\musicbell.log`
2. Lee [FAQ.md](../FAQ.md)
3. Verifica [DESARROLLO.md](../DESARROLLO.md) para detalles técnicos

## 📝 Scripts Disponibles

| Script                     | Función                        |
| -------------------------- | ------------------------------ |
| `install_requirements.bat` | Instala todas las dependencias |
| `run.bat`                  | Inicia la aplicación           |
| `backend\app.py`           | API del servidor               |

---

**¡Listo!** 🎉 Tu aplicación MusicBell está funcionando en Windows.

Para detener la aplicación: Presiona `Ctrl+C` en la ventana del terminal.
