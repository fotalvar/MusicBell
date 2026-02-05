# Instalación de MusicBell

## Requisitos previos

- **Python 3.8+** instalado
- **pip** (gestor de paquetes de Python)
- Navegador web moderno
- Canciones en formato MP3

## Instalación Rápida

```bash
cd MusicBell
bash start.sh
```

Luego abre: **http://localhost:5000**

---

## Instalación Detallada

### 1. Descargar el proyecto

```bash
git clone <repositorio>
cd MusicBell
```

### 2. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Agregar canciones

Copia tus archivos MP3 a la carpeta `canciones/`

### 4. Ejecutar la aplicación

#### Opción A: Script de inicio (Recomendado)

```bash
bash start.sh
```

#### Opción B: Comando directo

```bash
python backend/app.py
```

### 5. Acceder a la interfaz

Abre tu navegador en: **http://localhost:5000**

---

## Instalación como Servicio en Linux

Para que MusicBell inicie automáticamente:

### Usando systemd (Recomendado)

1. Crea un archivo `/etc/systemd/system/musicbell.service`:

```ini
[Unit]
Description=MusicBell - Automatic Music Player
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/home/tu_usuario/MusicBell
ExecStart=/usr/bin/python3 /home/tu_usuario/MusicBell/backend/app.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Habilita el servicio:

```bash
sudo systemctl enable musicbell
sudo systemctl start musicbell
```

3. Verifica el estado:

```bash
sudo systemctl status musicbell
```

---

## Instalación como Servicio en macOS

Para que MusicBell inicie automáticamente:

### Usando LaunchAgent

1. Crea `~/Library/LaunchAgents/com.musicbell.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.musicbell</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/tu_usuario/MusicBell/backend/app.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/tu_usuario/MusicBell</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

2. Carga el servicio:

```bash
launchctl load ~/Library/LaunchAgents/com.musicbell.plist
launchctl start com.musicbell
```

---

## Acceso Remoto desde la Red

1. Obtén la IP del servidor:

```bash
ifconfig | grep inet
```

2. Desde otro dispositivo en la red local:

```
http://192.168.1.100:5000
```

---

## Solución de Problemas

### No se escucha sonido

- Verifica volumen del sistema (no en silencio)
- Revisa logs: `logs/musicbell.log`
- Comprueba que los MP3 existen en `canciones/`

### Puerto 5000 en uso

```bash
lsof -i :5000
# Cambia a otro puerto en backend/app.py
```

### Error: python-vlc no se instala

```bash
# Instala VLC Media Player primero desde videolan.org
python -m pip install --upgrade pip
python -m pip install python-vlc==3.0.20123
```

### Error de permisos

```bash
chmod -R 755 canciones/
chmod +x start.sh
```

---

## Verificación de la instalación

```bash
# Verifica Python
python3 --version

# Verifica dependencias
cd backend
python3 -c "import flask; import flask_cors; import vlc; print('✓ OK')"
```

---

## Actualizar dependencias

```bash
cd backend
pip install --upgrade -r requirements.txt
```

---

## Desinstalación

Simplemente elimina la carpeta `MusicBell`.

---

**Nota**: Para producción, se recomienda usar systemd (Linux) o LaunchAgent (macOS).
