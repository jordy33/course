#!/bin/bash

# Script para instalar dependencias en macOS: Homebrew, FFmpeg, Node.js, Mermaid-CLI y Chrome
# Ejecuta con: chmod +x install_dependencies.sh && ./install_dependencies.sh

echo "Verificando e instalando dependencias para el proyecto de cursos..."

# Instalar Homebrew si no está presente
if ! command -v brew &> /dev/null; then
    echo "Homebrew no encontrado. Instalando Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "Homebrew instalado. Actualizando..."
    brew update
else
    echo "Homebrew ya está instalado."
fi

# Instalar FFmpeg (incluye ffprobe)
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg no encontrado. Instalando FFmpeg..."
    brew install ffmpeg
else
    echo "FFmpeg ya está instalado."
fi

# Verificar ffprobe (debería venir con FFmpeg)
if ! command -v ffprobe &> /dev/null; then
    echo "Error: ffprobe no encontrado. Intenta reinstalar FFmpeg con 'brew reinstall ffmpeg'."
else
    echo "ffprobe está disponible."
fi

# Instalar Node.js (incluye npm)
if ! command -v node &> /dev/null; then
    echo "Node.js no encontrado. Instalando Node.js..."
    brew install node
else
    echo "Node.js ya está instalado."
fi

# Instalar Mermaid-CLI globalmente
if ! command -v mmdc &> /dev/null; then
    echo "Mermaid-CLI no encontrado. Instalando Mermaid-CLI..."
    npm install -g @mermaid-js/mermaid-cli
else
    echo "Mermaid-CLI ya está instalado."
fi

# Instalar Chrome para Puppeteer
echo "Instalando Chrome Headless para Mermaid-CLI..."
npx puppeteer browsers install chrome

echo "Instalación completada. Verifica con 'ffmpeg -version', 'node -v', 'npm -v' y 'mmdc -h'."