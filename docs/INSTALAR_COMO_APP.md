# Instalar MusicBell como App (PWA)

MusicBell es una **Progressive Web App (PWA)**, lo que permite instalarla como aplicación nativa en macOS, Linux y navegadores web.

## ✅ Requisitos

- Navegador moderno (Chrome, Firefox, Safari, Edge)
- MusicBell ejecutándose en `http://localhost:5000`

## 📱 Instalación en el Navegador

### Método 1: Desde el ícono de instalación (Recomendado)

1. **Abre MusicBell en tu navegador**: `http://localhost:5000`
2. **Busca el ícono de instalación** en la barra de direcciones:
   - Lado derecho de la barra de direcciones
   - Es un **ícono pequeño de descarga/instalación**
3. **Haz clic** en el ícono
4. **Selecciona "Instalar"** en el popup
5. ¡Listo! La app aparecerá en tu menú o dock

### Método 2: Desde el menú

1. **Abre el navegador**
2. **Accede a**: `http://localhost:5000`
3. **Haz clic en el menú** (⋮ o ≡) en la esquina superior derecha
4. **Selecciona**: `Instalar MusicBell` (si está disponible)
5. **Confirma la instalación**

### Método 3: Crear acceso directo

Si el método 1 no funciona:

1. **Abre MusicBell en tu navegador**: `http://localhost:5000`
2. **Menú** → **Más herramientas** → **Crear acceso directo**
3. Marca: "Abrir como ventana" (importante)
4. **Crear**

---

## 🎯 Características de la App Instalada

✅ **Icono personalizado** - Cara sonriente con fondo indigo  
✅ **Sin barras del navegador** - Se ve como una aplicación nativa  
✅ **Acceso directo** - En el menú de aplicaciones o dock  
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

Desde el menú de la app:

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

## 🍎 En macOS

Una vez instalada:

1. **Aparecerá en el Dock** - Puedes anclarla permanentemente
2. **Abierta desde Spotlight** - Busca "MusicBell" en Spotlight
3. **Acceso rápido** - Está con tus aplicaciones normales

---

## 🐧 En Linux

Una vez instalada:

1. **Aparecerá en el menú de aplicaciones**
2. **Acceso directo en el escritorio** (opcional)
3. **Se integra con el gestor de ventanas**

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
**Plataformas**: macOS, Linux
