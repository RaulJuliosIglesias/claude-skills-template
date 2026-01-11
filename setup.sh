#!/bin/bash

# Script de configuración rápida para Claude Skills Template
# Uso: ./setup.sh

set -e

echo "🚀 Configurando Claude Skills Template..."
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Por favor instala Python 3.8 o superior."
    exit 1
fi

echo -e "${GREEN}✓${NC} Python encontrado: $(python3 --version)"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Entorno virtual creado"
else
    echo -e "${GREEN}✓${NC} Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencias instaladas"

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️${NC}  Por favor edita .env y agrega tu ANTHROPIC_API_KEY"
    echo -e "   Obtén tu API key en: https://console.anthropic.com/"
else
    echo -e "${GREEN}✓${NC} Archivo .env ya existe"
fi

# Crear directorio de outputs
if [ ! -d "outputs" ]; then
    mkdir outputs
    echo -e "${GREEN}✓${NC} Directorio outputs creado"
fi

echo ""
echo -e "${GREEN}✅${NC} Configuración completada!"
echo ""
echo "Próximos pasos:"
echo "1. Edita .env y agrega tu ANTHROPIC_API_KEY"
echo "2. Ejecuta: python test_skills.py (verificar configuración)"
echo "3. Lee GETTING_STARTED.md para tu primer uso"
echo "4. Revisa examples/ para ver ejemplos de uso"
echo ""
echo "Para activar el entorno virtual en el futuro:"
echo "  source venv/bin/activate"
