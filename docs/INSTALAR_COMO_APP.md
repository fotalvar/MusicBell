# Instalar MusicBell como App en Windows

MusicBell ahora es una **Progressive Web App (PWA)**, lo que permite instalarla como aplicación nativa en Windows a través de Chrome.

## ✅ Requisitos

- Google Chrome (versión 88+) en Windows
- MusicBell ejecutándose en `http://localhost:5000`

## 📱 Instalación en Chrome

### Método 1: Desde el ícono de instalación

1. **Abre MusicBell en Chrome**: `http://localhost:5000`
2. **Busca el ícono de instalación** en la barra de direcciones:
   - Lado derecho de la barra de direcciones
   - Es un **ícono pequeño de descarga**
3. **Haz clic** en el ícono
4. **Selecciona "Instalar"** en el popup
5. ¡Listo! La app aparecerá en tu menú de inicio y en el escritorio

### Método 2: Desde el menú

1. **Abre Chrome**
2. **Accede a**: `http://localhost:5000`
3. **Haz clic en el menú** (⋮) en la esquina superior derecha
4. **Selecciona**: `Instalar MusicBell` (si está disponible)
5. **Confirma la instalación**

### Método 3: Crear acceso directo

Si el método 1 no funciona:

1. **Abre MusicBell en Chrome**: `http://localhost:5000`
2. **Menú de Chrome** (⋮) → **Más herramientas** → **Crear acceso directo**
3. Marca: "Abrir como ventana" (importante)
4. **Crear**

---

## 🎯 Características de la App Instalada

✅ **Icono personalizado** - Cara sonriente con fondo indigo  
✅ **Sin barras del navegador** - Se ve como una aplicación nativa  
✅ **Acceso directo** - En Inicio y Escritorio  
✅ **Modo offline mejorado** - Funciona sin conexión parcialmente  
✅ **Sincronización** - Se sincroniza cuando vuelve la conexión  
✅ **Notificaciones** - Futura funcionalidad

---

## 🚀 Comportamiento de la App

### Pantalla de inicio

- **Ícono**: Cara sonriente amarilla con fondo indigo
- **Nombre**: MusicBell
- **Descripción**: Sistema automático de reproducción de música

### Accesos rápidos

Desde el menú de la app (botón derecho):

- **Reproducir canción** - Acceso directo a la pestaña de reproducción
- **Ver programación** - Acceso rápido a la playlist

### Modo offline

- Muchas funciones funcionan sin conexión
- Se sincroniza automáticamente cuando vuelve la conexión
- Los datos se cachean para carga rápida

---

## ⚙️ Configuración de la PWA

Los siguientes archivos configuran la app:

- **`manifest.json`** - Información de la app (nombre, iconos, etc.)
- **`service-worker.js`** - Caché y funcionalidad offline
- **`frontend/images/`** - Iconos en diferentes tamaños

---

## 🖥️ En Windows

Una vez instalada:

1. **Ícono en el Escritorio** - Abre la app directamente
2. **En el Menú de Inicio** - Busca "MusicBell"
3. **Anclar en la Barra de Tareas** - Click derecho → Anclar a barra de tareas
4. **Gestos táctiles** - Si tienes pantalla táctil

---

## 📲 Ventajas de PWA vs App Tradicional

| Aspecto              | PWA          | App Tradicional     |
| -------------------- | ------------ | ------------------- |
| **Tamaño**           | ~100 KB      | 50+ MB              |
| **Instalación**      | 1 clic       | App Store/Microsoft |
| **Actualizaciones**  | Automáticas  | Manual              |
| **Funciona offline** | Parcialmente | Sí                  |
| **Acceso**           | Web + App    | App                 |

---

## 🐛 Solución de Problemas

### No aparece ícono de instalación

- Asegúrate que Chrome está ejecutando MusicBell en `http://localhost:5000`
- Chrome necesita conexión HTTPS para PWA en producción (HTTP funciona en localhost)
- Recarga la página con `Ctrl+F5`

### La app no abre correctamente

- Comprueba que el backend (MusicBell) está ejecutándose
- Cierra y vuelve a abrir la app instalada

### Desinstalar la app

1. **Haz clic derecho** en el ícono de la app
2. **Selecciona**: "Desinstalar"
3. O desde Chrome: **Menú** → **Más herramientas** → **Crear acceso directo** → (verás opción de desinstalar)

---

## 💡 Próximas mejoras

- [ ] Notificaciones push
- [ ] Sincronización en background
- [ ] Soporte para compartir archivos
- [ ] Interfaz adaptada para móvil
- [ ] Modo oscuro nativo

---

**Tecnología**: Progressive Web App (PWA)  
**Navegadores soportados**: Chrome 88+, Edge 88+, Opera 74+  
**Plataformas**: Windows 10+, macOS, Linux
