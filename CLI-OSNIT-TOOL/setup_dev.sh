#!/bin/bash
# InspectorBrain Development Environment Setup Script
# Run this script to set up a complete development environment

set -e  # Exit on any error

echo "🔍 InspectorBrain Development Setup 🕵️"
echo "=========================================="

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    print_status "Python $PYTHON_VERSION detected (>= 3.8 required)"
else
    print_error "Python $PYTHON_VERSION detected, but >= 3.8 is required"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip
print_status "Pip upgraded"

# Install dependencies
echo -e "${YELLOW}Installing core dependencies...${NC}"
pip install textual rich typer pydantic pydantic-settings loguru
print_status "Core dependencies installed"

echo -e "${YELLOW}Installing development dependencies...${NC}"
pip install pytest pytest-asyncio black mypy pre-commit
print_status "Development dependencies installed"

echo -e "${YELLOW}Installing optional dependencies...${NC}"
pip install httpx aiohttp beautifulsoup4 python-whois phonenumbers dnspython
print_status "Optional dependencies installed"

# Create .env file if it doesn't exist
echo -e "${YELLOW}Setting up environment configuration...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << EOF
# InspectorBrain Environment Configuration
INSPECTORBRAIN_APP_NAME="InspectorBrain"
INSPECTORBRAIN_LOG_LEVEL="INFO"
INSPECTORBRAIN_THEME_NAME="inspector_gadget"
INSPECTORBRAIN_COLOR_SCHEME="classic_terminal"
INSPECTORBRAIN_BRAIN_MODE=true
INSPECTORBRAIN_GADGET_COMMANDS=true
INSPECTORBRAIN_CATCHPHRASES_ENABLED=true
INSPECTORBRAIN_WOWSER_NOTIFICATIONS=true
EOF
    print_status ".env file created with default configuration"
else
    print_warning ".env file already exists"
fi

# Set up pre-commit hooks
echo -e "${YELLOW}Setting up pre-commit hooks...${NC}"
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
EOF

# Install pre-commit hooks
pre-commit install
print_status "Pre-commit hooks installed"

# Make the main script executable
chmod +x inspectorbrain.py
print_status "InspectorBrain script made executable"

# Test the installation
echo -e "${YELLOW}Testing installation...${NC}"
if python3 inspectorbrain.py version > /dev/null 2>&1; then
    print_status "Installation test passed"
else
    print_error "Installation test failed"
    exit 1
fi

# Create initial database
echo -e "${YELLOW}Initializing database...${NC}"
python3 -c "
from src.core.database import db_manager
db_manager.create_tables()
print('Database initialized successfully')
" 2>/dev/null || print_warning "Database initialization skipped (SQLAlchemy not fully configured yet)"

echo ""
echo "🎉 InspectorBrain Development Environment Setup Complete! 🎉"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run InspectorBrain: python3 inspectorbrain.py"
echo "3. For TUI mode: python3 inspectorbrain.py tui"
echo "4. For help: python3 inspectorbrain.py --help"
echo ""
print_status "Go-Go-Gadget Development Environment!"
echo "🧠 Brain mode enabled - ready for intelligent OSINT investigations!"