#!/bin/bash
#
# Inspector-G Terminal Splits Launcher
# Creates splits using terminal-specific methods
#

echo "🔍 Launching Inspector-G with terminal splits..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect available terminal emulators
detect_terminal() {
    if command -v gnome-terminal &> /dev/null; then
        echo "gnome-terminal"
    elif command -v kitty &> /dev/null; then
        echo "kitty"
    elif command -v konsole &> /dev/null; then
        echo "konsole"
    elif command -v alacritty &> /dev/null; then
        echo "alacritty"
    else
        echo "none"
    fi
}

TERMINAL=$(detect_terminal)

if [ "$TERMINAL" = "none" ]; then
    echo "❌ No supported terminal emulator found!"
    echo "Please install one of: gnome-terminal, kitty, konsole, alacritty"
    exit 1
fi

echo "📱 Using terminal: $TERMINAL"

case $TERMINAL in
    "kitty")
        # Kitty has excellent split support
        kitty --title="Inspector-G" \
              --session <(cat << 'EOF'
layout splits
launch ./tools/intel-feed.sh
launch ./tools/status-monitor.sh
launch ./tools/main-console.sh
focus
enabled_layouts splits
EOF
) &
        ;;

    "gnome-terminal")
        # Use gnome-terminal tabs as splits
        gnome-terminal \
            --title="Inspector-G" \
            --tab --title="Intelligence Feed" --working-directory="$SCRIPT_DIR" -- bash -c "./tools/intel-feed.sh; exec bash" \
            --tab --title="Status Monitor" --working-directory="$SCRIPT_DIR" -- bash -c "./tools/status-monitor.sh; exec bash" \
            --tab --title="Main Console" --working-directory="$SCRIPT_DIR" -- bash -c "./tools/main-console.sh; exec bash" &
        ;;

    "konsole")
        # Use konsole tabs
        konsole \
            --new-tab --title="Intelligence Feed" --workdir "$SCRIPT_DIR" -e bash -c "./tools/intel-feed.sh; exec bash" \
            --new-tab --title="Status Monitor" --workdir "$SCRIPT_DIR" -e bash -c "./tools/status-monitor.sh; exec bash" \
            --new-tab --title="Main Console" --workdir "$SCRIPT_DIR" -e bash -c "./tools/main-console.sh; exec bash" &
        ;;

    *)
        echo "❌ Terminal splits not supported for: $TERMINAL"
        echo "💡 Try installing kitty for best split support: sudo apt install kitty"
        echo "🔄 Falling back to simple launcher..."
        ./launch-simple.sh
        ;;
esac

echo "✅ Inspector-G launched with splits/tabs!"
echo "💡 Use Ctrl+Shift+T for new tabs, Ctrl+PageUp/PageDown to switch"