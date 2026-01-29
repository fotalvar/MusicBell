#!/bin/bash
# Script para crear canciones de prueba

echo "Creando canciones de prueba..."

# Crear carpeta si no existe
mkdir -p /Users/federicootalvares/Desktop/MusicBell/canciones

# Crear tonos de prueba con ffmpeg si está disponible
if command -v ffmpeg &> /dev/null; then
    # Crear varios tonos diferentes
    ffmpeg -f lavfi -i sine=f=440:d=2 -q:a 9 -acodec libmp3lame /Users/federicootalvares/Desktop/MusicBell/canciones/himno.mp3 -y 2>/dev/null
    ffmpeg -f lavfi -i sine=f=523:d=2 -q:a 9 -acodec libmp3lame /Users/federicootalvares/Desktop/MusicBell/canciones/musica_recreo.mp3 -y 2>/dev/null
    ffmpeg -f lavfi -i sine=f=659:d=2 -q:a 9 -acodec libmp3lame /Users/federicootalvares/Desktop/MusicBell/canciones/evento.mp3 -y 2>/dev/null
    ffmpeg -f lavfi -i sine=f=784:d=2 -q:a 9 -acodec libmp3lame /Users/federicootalvares/Desktop/MusicBell/canciones/almuerzo.mp3 -y 2>/dev/null
    ffmpeg -f lavfi -i sine=f=880:d=2 -q:a 9 -acodec libmp3lame /Users/federicootalvares/Desktop/MusicBell/canciones/fin_clases.mp3 -y 2>/dev/null
    
    echo "✓ 5 canciones de prueba creadas en canciones/"
    ls -lh /Users/federicootalvares/Desktop/MusicBell/canciones/*.mp3
else
    echo "ℹ️ ffmpeg no está instalado. Para crear canciones de prueba:"
    echo "   brew install ffmpeg"
    echo ""
    echo "O copia tus propios archivos MP3 a la carpeta canciones/"
fi
