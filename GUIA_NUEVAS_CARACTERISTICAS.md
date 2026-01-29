# 🎵 MusicBell v2.0 - Guía de Uso de Nuevas Características

## 📋 Contenido

1. [Interfaz Rediseñada](#interfaz-rediseñada)
2. [Acceso Remoto](#acceso-remoto)
3. [Versión Móvil](#versión-móvil)
4. [Cargar Música Remotamente](#cargar-música-remotamente)
5. [Panel de Estado](#panel-de-estado)

---

## 🎨 Interfaz Rediseñada

### Nuevo Diseño

La interfaz ha sido completamente rediseñada para ser más intuitiva y limpia:

#### **Barra de Navegación Principal**

```
┌─────────────────────────────────────────────────────────────┐
│ 🎵 MusicBell  │  Playlist  Archivado  Reproducción  Conflictos  │  Apagar │
└─────────────────────────────────────────────────────────────┘
```

- **Izquierda**: Logo y nombre de la app
- **Centro**: Opciones de navegación principales
- **Derecha**: Botón para apagar la aplicación

#### **Barra de Acciones Contextuales**

```
┌─────────────────────────────────────────────────────────────┐
│ Añadir Canción  │  Programación Rápida  │  Cargar Música  │
└─────────────────────────────────────────────────────────────┘
```

Los botones cambian según la pestaña activa:

- **Playlist**: Añadir, Programación, Cargar
- **Otras pestañas**: Información contextual

### Simplificación

- Se eliminaron títulos duplicados
- Diseño más limpio y organizado
- Mejor uso del espacio

---

## 🌐 Acceso Remoto

MusicBell ahora puede ser controlado desde cualquier dispositivo conectado a tu red.

### Cómo Acceder Remotamente

#### Paso 1: Obtener la dirección remota

1. Abre MusicBell normalmente
2. Busca el panel **"Estado"** en la esquina inferior derecha
3. Verás algo como:
   ```
   IP Local: 192.168.1.100
   Puerto: 5000
   Acceso Remoto: 192.168.1.100:5000
   ```

#### Paso 2: Copiar dirección

- Haz clic en el botón **"Copiar datos remoto"**
- Se copiará la dirección: `192.168.1.100:5000`

#### Paso 3: Acceder desde otro dispositivo

En otro ordenador o dispositivo móvil conectado a la misma red:

1. Abre un navegador web
2. Escribe en la barra de direcciones: `http://192.168.1.100:5000`
3. ¡Listo! Verás la app de MusicBell

### Características del Acceso Remoto

- ✅ Acceso desde cualquier dispositivo en la red
- ✅ Control completo de reproducción
- ✅ Gestión de canciones
- ✅ Carga de archivos
- ✅ Sin necesidad de instalar nada (solo navegador)

### Requisitos

- Ambos dispositivos en la **misma red** (WiFi o Ethernet)
- El ordenador con MusicBell debe estar **encendido**
- Firewall debe permitir la conexión (generalmente es automático en redes caseras)

---

## 📱 Versión Móvil

MusicBell es completamente **responsive** y funciona perfectamente en dispositivos móviles.

### Características Mobile

#### Adaptive Layout

- Interfaz se adapta automáticamente a cualquier tamaño
- Botones grandes y táctiles
- Scroll optimizado
- Lecturable sin zoom

#### Dispositivos Soportados

- 📱 Smartphones (iPhone, Android)
- 📱 Tablets (iPad, Samsung Tab, etc.)
- 💻 Laptops
- 🖥️ Ordenadores de escritorio

#### Cómo Usar en Móvil

**Desde el mismo dispositivo:**

1. En el navegador móvil, accede a: `http://localhost:5000`

**Desde otro móvil (en la red):**

1. Copia la dirección remota desde el panel de Estado
2. En tu móvil, abre el navegador
3. Pega la dirección remota

### Breakpoints Optimizados

- **Desktop** (>1024px): Vista completa con todas las opciones
- **Tablet** (768px-1023px): Interfaz optimizada para pantallas medianas
- **Móvil** (480px-767px): Interfaz táctil compacta
- **Extra pequeño** (<480px): Optimizado para pantallas muy pequeñas

---

## 📤 Cargar Música Remotamente

Puedes agregar archivos de música directamente desde cualquier dispositivo.

### Cómo Cargar Archivos

#### Paso 1: Ir a la sección de carga

1. Haz clic en la pestaña **"Playlist"**
2. Busca el botón **"Cargar Música"** en la barra de acciones
3. Se abrirá un modal de carga

#### Paso 2: Seleccionar archivos

Hay dos formas de seleccionar archivos:

**Opción A: Arrastra y suelta (Drag & Drop)**

```
┌─────────────────────────────────────────────┐
│  📁 Arrastra archivos aquí                  │
│     o haz clic para seleccionar             │
└─────────────────────────────────────────────┘
```

- Arrastra archivos MP3 directamente
- Se subirán automáticamente

**Opción B: Seleccionar manualmente**

- Haz clic en el área de carga
- Se abrirá el explorador de archivos
- Selecciona tus archivos MP3

#### Paso 3: Ver progreso

- Una barra de progreso muestra el estado de carga
- Se mostrará el número de archivos subidos

#### Paso 4: Finalizar

- Los archivos se cargarán a la carpeta de canciones
- Aparecerán automáticamente en tu playlist
- Cierra el modal

### Requisitos

- ✅ Solo archivos **MP3**
- ✅ Máximo **500 MB** por archivo
- ✅ Conexión a Internet (para access remoto)

### Ejemplo

```
📁 Mis Canciones
  ├─ Canción1.mp3 (3.5 MB) ✅
  ├─ Canción2.mp3 (4.2 MB) ✅
  └─ Canción3.mp3 (2.8 MB) ✅
```

---

## 📊 Panel de Estado

El panel de estado te muestra información en tiempo real.

### Ubicación

Esquina **inferior derecha** de la pantalla, siempre visible.

### Información Mostrada

```
┌─────────────────┐
│ Estado       ⌀  │  (⌀ = Minimizar)
├─────────────────┤
│ Reproduciendo: Parado
│ IP Local: 192.168.1.100
│ Puerto: 5000
│ Acceso Remoto: 192.168.1.100:5000
│ [Copiar datos remoto]
│ [STOP]
└─────────────────┘
```

### Funciones

#### Estado de Reproducción

- Muestra qué canción se está reproduciendo
- Se actualiza automáticamente

#### IP Local

- Tu dirección IP en la red

#### Puerto

- Puerto del servidor

#### Acceso Remoto

- Dirección completa para acceder remotamente

#### Botones

**"Copiar datos remoto"**

- Copia la dirección: `IP:PUERTO`
- Pega fácilmente en otro dispositivo

**"STOP"**

- Detiene la reproducción actual
- Útil para pausar música rápidamente

### Minimizar/Maximizar

- Haz clic en el botón **⌀** para minimizar
- Se convertirá en un pequeño botón
- Haz clic nuevamente para maximizar

---

## ⚙️ Configuración de Firewall

Si tienes problemas de acceso remoto, puede ser por el firewall.

### Windows

1. Panel de Control → Firewall de Windows
2. Permitir una aplicación a través del firewall
3. Busca Python o MusicBell
4. Marca ambas opciones (Privada y Pública)

### macOS

```bash
# Permitir puerto en firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw -k allow 5000
```

### Linux

```bash
# UFW (si está activo)
sudo ufw allow 5000/tcp
```

---

## 🐛 Solución de Problemas

### No puedo acceder remotamente

1. ✅ Verifica que ambos dispositivos estén en la misma red
2. ✅ Revisa que MusicBell esté ejecutándose
3. ✅ Comprueba la IP en el panel de Estado
4. ✅ Intenta desactivar el firewall temporalmente

### La carga de archivos es lenta

- Los archivos grandes tardan más
- Mejora la conexión WiFi si es posible
- Comprime los archivos si es necesario

### El móvil no se ve bien

- Recarga la página (F5 o Cmd+R)
- Gira el dispositivo
- Cierra y reabre el navegador

### El panel de Estado no aparece

- Baja la página (scroll down)
- Puede estar minimizado
- Recarga la página

---

## 💡 Tips y Trucos

### Acceso Rápido

1. Guarda la dirección remota en favoritos
2. Acceso instantáneo desde cualquier dispositivo

### En Clase

1. Comparte la dirección con los estudiantes
2. Ellos pueden ver el estado desde sus dispositivos
3. Perfecto para enseñanza

### Múltiples Dispositivos

- La app funciona en múltiples navegadores simultáneamente
- Todos ven los mismos cambios en tiempo real
- Ideal para sincronización

### Protección

- Usa la app en redes locales de confianza
- No expongas el puerto a Internet público
- Para acceso remoto seguro, usa VPN

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs en `logs/`
2. Verifica que Python 3 esté instalado
3. Confirma que Flask y dependencias están instaladas:
   ```bash
   pip install -r backend/requirements.txt
   ```

---

**Versión**: 2.0  
**Última actualización**: Enero 29, 2026  
**Estado**: Producción
