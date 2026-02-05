# Guía: Crear EXE de MusicBell para Windows

Esta guía te ayudará a crear un archivo EXE ejecutable de MusicBell con un icono personalizado.

## Opción 1: EXE Completo (Recomendado)

### Paso 1: Generar el EXE

1. Haz doble clic en **`generar_exe.bat`**
2. Espera a que se complete el proceso (puede tardar 2-5 minutos)
3. Se creará una carpeta `dist` con el archivo `MusicBell.exe`

### Paso 2: Crear Acceso Directo (Opcional)

Si ejecutaste `generar_exe.bat`:

1. Haz doble clic en **`crear_acceso_directo_exe.bat`**
2. Se creará un acceso directo en tu escritorio con icono
3. Ya puedes ejecutar MusicBell desde el escritorio

### Paso 3: Usar MusicBell

- **Opción A**: Doble clic en `dist/MusicBell.exe`
- **Opción B**: Doble clic en el acceso directo del escritorio

---

## Opción 2: Acceso Directo Simple (Rápido)

Si no quieres generar un EXE completo, puedes crear un acceso directo del script batch:

1. Haz clic derecho en **`start_windows.bat`**
2. Selecciona "Enviar a" > "Escritorio (crear acceso directo)"
3. El acceso directo aparecerá en tu escritorio
4. Renómbralo a "MusicBell" si lo deseas

---

## Solución de Problemas

### "PyInstaller no encontrado"

```bash
# En Windows, abre CMD y ejecuta:
pip install pyinstaller
```

### "El EXE no se ejecuta"

- Verifica que has ejecutado `pip install -r backend/requirements.txt` primero
- Comprueba que la carpeta `frontend`, `canciones`, `config` existen

### "El icono no se ve"

- Verifica que existe el archivo `icon.ico`
- Si no existe, ejecuta: `python crear_icono.py`

### Distribuir MusicBell a Otros

Si quieres compartir MusicBell con otros usuarios:

1. Copia la carpeta `dist/` (contiene `MusicBell.exe`)
2. Copia las carpetas `frontend/`, `canciones/`, `config/` junto a `MusicBell.exe`
3. Copia `icon.ico` también
4. Distribuye el acceso directo o el EXE

---

## Características del EXE

✓ Ejecutable sin necesidad de Python instalado  
✓ Icono personalizado de MusicBell  
✓ Interfaz de usuario amigable  
✓ Se ejecuta en modo ventana (no consola)  
✓ Incluye todas las dependencias necesarias

---

## ¿Necesitas ayuda?

Si tienes problemas, ejecuta primero:

```
diagnostico_windows.bat
```

Este script verificará que todo esté bien instalado antes de generar el EXE.
