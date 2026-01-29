# 🎯 Guía Visual - Navegación por Tabs

## Estructura de la Interfaz

```
╔════════════════════════════════════════════════════════════╗
║  🎵 MusicBell                                               ║
║  Sistema de reproducción de música automático para escuelas║
╠════════════════════════════════════════════════════════════╣
║ [📊 Estado] [➕ Agregar] [⚡ Rápida] [🎵 Canciones] [⚠️ Conflictos] ║
╠════════════════════════════════════════════════════════════╣
║                                                             ║
║  ┌─ TAB CONTENIDO (Dinámico) ──────────────────────────┐  ║
║  │                                                      │  ║
║  │  Solo se muestra un tab a la vez                     │  ║
║  │  Las transiciones son suaves (fade in)              │  ║
║  │  Responsive en todos los dispositivos                │  ║
║  │                                                      │  ║
║  └──────────────────────────────────────────────────────┘  ║
║                                                             ║
╠════════════════════════════════════════════════════════════╣
║  © 2026 MusicBell - Sistema de reproducción automática    ║
╚════════════════════════════════════════════════════════════╝
```

---

## 📊 Tab 1: Estado Actual

**Muestra la información en tiempo real:**

```
┌─────────────────────────────────────┐
│ Estado Actual                       │
├─────────────────────────────────────┤
│ 🎵 Ahora Sonando:                  │
│    Himno Nacional                   │
│    08:00 - Todos los días           │
│                                     │
│ ⏭️  Próximas Canciones:              │
│    • Marcha de Zacatecas (09:30)    │
│    • Canción K-Pop (11:00)          │
│    • Música de Descanso (14:00)     │
│                                     │
│ 🕒 Hora del Servidor: 08:32:15     │
└─────────────────────────────────────┘
```

**Se actualiza automáticamente cada 5 segundos**

---

## ➕ Tab 2: Agregar Canción

**Formulario para agregar canciones manualmente:**

```
┌─────────────────────────────────────┐
│ Añadir Nueva Canción                │
├─────────────────────────────────────┤
│                                     │
│ Nombre: [____________]              │
│                                     │
│ Archivo MP3:                        │
│ ▼ [Selecciona un archivo ▼]         │
│   • Himno Nacional.mp3              │
│   • Marcha Zacatecas.mp3            │
│   • Canción K-Pop.mp3               │
│                                     │
│ Tipo de Planificación:              │
│ ▼ [Hora diaria ▼]                   │
│   • Hora diaria                     │
│   • Fecha específica                │
│   • Días de la semana               │
│                                     │
│ Hora: [08:00]                       │
│                                     │
│ [Agregar Canción]                   │
│                                     │
└─────────────────────────────────────┘
```

**Los campos cambian según el tipo seleccionado**

---

## ⚡ Tab 3: Programación Rápida

**Generador automático de programación:**

```
┌─────────────────────────────────────────────┐
│ ⚡ Programación Rápida                       │
├─────────────────────────────────────────────┤
│                                             │
│ ℹ️ Selecciona un rango de fechas, una hora  │
│    y deja que el sistema programe            │
│    canciones automáticamente                 │
│                                             │
│ [Programar Canciones]                       │
│                                             │
│ Usa el botón de arriba para crear            │
│ una nueva programación rápida                │
│                                             │
└─────────────────────────────────────────────┘
```

### Cuando haces clic en "Programar Canciones":

```
╔═════════════════════════════════════╗
║ ⚡ Programación Rápida              ║
╠═════════════════════════════════════╣
║                                     ║
║ Fecha de Inicio: [2025-02-01]       ║
║                                     ║
║ Fecha de Fin: [2025-02-07]          ║
║                                     ║
║ Hora de Reproducción: [08:00]       ║
║                                     ║
║ ☐ Incluir fines de semana           ║
║                                     ║
╠─ Resumen ───────────────────────────╣
║ 📅 5 día(s) × 🎵 2 canción(es)      ║
║ disponibles (se reciclará)          ║
║                                     ║
║ 📋 Canciones disponibles:           ║
║ • Himno Nacional                    ║
║ • Marcha de Zacatecas               ║
║                                     ║
╠═════════════════════════════════════╣
║ [Generar Programación] [Cancelar]   ║
╚═════════════════════════════════════╝
```

**El resumen se actualiza automáticamente al cambiar fechas**

---

## 🎵 Tab 4: Mis Canciones

**Lista de todas las canciones programadas:**

