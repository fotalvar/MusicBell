# 🎨 Paleta de Colores - MusicBell 2025

## Colores Principales (Flat Design)

### Azul Primario
```
Color: #5B6DFF
HSL: 231° 100% 63%
RGB: 91 109 255
Uso: Botones principales, links, headers, accents
```

### Azul Primario Light
```
Color: #E8EBFF
HSL: 231° 100% 93%
RGB: 232 235 255
Uso: Fondos de hover, highlights
```

### Rojo/Coral
```
Color: #FF6B6B
HSL: 0° 100% 74%
RGB: 255 107 107
Uso: Botones peligrosos, advertencias, stop
```

### Rojo/Coral Light
```
Color: #FFE8E8
HSL: 0° 100% 93%
RGB: 255 232 232
Uso: Fondos de error, backgrounds
```

### Verde Mint
```
Color: #51CF66
HSL: 131° 61% 60%
RGB: 81 207 102
Uso: Acciones positivas, éxito, reproducción
```

### Verde Light
```
Color: #D3F9D8
HSL: 131° 71% 87%
RGB: 211 249 216
Uso: Fondos de éxito
```

### Amarillo/Miel
```
Color: #FFD43B
HSL: 45° 100% 67%
RGB: 255 212 59
Uso: Advertencias, botones secundarios
```

### Amarillo Light
```
Color: #FFF3BF
HSL: 45° 100% 88%
RGB: 255 243 191
Uso: Fondos de advertencia
```

### Cian/Azul Claro
```
Color: #74C0FC
HSL: 207° 89% 70%
RGB: 116 192 252
Uso: Información, detalles
```

### Cian Light
```
Color: #D0EBFF
HSL: 207° 100% 88%
RGB: 208 235 255
Uso: Fondos de información
```

---

## Escala de Grises

### Gray 50 (Fondos claros)
```
Color: #F9FAFB
Uso: Fondo de secciones, contenedores claros
```

### Gray 100 (Fondos)
```
Color: #F3F4F6
Uso: Fondos alternos, hover suave
```

### Gray 200 (Bordes)
```
Color: #E5E7EB
Uso: Bordes, divisores, separadores
```

### Gray 400 (Texto secundario)
```
Color: #9CA3AF
Uso: Texto deshabilitado, hints
```

### Gray 600 (Texto secundario)
```
Color: #4B5563
Uso: Descripciones, text-light
```

### Gray 800 (Texto principal)
```
Color: #1F2937
Uso: Encabezados, texto principal
```

### Blanco
```
Color: #FFFFFF
Uso: Fondo principal, inputs, containers
```

---

## Gradientes Implementados

### Header Gradient
```
linear-gradient(135deg, #5B6DFF 0%, #7C3AED 100%)
Azul vibrante → Púrpura
```

### Background Body Gradient
```
linear-gradient(135deg, #F8F9FF 0%, #F0F4FF 100%)
Azul muy claro → Violeta muy claro
```

### Botón Primario
```
linear-gradient(135deg, #5B6DFF 0%, #7C3AED 100%)
```

### Botón Danger
```
linear-gradient(135deg, #FF6B6B 0%, #FF5252 100%)
```

### Botón Success
```
linear-gradient(135deg, #51CF66 0%, #40C057 100%)
```

### Botón Warning
```
linear-gradient(135deg, #FF8C42 0%, #FF6B35 100%)
```

---

## Ejemplos de Uso

### Botón Primario
```html
<button class="btn-agregar">
  <svg>...</svg>
  Agregar Canción
</button>
```
**Fondo**: Gradient Azul-Púrpura
**Texto**: Blanco
**Hover**: Sombra azul, move up

### Botón Danger/Stop
```html
<button class="btn-stop">
  <svg>...</svg>
  STOP
</button>
```
**Fondo**: Gradient Rojo
**Texto**: Blanco
**Hover**: Sombra roja

### Input Focus
```css
border-color: #5B6DFF;
box-shadow: 0 0 0 4px #E8EBFF;
```

### Tab Active
```css
color: #5B6DFF;
border-bottom-color: #5B6DFF;
```

### Table Header
```css
background: linear-gradient(135deg, #5B6DFF, #7C3AED);
color: #FFFFFF;
```

### Success Badge
```css
background: #D3F9D8;
color: #2B8A3E;
```

### Warning Alert
```css
background: #FFF3BF;
border-left: 4px solid #FFD43B;
color: #664D03;
```

---

## Accessibility (A11y)

- ✅ Contraste suficiente en textos
- ✅ Colores no solo para transmitir información
- ✅ Estados hover y focus claros
- ✅ Iconos + texto en botones
- ✅ Bordes visibles en inputs

---

**Paleta diseñada para**: Interfaz moderna, limpia y profesional
**Inspiración**: Flat Design + Material Design
**Año**: 2025
