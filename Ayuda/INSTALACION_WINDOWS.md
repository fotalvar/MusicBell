# Instalación en Windows como Servicio

## Descripción

Este documento explica cómo instalar MusicBell como un servicio de Windows que se ejecute automáticamente al iniciar el sistema.

## Opción 1: Instalación Manual (Recomendado para pruebas)

### Requisitos
- Python 3.8+ instalado en Windows
- Terminal con permisos de administrador

### Pasos

1. **Descargar e instalar Python**
   - Descarga desde https://www.python.org/downloads/
   - **IMPORTANTE**: Marca "Add Python to PATH" durante la instalación
   - Verifica la instalación: Abre cmd y escribe `python --version`

2. **Instalar dependencias**
   ```cmd
   cd C:\ruta\a\MusicBell\backend
   pip install -r requirements.txt
   ```

3. **Copiar archivos MP3**
   - Copia tus canciones a `C:\ruta\a\MusicBell\canciones\`

4. **Ejecutar la aplicación**
   - Opción A: Doble clic en `start_windows.bat`
   - Opción B: Terminal:
     ```cmd
     cd C:\ruta\a\MusicBell
     python backend\app.py
     ```

5. **Acceder a la interfaz**
   - Abre http://localhost:5000 en tu navegador

## Opción 2: Instalar como Servicio de Windows

Para que MusicBell inicie automáticamente con Windows, necesitas convertirlo en un servicio.

### Requisitos
- Python 3.8+
- `pywin32` instalado
- Terminal con permisos de administrador

### Instalación

1. **Instalar herramientas necesarias**
   ```cmd
   pip install pywin32
   python -m pywin32_postinstall -install
   ```

2. **Crear script de servicio**
   
   Crea `C:\MusicBell\install_service.py`:
   
   ```python
   import win32serviceutil
   import win32service
   import win32event
   import servicemanager
   import socket
   import sys
   import os
   from pathlib import Path

   class MusicBellService(win32serviceutil.ServiceFramework):
       _svc_name_ = "MusicBellService"
       _svc_display_name_ = "MusicBell - Sistema de Música Escolar"
       _svc_description_ = "Reproductor automático de música para escuelas"

       def __init__(self, args):
           win32serviceutil.ServiceFramework.__init__(self, args)
           self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
           self.is_alive = True
           
           # Cambiar al directorio de la aplicación
           os.chdir(Path(__file__).parent)

       def SvcStop(self):
           self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
           win32event.SetEvent(self.hWaitStop)
           self.is_alive = False

       def SvcDoRun(self):
           servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                servicemanager.PYS_SYSTEM_EXIT,
                                (self._svc_name_, ''))
           
           # Ejecutar la aplicación Flask
           os.system('python backend\\app.py')

   if __name__ == '__main__':
       if len(sys.argv) == 1:
           servicemanager.Initialize()
           servicemanager.PrepareToHostSingleServiceUser(MusicBellService)
           servicemanager.StartServiceCtrlDispatcher()
       else:
           win32serviceutil.HandleCommandLine(MusicBellService)
   ```

3. **Instalar el servicio**
   ```cmd
   cd C:\MusicBell
   python install_service.py install
   ```

4. **Iniciar el servicio**
   ```cmd
   python install_service.py start
   ```

### Comandos útiles

```cmd
# Ver estado
python install_service.py status

# Detener
python install_service.py stop

# Eliminar servicio
python install_service.py remove

# Ver logs (en Visor de eventos de Windows)
# Abrir Event Viewer y buscar "MusicBell"
```

## Opción 3: Usar Scheduler de Windows

Una alternativa más simple es usar el Scheduler de Windows:

1. Abre "Programador de tareas"
2. Nueva tarea
3. General:
   - Nombre: "MusicBell"
   - Marcar "Ejecutar con los privilegios más altos"
4. Desencadenador:
   - "Al iniciar" o la hora que prefieras
5. Acción:
   - Programa: `C:\Python\python.exe` (tu ruta de Python)
   - Argumentos: `C:\MusicBell\backend\app.py`
   - Iniciar en: `C:\MusicBell\backend`
6. Aceptar

## Acceso Remoto

Una vez instalado, puedes acceder desde otros dispositivos en la red:

1. Obtén la IP de tu PC Windows:
   ```cmd
   ipconfig
   ```
   Busca "Dirección IPv4" (ej: 192.168.1.100)

2. Desde otro dispositivo, abre el navegador:
   ```
   http://192.168.1.100:5000
   ```

## Solución de Problemas

### El servicio no inicia
- Verifica que Python está en el PATH
- Revisa los logs en Visor de eventos
- Intenta con Opción 1 primero

### No se escucha sonido
- Verifica que los altavoces están conectados
- Prueba con un MP3 directamente en Windows

### Puerto 5000 en uso
- Edita `backend/app.py` y cambia el puerto:
  ```python
  app.run(host='0.0.0.0', port=8080, debug=False)
  ```

### Error de permisos
- Ejecuta cmd como administrador
- Verifica permisos en la carpeta de instalación

## Monitoreo

Para monitorear la aplicación:

1. **Logs**: Revisa `logs/musicbell.log`
2. **Estado**: Accede a http://localhost:5000/api/estado
3. **Task Manager**: Busca proceso Python

## Actualizar Windows desde Mac

Si estás desarrollando en Mac y necesitas actualizar en Windows:

1. Copia los cambios a una carpeta compartida o USB
2. En Windows, reemplaza los archivos
3. Detén y reinicia el servicio:
   ```cmd
   python backend\install_service.py stop
   python backend\install_service.py start
   ```

---

**Nota**: Para máxima confiabilidad, es recomendable usar la Opción 2 (Servicio) en producción, ya que Windows se encargará de reiniciar automáticamente la aplicación si falla.
