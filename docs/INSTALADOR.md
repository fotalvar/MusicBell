# Instalador de Dependencias para Linux Mint

## ¿Qué es?

`install-dependencies.sh` es un script automatizado que instala todas las dependencias necesarias para ejecutar MusicBell en Linux Mint.

## ¿Qué instala?

✅ **Python 3** - Lenguaje de programación  
✅ **pip3** - Gestor de paquetes de Python  
✅ **VLC** - Motor de reproducción de audio  
✅ **python-vlc** - Librería para controlar VLC desde Python  
✅ **Flask** - Framework web para el backend  
✅ **Flask-CORS** - Soporte para CORS  
✅ **Todas las dependencias del proyecto**

## Uso

### Paso 1: Abrir terminal

```bash
cd /ruta/a/MusicBell
```

### Paso 2: Ejecutar el instalador

```bash
bash install-dependencies.sh
```

### Paso 3: Esperar a que termine

El script mostrará el progreso con emojis y colores:

- ✅ Verde = Exitoso
- ⚠️ Amarillo = Advertencia
- ✗ Rojo = Error
- ℹ️ Azul = Información

## ¿Qué sucede si hay un error?

Si el script falla en algún punto:

1. **Lee el mensaje de error** - Te indica qué falló
2. **Instala manualmente** lo que falte (el script lo sugerirá)
3. **Ejecuta el instalador de nuevo** - Puedes ejecutarlo múltiples veces

Ejemplo:

```bash
# Si falla VLC
sudo apt-get install vlc vlc-plugin-base

# Si fallan dependencias de Python
pip3 install -r backend/requirements.txt

# Luego ejecuta el instalador de nuevo
bash install-dependencies.sh
```

## Error: "Error al actualizar la lista de paquetes"

Este es el error más común. **No significa que no se pueda continuar**. Intenta esto:

### Solución 1: Verificar conexión a internet

```bash
ping google.com
```

Si no hay respuesta, no tienes conexión a internet.

### Solución 2: Limpiar cache de apt

```bash
sudo apt-get clean
sudo apt-get autoclean
bash install-dependencies.sh
```

### Solución 3: Reparar repositorios dañados

```bash
sudo apt-get update --fix-missing
bash install-dependencies.sh
```

### Solución 4: Actualización completa del sistema

```bash
sudo apt-get update
sudo apt-get upgrade
bash install-dependencies.sh
```

### Solución 5: Ver detalles del error

```bash
bash -x install-dependencies.sh
```

Esto mostrará exactamente qué está fallando.

### Solución 6: Ayuda del script

```bash
bash install-dependencies.sh --help
bash install-dependencies.sh --troubleshoot
```

## Requisitos previos

- **Linux Mint** (u otro Linux basado en Debian)
- **Conexión a internet** (obligatorio para `apt-get`)
- **Permisos de sudo** (para instalar paquetes del sistema)
- **Al menos 500MB de espacio libre** en disco

## Pasos después de instalar

Una vez que el instalador termine:

### 1. Coloca tus archivos MP3

```bash
mkdir -p canciones
# Copia tus archivos .mp3 a la carpeta canciones/
```

### 2. Inicia MusicBell

```bash
bash start.sh
```

### 3. Abre en tu navegador

```
http://localhost:5000
```

## Solución de problemas

### "sudo: comando no encontrado"

Significa que `sudo` no está disponible. Ejecuta:

```bash
su
bash install-dependencies.sh
```

### "E: No se puede instalar los paquetes en estado no confiable"

Puede ocurrir en algunas configuraciones. Intenta:

```bash
sudo apt-get install -y --allow-unauthenticated vlc vlc-plugin-base
```

### "Python3 no se instala"

Intenta actualizar primero:

```bash
sudo apt-get update
sudo apt-get upgrade
bash install-dependencies.sh
```

### "VLC se instala pero no funciona"

A veces VLC no se instala completamente. Intenta:

```bash
sudo apt-get remove vlc vlc-plugin-base
sudo apt-get install vlc vlc-plugin-base
```

## Ver logs de instalación

Si necesitas ver toda la salida del instalador (incluyendo errores):

```bash
bash -x install-dependencies.sh 2>&1 | tee install.log
```

Esto creará un archivo `install.log` con todos los detalles.

## Desinstalación

El instalador no modifica tu sistema de forma permanente. Para desinstalar:

```bash
# Solo elimina la carpeta del proyecto
rm -rf ~/MusicBell

# Si deseas desinstalar las dependencias del sistema:
sudo apt-get remove python3 pip3 vlc vlc-plugin-base
```

## Contacto

Si tienes problemas con el instalador, revisa:

- [INSTALACION.md](INSTALACION.md) - Instalación detallada
- [DEBUGGING_AUDIO.md](DEBUGGING_AUDIO.md) - Problemas de audio
- [FAQ.md](FAQ.md) - Preguntas frecuentes
