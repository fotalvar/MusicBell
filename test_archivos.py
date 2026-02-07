#!/usr/bin/env python3
from pathlib import Path

project_root = Path(__file__).parent
songs_dir = project_root / 'canciones'

print(f"Project root: {project_root}")
print(f"Songs dir: {songs_dir}")
print(f"Exists: {songs_dir.exists()}")

if songs_dir.exists():
    print(f"\nArchivos MP3 en carpeta:")
    mp3_files = list(songs_dir.glob('*.mp3'))
    print(f"Total MP3 files: {len(mp3_files)}")
    for file in mp3_files:
        print(f"  - {file.name} ({file.stat().st_size} bytes)")
