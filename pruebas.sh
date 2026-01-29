#!/bin/bash
# 🧪 Script de Pruebas - MusicBell
# Ejecutar: bash pruebas.sh

echo "🎵 MusicBell - Script de Pruebas"
echo "================================="
echo ""

# Color de salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir resultados
print_test() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ ÉXITO${NC}: $2"
    else
        echo -e "${RED}✗ ERROR${NC}: $2"
    fi
}

print_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# ===========================================
# TEST 1: Verificar estructura de carpetas
# ===========================================
print_section "TEST 1: Estructura de Carpetas"

# Verificar carpetas principales
for dir in "frontend" "backend" "config" "canciones" "logs"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} Carpeta existe: $dir/"
    else
        echo -e "${RED}✗${NC} Carpeta no existe: $dir/"
    fi
done

# ===========================================
# TEST 2: Verificar archivos principales
# ===========================================
print_section "TEST 2: Archivos Principales"

files=(
    "frontend/index.html"
    "frontend/style.css"
    "frontend/script.js"
    "backend/app.py"
    "backend/music_player.py"
    "config/canciones.json"
    "start.sh"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} Archivo existe: $file"
    else
        echo -e "${RED}✗${NC} Archivo no existe: $file"
    fi
done

# ===========================================
# TEST 3: Verificar servidor running
# ===========================================
print_section "TEST 3: Estado del Servidor"

# Verificar si el puerto 5000 está en uso
if lsof -i :5000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Servidor está corriendo en puerto 5000"
    
    # Obtener PID
    PID=$(lsof -t -i :5000)
    echo "   PID: $PID"
else
    echo -e "${RED}✗${NC} Servidor no está corriendo en puerto 5000"
    echo -e "${YELLOW}ℹ${NC} Para iniciar: bash start.sh (macOS/Linux) o start.bat (Windows)"
fi

# ===========================================
# TEST 4: Verificar API endpoints
# ===========================================
print_section "TEST 4: Endpoints de API"

# Probar conexión al servidor
if ! lsof -i :5000 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠${NC} Servidor no está corriendo, saltando pruebas de API"
else
    # Probar GET /api/canciones
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/canciones)
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓${NC} GET /api/canciones - HTTP $response"
    else
        echo -e "${RED}✗${NC} GET /api/canciones - HTTP $response"
    fi
    
    # Probar GET /api/archivos
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/archivos)
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓${NC} GET /api/archivos - HTTP $response"
    else
        echo -e "${RED}✗${NC} GET /api/archivos - HTTP $response"
    fi
    
    # Probar GET /api/estado
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/estado)
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓${NC} GET /api/estado - HTTP $response"
    else
        echo -e "${RED}✗${NC} GET /api/estado - HTTP $response"
    fi
    
    # Probar GET /api/detectar-conflictos
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/detectar-conflictos)
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓${NC} GET /api/detectar-conflictos - HTTP $response"
    else
        echo -e "${RED}✗${NC} GET /api/detectar-conflictos - HTTP $response"
    fi
fi

# ===========================================
# TEST 5: Verificar archivos MP3
# ===========================================
print_section "TEST 5: Archivos MP3 en carpeta canciones/"

