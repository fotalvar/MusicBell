#!/bin/bash
# Script de inicio para MusicBell en macOS/Linux

echo "================================================"
echo "Iniciando MusicBell - Sistema de Música Escolar"
echo "================================================"

# Navegar a la carpeta del proyecto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "Descárgalo desde: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python $(python3 --version) encontrado"

# Instalar dependencias si es necesario
if [ ! -d "backend/venv" ]; then
    echo "Creando entorno virtual..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Activar entorno virtual
source backend/venv/bin/activate

# Matar procesos que usen el puerto 5000
echo "🔍 Verificando puerto 5000..."
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Encontrado proceso usando puerto 5000, matando..."
    lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null
    sleep 1
    echo "✓ Puerto 5000 liberado"
else
    echo "✓ Puerto 5000 disponible"
fi

# Iniciar la aplicación
echo ""
echo "📂 Carpeta de trabajo: $(pwd)"
echo "🎵 Carpeta de canciones: $(pwd)/canciones"
echo "📝 Logs: $(pwd)/logs"
echo ""
echo "🚀 Iniciando servidor..."
echo ""

# Abrir el navegador automáticamente después de un pequeño delay (solo en macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    (sleep 3 && echo "🌐 Abriendo navegador..." && open "http://localhost:5000") &
fi

cd backend
python app.py
