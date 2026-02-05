# Instalación de MusicBell

## Requisitos previos

- **Python 3.8+** instalado
- **pip** (gestor de paquetes de Python)
- Navegador web moderno
- Canciones en formato MP3

## Instalación Rápida

### macOS y Linux

```bash
cd MusicBell
bash start.sh
```

### Windows

```bash
cd MusicBell
start_windows.bat
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

**Nota Windows**: Si `playsound` falla durante la instalación, asegúrate de tener:

- Python 3.8+
- Acceso a internet
- Ejecutar como administrador si es necesario

### 3. Agregar canciones

Copia tus archivos MP3 a la carpeta `canciones/`

### 4. Ejecutar la aplicación

#### Opción A: Script de inicio (Recomendado)

```bash
# macOS/Linux
bash start.sh

# Windows
start_windows.bat
```

#### Opción B: Comando directo

```bash
python backend/app.py
```

#### Opción C: Desde Python

```python
cd backend
python app.py
```

### 5. Acceder a la interfaz

Abre tu navegador en: **http://localhost:5000**

---

## Instalación como Servicio de Windows

Para que MusicBell inicie automáticamente con Windows:

### Opción 1: Programador de Tareas (Recomendado)

1. Abre "Programador de tareas"
2. Crear nueva tarea:
   - Nombre: `MusicBell`
   - Marcar "Ejecutar con los privilegios más altos"
3. Desencadenador: "Al iniciar"
4. Acción:
   - Programa: `C:\Python\python.exe` (tu Python)
   - Argumentos: `C:\MusicBell\backend\app.py`
   - Directorio: `C:\MusicBell`
5. Guardar

### Opción 2: Servicio de Windows (Avanzado)

Requiere `pywin32`:

```bash
pip install pywin32
python -m pywin32_postinstall -install
```

Luego crear un servicio personalizado (ver documentación de `pywin32`).

---

## Acceso Remoto desde la Red

1. Obtén la IP del servidor:
   - **Windows**: `ipconfig` → IPv4
   - **macOS/Linux**: `ifconfig` → inet

2. Desde otro dispositivo:
   ```
   http://192.168.1.100:5000
   ```

---

## Solución de Problemas

### No se escucha sonido

- Verifica volumen de Windows (no en silencio)
- Revisa logs: `logs/musicbell.log`
- Comprueba que los MP3 existen en `canciones/`
- Prueba reproducir un MP3 directamente en Windows

### Puerto 5000 en uso

```bash
# Edita backend/app.py
# Cambiar: app.run(host='0.0.0.0', port=8080, debug=False)
```

### Error: playsound no se instala

- Ejecuta como administrador en Windows
- Intenta: `python -m pip install --upgrade pip`
- Luego: `python -m pip install playsound==1.2.2`

### Error de permisos en macOS/Linux

```bash
chmod +x start.sh
bash start.sh
```

### Error: "Port already in use"

```bash
# Busca qué proceso está usando el puerto 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Detén el proceso o cambia de puerto
```

---

## Verificación de la instalación

```bash
# Verifica Python
python --version

# Verifica dependencias
cd backend
python -c "import flask; import flask_cors; print('Dependencias OK')"

# Verifica reproducción de audio
python -c "from playsound import playsound; print('Audio OK')"
```

---

## Actualizar dependencias

```bash
cd backend
pip install --upgrade -r requirements.txt
```

---

## Desinstalación

Simplemente elimina la carpeta `MusicBell`. No modifica el registro ni archivos del sistema.

---

**Nota**: Para producción, se recomienda usar la Opción 1 (Programador de Tareas) en Windows, ya que es más confiable y no requiere dependencias adicionales.
