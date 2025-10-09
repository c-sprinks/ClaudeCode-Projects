#!/bin/bash
# Inspector-G Desktop Launcher Script
# This script handles environment activation and launches Inspector-G

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the Inspector-G directory
cd "$SCRIPT_DIR"

# Clear screen and show banner
clear
echo "=================================================================="
echo "🧠 Inspector-G - Advanced OSINT TUI"
echo "🔍 Go-Go-Gadget Intelligence!"
echo "=================================================================="
echo "Like Brain the dog, working intelligently behind the scenes..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚙️  Setting up Inspector-G environment for first time..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "Press Enter to exit..."
        read
        exit 1
    fi

    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        echo "Press Enter to exit..."
        read
        exit 1
    fi
    echo "✅ Environment setup complete!"
    echo ""
else
    # Activate virtual environment
    source venv/bin/activate
fi

# Verify Python environment
echo "🧠 Brain initializing..."
python --version
echo "📂 Working directory: $SCRIPT_DIR"
echo ""

# Launch Inspector-G TUI
echo "🚀 Launching Inspector-G TUI..."
echo ""

# Run Inspector-G with better error handling
python inspectorbrain.py

# Capture exit code
EXIT_CODE=$?

# Handle exit
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Inspector-G session completed successfully"
    echo "🧠 Brain says: 'Woof! Another case solved!'"
else
    echo "❌ Inspector-G encountered an error (exit code: $EXIT_CODE)"
    echo "🧠 Brain says: 'Woof? Something's not right...'"
    echo ""
    echo "For help, check the documentation or run:"
    echo "python inspectorbrain.py --help"
fi

echo ""
echo "Press Enter to close this window..."
read