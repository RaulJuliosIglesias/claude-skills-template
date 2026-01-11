#!/bin/bash

# Quick setup script for Claude Skills Template
# Usage: ./setup.sh

set -e

echo "🚀 Setting up Claude Skills Template..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo -e "${GREEN}✓${NC} Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️${NC}  Please edit .env and add your ANTHROPIC_API_KEY"
    echo -e "   Get your API key at: https://console.anthropic.com/"
else
    echo -e "${GREEN}✓${NC} .env file already exists"
fi

# Create outputs directory
if [ ! -d "outputs" ]; then
    mkdir outputs
    echo -e "${GREEN}✓${NC} outputs directory created"
fi

echo ""
echo -e "${GREEN}✅${NC} Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your ANTHROPIC_API_KEY"
echo "2. Run: python test_skills.py (verify configuration)"
echo "3. Read GETTING_STARTED.md for your first use"
echo "4. Review examples/ to see usage examples"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