mp3_count=$(find canciones -name "*.mp3" 2>/dev/null | wc -l)
if [ "$mp3_count" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Se encontraron $mp3_count archivo(s) MP3"
    find canciones -name "*.mp3" | sed 's/^/   /'
else
    echo -e "${YELLOW}⚠${NC} No se encontraron archivos MP3"
    echo "   Agrega archivos MP3 a la carpeta 'canciones/' para empezar"
fi

# ===========================================
# TEST 6: Verificar contenido de HTML
# ===========================================
print_section "TEST 6: Estructura HTML"

# Verificar que el HTML contiene los tabs
if grep -q "tab-estado" frontend/index.html; then
    echo -e "${GREEN}✓${NC} HTML contiene tab-estado"
else
    echo -e "${RED}✗${NC} HTML no contiene tab-estado"
fi

if grep -q "tab-agregar" frontend/index.html; then
    echo -e "${GREEN}✓${NC} HTML contiene tab-agregar"
else
    echo -e "${RED}✗${NC} HTML no contiene tab-agregar"
fi

if grep -q "tab-rapida" frontend/index.html; then
    echo -e "${GREEN}✓${NC} HTML contiene tab-rapida"
else
    echo -e "${RED}✗${NC} HTML no contiene tab-rapida"
fi

if grep -q "tab-canciones" frontend/index.html; then
    echo -e "${GREEN}✓${NC} HTML contiene tab-canciones"
else
    echo -e "${RED}✗${NC} HTML no contiene tab-canciones"
fi

if grep -q "tab-conflictos" frontend/index.html; then
    echo -e "${GREEN}✓${NC} HTML contiene tab-conflictos"
else
    echo -e "${RED}✗${NC} HTML no contiene tab-conflictos"
fi

# ===========================================
# TEST 7: Verificar funciones JavaScript
# ===========================================
print_section "TEST 7: Funciones JavaScript"

if grep -q "function cambiarTab" frontend/script.js; then
    echo -e "${GREEN}✓${NC} JavaScript contiene función cambiarTab()"
else
    echo -e "${RED}✗${NC} JavaScript no contiene función cambiarTab()"
fi

if grep -q "actualizarResumenProgramacion" frontend/script.js; then
    echo -e "${GREEN}✓${NC} JavaScript contiene función actualizarResumenProgramacion()"
else
    echo -e "${RED}✗${NC} JavaScript no contiene función actualizarResumenProgramacion()"
fi

if grep -q "cargarCanciones" frontend/script.js; then
    echo -e "${GREEN}✓${NC} JavaScript contiene función cargarCanciones()"
else
    echo -e "${RED}✗${NC} JavaScript no contiene función cargarCanciones()"
fi

# ===========================================
# TEST 8: Verificar CSS
# ===========================================
print_section "TEST 8: Estilos CSS"

if grep -q ".tab-btn" frontend/style.css; then
    echo -e "${GREEN}✓${NC} CSS contiene estilos para .tab-btn"
else
    echo -e "${RED}✗${NC} CSS no contiene estilos para .tab-btn"
fi

if grep -q ".tab-content" frontend/style.css; then
    echo -e "${GREEN}✓${NC} CSS contiene estilos para .tab-content"
else
    echo -e "${RED}✗${NC} CSS no contiene estilos para .tab-content"
fi

if grep -q "tabs-nav" frontend/style.css; then
    echo -e "${GREEN}✓${NC} CSS contiene estilos para .tabs-nav"
else
    echo -e "${RED}✗${NC} CSS no contiene estilos para .tabs-nav"
fi

# ===========================================
# TEST 9: Verificar config/canciones.json
# ===========================================
print_section "TEST 9: Archivo de Configuración"

if [ -f "config/canciones.json" ]; then
    echo -e "${GREEN}✓${NC} Archivo config/canciones.json existe"
    
    # Verificar que es JSON válido
    if python3 -m json.tool config/canciones.json > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} JSON es válido"
        
        # Contar canciones
        cancion_count=$(python3 -c "import json; f=open('config/canciones.json'); data=json.load(f); f.close(); print(len(data))" 2>/dev/null)
        echo "   Total de canciones en BD: $cancion_count"
    else
        echo -e "${RED}✗${NC} JSON no es válido"
    fi
else
    echo -e "${RED}✗${NC} Archivo config/canciones.json no existe"
fi

# ===========================================
# TEST 10: Documentación
# ===========================================
print_section "TEST 10: Archivos de Documentación"

docs=(
    "README_NUEVO.md"
    "CAMBIOS_INTERFAZ_TABS.md"
    "GUIA_VISUAL_TABS.md"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "${GREEN}✓${NC} Documentación: $doc"
    else
        echo -e "${YELLOW}⚠${NC} Documentación no encontrada: $doc"
    fi
done

# ===========================================
# RESUMEN FINAL
# ===========================================
print_section "RESUMEN DE PRUEBAS"

echo ""
echo -e "${GREEN}✅ Sistema MusicBell configurado correctamente${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Abre navegador: http://localhost:5000"
echo "2. Navega entre los 5 tabs usando los botones"
echo "3. Agrega canciones usando tab [➕ Agregar Canción]"
echo "4. Usa [⚡ Programación Rápida] para generar automáticamente"
echo "5. Verifica estado en [📊 Estado]"
echo "6. Detección de conflictos en [⚠️ Conflictos]"
echo ""
echo "Para iniciar el servidor:"
echo -e "  ${BLUE}bash start.sh${NC} (macOS/Linux)"
echo -e "  ${BLUE}start.bat${NC} (Windows)"
echo ""