```
┌─────────────────────────────────────────────────┐
│ Canciones Programadas                           │
├─────────────────────────────────────────────────┤
│                                                 │
│ ┌─ Himno Nacional ─────────────────────────┐   │
│ │ 🎵 himno.mp3                               │   │
│ │ ⏰ Hora diaria: [08:00] 📝                │   │
│ │ 📅 Todos los días                         │   │
│ │ ✓ Habilitada                              │   │
│ │ [Editar] [Eliminar]                       │   │
│ └─────────────────────────────────────────────┘  │
│                                                 │
│ ┌─ Marcha de Zacatecas ────────────────────┐   │
│ │ 🎵 marcha.mp3                             │   │
│ │ ⏰ Días de la semana: [09:30] 📝          │   │
│ │ 📅 Lunes, Miércoles, Viernes              │   │
│ │ ✓ Habilitada                              │   │
│ │ [Editar] [Eliminar]                       │   │
│ └─────────────────────────────────────────────┘  │
│                                                 │
│ ┌─ Evento Especial ─────────────────────────┐   │
│ │ 🎵 especial.mp3                           │   │
│ │ ⏰ Fecha específica: [2025-02-14] [14:30] 📝 │
│ │ 📅 Viernes 14 de febrero de 2025          │   │
│ │ ✓ Habilitada                              │   │
│ │ [Editar] [Eliminar]                       │   │
│ └─────────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Puedes hacer clic en los campos para editarlos rápidamente**

---

## ⚠️ Tab 5: Conflictos

**Detector automático de conflictos de horarios:**

```
┌─────────────────────────────────────┐
│ ⚠️ Conflictos de Horario             │
├─────────────────────────────────────┤
│ ℹ️ Verifica si hay múltiples         │
│    canciones programadas para sonar  │
│    al mismo tiempo                   │
│                                     │
│ [Verificar Conflictos]              │
│                                     │
└─────────────────────────────────────┘
```

### Cuando se detectan conflictos:

```
┌─────────────────────────────────────────┐
│ ⚠️ Conflictos de Horario                 │
├─────────────────────────────────────────┤
│                                         │
│ ⚠️ Se encontraron 2 conflictos           │
│                                         │
│ 🔴 Viernes 14-02-2025 a las 14:00       │
│    • Himno Nacional                     │
│    • Evento Especial                    │
│    Acción: Editar una de estas          │
│                                         │
│ 🔴 Lunes 17-02-2025 a las 09:30         │
│    • Marcha de Zacatecas                │
│    • Programación Rápida #1             │
│    Acción: Editar una de estas          │
│                                         │
│ [Verificar Conflictos]                  │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎨 Colores y Estilos

### Colores de los Tabs

| Elemento | Color | Hex |
|----------|-------|-----|
| Primario (Activo) | Índigo | #6366f1 |
| Secundario | Púrpura | #8b5cf6 |
| Éxito | Verde | #10b981 |
| Advertencia | Naranja | #f59e0b |
| Peligro | Rojo | #ef4444 |
| Fondo Claro | Gris Claro | #f3f4f6 |
| Borde | Gris | #e5e7eb |

### Estados de los Botones

```
[Inactivo] ← Tab deshabilitado (gris)
[Hover]    ← Al pasar el mouse (tono azul ligero)
[ACTIVO]   ← Tab seleccionado (azul con subrayado)
```

---

## ⌨️ Atajos de Teclado (Futuros)

*Próximas versiones incluirán:*
- `Ctrl+1` - Ir a Tab Estado
- `Ctrl+2` - Ir a Tab Agregar
- `Ctrl+3` - Ir a Tab Programación Rápida
- `Ctrl+4` - Ir a Tab Canciones
- `Ctrl+5` - Ir a Tab Conflictos

---

## 📱 Responsividad Móvil

La interfaz se adapta automáticamente:

```
DESKTOP (1200px+)
┌──────────────────────────┐
│ [Tab1] [Tab2] [Tab3] ... │
├──────────────────────────┤
│ Contenido ancho          │
└──────────────────────────┘

TABLET (768px-1200px)
┌──────────────────┐
│ [Tab1] [Tab2] ... │
├──────────────────┤
│ Contenido medio  │
└──────────────────┘

MÓVIL (< 768px)
┌────────────────┐
│ [Tab1] [Más ▼] │
├────────────────┤
│ Contenido      │
│ completo       │
└────────────────┘
```

---

## 🔄 Flujo de Trabajo Típico

### 1️⃣ Primer Uso - Agregar Canciones
```
[➕ Agregar Canción] → [Completar formulario] → [Agregar]
```

### 2️⃣ Programar Automáticamente
```
[⚡ Programación Rápida] → [Programar Canciones] → [Seleccionar fechas] → [Generar]
```

### 3️⃣ Monitorear
```
[📊 Estado] → [Ver estado actual] ↻ [Se actualiza cada 5s]
```

### 4️⃣ Revisar Conflictos (Si es necesario)
```
[⚠️ Conflictos] → [Verificar] → [Editar si hay] → [📊 Estado]
```

### 5️⃣ Gestionar (Opcionales)
```
[🎵 Mis Canciones] → [Ver lista] → [Editar/Eliminar]
```

---

## 💡 Tips y Trucos

✅ **Mejor para grandes volúmenes:** Usar la Programación Rápida
✅ **Control fino:** Usar Agregar Canción manual
✅ **Evitar conflictos:** Usar Tab Conflictos regularmente
✅ **Verificar estado:** Tab Estado se actualiza automáticamente
✅ **Monitoreo:** Dejar pestaña abierta durante el día

---

## 🎓 Ejemplo Completo - Semana Escolar

**Objetivo:** Programar música automática para una semana escolar

### Paso 1: Agregar Canciones Base
```
Tab [➕ Agregar Canción]
- Himno Nacional (Hora diaria: 08:00)
- Música de Descanso (Dias de semana: Lunes-Viernes, 11:00)
- Himno de Salida (Hora diaria: 16:00)
```

### Paso 2: Programación Especial
```
Tab [⚡ Programación Rápida]
- Rango: 17-21 de febrero 2025
- Hora: 13:30 (después del almuerzo)
- Sin fines de semana
- Canción: "Música Relajante"
```

### Paso 3: Verificar
```
Tab [⚠️ Conflictos]
- Ejecutar verificación
- Resolver cualquier conflicto
```

### Paso 4: Monitorear
```
Tab [📊 Estado]
- Verificar que está sonando correctamente
- Se actualiza automáticamente
```

---

## 📞 ¿Problemas?

Si algo no funciona:
1. Recargar página: `Ctrl+R` o `Cmd+R`
2. Abrir consola: `F12` → Pestaña "Console"
3. Revisar logs en servidor
4. Verificar que el servidor está corriendo en puerto 5000

**¡Listo! 🎉 Ya puedes empezar a usar MusicBell con tabs.**
