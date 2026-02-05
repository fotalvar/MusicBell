#!/bin/bash

# MusicBell - Instalador de Dependencias para Linux Mint
# Este script instala todas las dependencias necesarias

echo "╔════════════════════════════════════════════╗"
echo "║  MusicBell - Instalador de Dependencias   ║"
echo "║       Para Linux Mint                      ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"

# Función para imprimir mensajes
print_info() {
    echo -e "${BLUE}ℹ${NC}  $1"
}

print_success() {
    echo -e "${GREEN}✓${NC}  $1"
}

print_error() {
    echo -e "${RED}✗${NC}  $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC}  $1"
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo ""
print_info "Iniciando instalación de dependencias..."
echo ""

# 1. Actualizar lista de paquetes
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_info "Paso 1/5: Actualizando lista de paquetes del sistema"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

print_info "Ejecutando: sudo apt-get update"
if sudo apt-get update 2>&1 | tail -5; then
    print_success "Lista de paquetes actualizada"
else
    print_warning "Advertencia: apt-get update mostró problemas"
    print_info "Intentando continuar de todas formas..."
fi

echo ""

# 2. Instalar Python3 y pip3
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_info "Paso 2/5: Verificando Python3 y pip3"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if ! command_exists python3; then
    print_info "Python3 no encontrado. Instalando..."
    sudo apt-get install -y python3 >/dev/null 2>&1
    if command_exists python3; then
        print_success "Python3 instalado: $(python3 --version)"
    else
        print_error "Error al instalar Python3"
        exit 1
    fi
else
    print_success "Python3 encontrado: $(python3 --version)"
fi

if ! command_exists pip3; then
    print_info "pip3 no encontrado. Instalando..."
    sudo apt-get install -y python3-pip >/dev/null 2>&1
    if command_exists pip3; then
        print_success "pip3 instalado"
    else
        print_error "Error al instalar pip3"
        exit 1
    fi
else
    print_success "pip3 encontrado"
fi

echo ""

# 3. Instalar VLC (necesario para reproducción de audio)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_info "Paso 3/5: Verificando VLC Media Player"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if ! command_exists vlc; then
    print_info "VLC no encontrado. Instalando..."
    sudo apt-get install -y vlc vlc-plugin-base >/dev/null 2>&1
    if command_exists vlc; then
        print_success "VLC instalado: $(vlc --version 2>/dev/null | head -n1)"
    else
        print_warning "No se pudo instalar VLC automáticamente"
        print_info "Por favor instala VLC manualmente:"
        print_info "  sudo apt-get install vlc vlc-plugin-base"
    fi
else
    print_success "VLC encontrado: $(vlc --version 2>/dev/null | head -n1)"
fi

echo ""

# 4. Instalar dependencias de Python
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_info "Paso 4/5: Instalando dependencias de Python"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$BACKEND_DIR" || exit 1

# Verificar si existe requirements.txt
if [ ! -f "requirements.txt" ]; then
    print_error "No se encontró requirements.txt en $BACKEND_DIR"
    exit 1
fi

print_info "Instalando paquetes de $BACKEND_DIR/requirements.txt"

# Actualizar pip
print_info "Actualizando pip3..."
pip3 install --upgrade pip >/dev/null 2>&1

# Instalar dependencias
if pip3 install -r requirements.txt 2>&1 | grep -q "Successfully installed"; then
    print_success "Dependencias de Python instaladas"
else
    print_warning "Algunas dependencias podrían no haberse instalado correctamente"
    print_info "Reintentando sin cache..."
    pip3 install --no-cache-dir -r requirements.txt >/dev/null 2>&1
fi

echo ""

# 5. Crear entorno virtual si es necesario
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_info "Paso 5/5: Configurando entorno virtual (opcional)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -d "venv" ]; then
    print_success "Entorno virtual ya existe"
else
    print_info "Creando entorno virtual..."
    if python3 -m venv venv >/dev/null 2>&1; then
        print_success "Entorno virtual creado"
        print_info "Para activarlo, ejecuta:"
        print_info "  source venv/bin/activate"
    else
        print_warning "No se pudo crear el entorno virtual"
    fi
fi

echo ""

# Verificación final
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_info "Verificando instalaciones"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verificar Python3
if command_exists python3; then
    print_success "Python3: $(python3 --version)"
else
    print_error "Python3 no disponible"
fi

# Verificar pip3
if command_exists pip3; then
    print_success "pip3: $(pip3 --version)"
else
    print_error "pip3 no disponible"
fi

# Verificar VLC
if command_exists vlc; then
    print_success "VLC: instalado"
else
    print_warning "VLC: no disponible"
fi

# Verificar python-vlc
if python3 -c "import vlc" 2>/dev/null; then
    print_success "python-vlc: $(python3 -c 'import vlc; print(vlc.__version__)')"
else
    print_warning "python-vlc: no disponible"
fi

# Verificar Flask
if python3 -c "import flask" 2>/dev/null; then
    print_success "Flask: $(python3 -c 'import flask; print(flask.__version__)')"
else
    print_warning "Flask: no disponible"
fi

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║     Instalación Completada                 ║"
echo "╚════════════════════════════════════════════╝"
echo ""

print_info "Próximos pasos:"
echo "   1. Navega a la carpeta del proyecto:"
echo "      cd $PROJECT_DIR"
echo ""
echo "   2. Coloca tus archivos MP3 en:"
echo "      mkdir -p canciones"
echo ""
echo "   3. Inicia MusicBell:"
echo "      bash start.sh"
echo ""
echo "   4. Abre en tu navegador:"
echo "      http://localhost:5000"
echo ""

print_success "¡Todo listo para usar MusicBell! 🎵"
echo ""

# Función adicional para troubleshooting
troubleshoot_apt() {
    echo ""
    echo "╔════════════════════════════════════════════╗"
    echo "║     Solución de Problemas con apt-get      ║"
    echo "╚════════════════════════════════════════════╝"
    echo ""
    print_info "Si tienes problemas con apt-get update, intenta:"
    echo ""
    echo "   1. Verificar conexión a internet:"
    echo "      ping google.com"
    echo ""
    echo "   2. Limpiar cache de apt:"
    echo "      sudo apt-get clean"
    echo "      sudo apt-get autoclean"
    echo ""
    echo "   3. Arreglar repositorios dañados:"
    echo "      sudo apt-get update --fix-missing"
    echo ""
    echo "   4. Ejecutar completo:"
    echo "      sudo apt-get update"
    echo "      sudo apt-get upgrade"
    echo ""
    echo "   5. Luego ejecuta el instalador de nuevo:"
    echo "      bash install-dependencies.sh"
    echo ""
}

# Si se pasa como parámetro '--help' mostrar ayuda
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    echo "MusicBell - Script Instalador"
    echo "Uso: bash install-dependencies.sh [opciones]"
    echo ""
    echo "Opciones:"
    echo "  --help, -h        Mostrar esta ayuda"
    echo "  --troubleshoot    Mostrar solución de problemas"
    echo ""
fi

# Si se pasa como parámetro '--troubleshoot' mostrar troubleshooting
if [[ "$1" == "--troubleshoot" ]]; then
    troubleshoot_apt
fi

