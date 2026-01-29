# Icono y Acceso Directo para MusicBell en Windows

## Configuración del Icono

Se ha incluido un **icono personalizado** para MusicBell que facilita el acceso a la aplicación en Windows.

### Ubicación de los archivos:

- `icon.ico` - Icono de la aplicación (256x256 píxeles)
- `crear_acceso_directo.bat` - Script para crear el acceso directo en el Escritorio
- `MusicBell.vbs` - Lanzador VBS (alternativa silenciosa)

## Cómo usar

### Opción 1: Crear Acceso Directo Automático (Recomendado)

1. **Haz clic derecho** en el archivo `crear_acceso_directo.bat`
2. Selecciona **"Ejecutar como administrador"**
3. Se creará un acceso directo en tu Escritorio llamado `MusicBell.lnk`

### Opción 2: Crear Acceso Directo Manual

1. Haz clic derecho en el Escritorio
2. Selecciona **Nuevo > Acceso directo**
3. Ingresa la ruta:
   ```
   C:\ruta\a\MusicBell\start_windows.bat
   ```
4. Dale el nombre: `MusicBell`
5. Haz clic derecho en el acceso directo
6. Selecciona **Propiedades**
7. En **Acceso directo > Icono**, haz clic en **Cambiar icono**
8. Navega a: `C:\ruta\a\MusicBell\icon.ico`

### Opción 3: Usar el Lanzador VBS Silencioso

- Haz doble clic en `MusicBell.vbs` para ejecutar la app sin ventana de comandos visible
- Puedes crear un acceso directo a este archivo con el icono

## Características del Icono

- **Diseño**: Nota musical dorada sobre fondo gradiente azul-púrpura
- **Tamaños**: Múltiples tamaños optimizados (256, 128, 64, 48, 32, 16 píxeles)
- **Compatible**: Windows 10, Windows 11, y versiones anteriores

## Solución de Problemas

**El icono no aparece en el acceso directo:**

- Asegúrate de estar ejecutando como administrador
- Verifica que `icon.ico` está en la carpeta raíz de MusicBell
- Intenta crear manualmente el acceso directo (Opción 2)

**El acceso directo no funciona:**

- Comprueba que Python está instalado y en PATH
- Asegúrate de haber ejecutado `install_requirements.bat` primero
- Intenta ejecutar `start_windows.bat` directamente para ver errores

## Regenerar el Icono

Si necesitas regenerar el icono, ejecuta:

```batch
python crear_icono.py
```

Esto creará un nuevo `icon.ico` con el diseño predeterminado.
