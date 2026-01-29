#!/bin/bash
# Script para sincronizar cambios desde desarrollo (macOS) a producción (Windows)
# Úsalo cuando realices cambios en macOS y quieras actualizarlos en Windows

set -e  # Salir si hay error

echo "================================================"
echo "MusicBell - Script de Sincronización"
echo "================================================"
echo ""

# Variables
PROJECT_DIR="/Users/federicootalvares/Desktop/MusicBell"
BACKUP_DIR="${PROJECT_DIR}/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Crear carpeta de backups
mkdir -p "$BACKUP_DIR"

# Crear backup antes de sincronizar
echo "📦 Creando backup..."
tar -czf "${BACKUP_DIR}/musicbell_backup_${TIMESTAMP}.tar.gz" \
  --exclude="backups" \
  --exclude="logs" \
  --exclude=".git" \
  -C "$PROJECT_DIR" . 2>/dev/null

echo "✓ Backup creado: musicbell_backup_${TIMESTAMP}.tar.gz"
echo ""

# Mostrar cambios
echo "📝 Cambios pendientes en:"
echo ""
cd "$PROJECT_DIR"

# Backend
echo "Backend:"
ls -lh backend/*.py backend/requirements.txt 2>/dev/null | awk '{print "  • " $9 " (" $5 ")"}'
echo ""

# Frontend
echo "Frontend:"
ls -lh frontend/* 2>/dev/null | awk '{print "  • " $9 " (" $5 ")"}'
echo ""

# Config
echo "Configuración:"
ls -lh config/*.json 2>/dev/null | awk '{print "  • " $9 " (" $5 ")"}'
echo ""

# Scripts
echo "Scripts:"
ls -lh *.sh *.bat 2>/dev/null | awk '{print "  • " $9 " (" $5 ")"}'
echo ""

echo "================================================"
echo "Instrucciones para sincronizar en Windows:"
echo "================================================"
echo ""
echo "Opción 1: Copiar archivos"
echo "  1. Zip: ${PROJECT_DIR}"
echo "  2. Descarga el ZIP en Windows"
echo "  3. Extrae en C:\\MusicBell"
echo "  4. Reinicia: python backend\\install_service.py restart"
echo ""
echo "Opción 2: Usar GitHub"
echo "  1. git add ."
echo "  2. git commit -m 'Updates'"
echo "  3. git push"
echo "  4. En Windows: git pull && restart"
echo ""
echo "Opción 3: Rsync (si tienes acceso remoto)"
echo "  rsync -avz --exclude='logs' --exclude='.git' \\"
echo "    '${PROJECT_DIR}/' 'usuario@windows-ip:C:\\MusicBell'"
echo ""

# Limpiar viejos backups (mantener últimos 5)
echo "🧹 Limpiando backups antiguos..."
cd "$BACKUP_DIR"
ls -t musicbell_backup_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm

echo ""
echo "✓ Sincronización lista. Ahora copia los cambios a Windows."
echo ""
