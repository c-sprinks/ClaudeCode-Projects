#!/bin/bash
#
# Inspector-G Terminal Suite Launcher
# Opens 3 positioned terminal windows for OSINT operations
#

echo "🔍 Launching Inspector-G Terminal Suite..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect available terminal emulators
detect_terminal() {
    if command -v gnome-terminal &> /dev/null; then
        echo "gnome-terminal"
    elif command -v konsole &> /dev/null; then
        echo "konsole"
    elif command -v kitty &> /dev/null; then
        echo "kitty"
    elif command -v alacritty &> /dev/null; then
        echo "alacritty"
    elif command -v xterm &> /dev/null; then
        echo "xterm"
    else
        echo "none"
    fi
}

TERMINAL=$(detect_terminal)

if [ "$TERMINAL" = "none" ]; then
    echo "❌ No supported terminal emulator found!"
    echo "Please install one of: gnome-terminal, konsole, kitty, alacritty, xterm"
    exit 1
fi

echo "📱 Using terminal: $TERMINAL"

# Get screen resolution for positioning (with fallbacks)
get_screen_resolution() {
    # Try multiple methods to get screen resolution
    if command -v xdpyinfo &> /dev/null; then
        SCREEN_WIDTH=$(xdpyinfo | grep dimensions | sed -r 's/.*\s([0-9]+)x([0-9]+)\s.*/\1/' 2>/dev/null)
        SCREEN_HEIGHT=$(xdpyinfo | grep dimensions | sed -r 's/.*\s([0-9]+)x([0-9]+)\s.*/\2/' 2>/dev/null)
    elif command -v xrandr &> /dev/null; then
        SCREEN_WIDTH=$(xrandr | grep '*' | head -1 | awk '{print $1}' | cut -d'x' -f1 2>/dev/null)
        SCREEN_HEIGHT=$(xrandr | grep '*' | head -1 | awk '{print $1}' | cut -d'x' -f2 2>/dev/null)
    else
        # Fallback to reasonable defaults
        SCREEN_WIDTH=1920
        SCREEN_HEIGHT=1080
        echo "⚠️  Could not detect screen resolution, using defaults: ${SCREEN_WIDTH}x${SCREEN_HEIGHT}"
    fi

    # Validate we got numbers
    if ! [[ "$SCREEN_WIDTH" =~ ^[0-9]+$ ]] || ! [[ "$SCREEN_HEIGHT" =~ ^[0-9]+$ ]]; then
        SCREEN_WIDTH=1920
        SCREEN_HEIGHT=1080
        echo "⚠️  Invalid screen resolution detected, using defaults: ${SCREEN_WIDTH}x${SCREEN_HEIGHT}"
    fi
}

get_screen_resolution

# Calculate window dimensions (thirds of screen)
WINDOW_WIDTH=$((SCREEN_WIDTH / 3))
WINDOW_HEIGHT=$((SCREEN_HEIGHT / 2))

# Window positions
TOP_LEFT_X=0
TOP_LEFT_Y=0
TOP_RIGHT_X=$((WINDOW_WIDTH))
TOP_RIGHT_Y=0
BOTTOM_X=0
BOTTOM_Y=$((WINDOW_HEIGHT))
BOTTOM_WIDTH=$((WINDOW_WIDTH * 2))

launch_gnome_terminal() {
    # Intelligence Feed (top-left)
    gnome-terminal --geometry=80x24+${TOP_LEFT_X}+${TOP_LEFT_Y} \
                   --title="Inspector-G: Intelligence Feed" \
                   --working-directory="$SCRIPT_DIR" \
                   -- bash -c "./tools/intel-feed.sh; exec bash" &

    sleep 0.5

    # Status Monitor (top-right)
    gnome-terminal --geometry=80x24+${TOP_RIGHT_X}+${TOP_RIGHT_Y} \
                   --title="Inspector-G: Status Monitor" \
                   --working-directory="$SCRIPT_DIR" \
                   -- bash -c "./tools/status-monitor.sh; exec bash" &

    sleep 0.5

    # Main Console (bottom, spanning full width)
    gnome-terminal --geometry=160x24+${BOTTOM_X}+${BOTTOM_Y} \
                   --title="Inspector-G: Main Console" \
                   --working-directory="$SCRIPT_DIR" \
                   -- bash -c "./tools/main-console.sh; exec bash" &
}

launch_kitty() {
    # Intelligence Feed (top-left)
    kitty --title="Inspector-G: Intelligence Feed" \
          -o initial_window_width=${WINDOW_WIDTH} \
          -o initial_window_height=${WINDOW_HEIGHT} \
          bash -c "./tools/intel-feed.sh; exec bash" &

    sleep 0.5

    # Status Monitor (top-right)
    kitty --title="Inspector-G: Status Monitor" \
          -o initial_window_width=${WINDOW_WIDTH} \
          -o initial_window_height=${WINDOW_HEIGHT} \
          bash -c "./tools/status-monitor.sh; exec bash" &

    sleep 0.5

    # Main Console (bottom)
    kitty --title="Inspector-G: Main Console" \
          -o initial_window_width=${BOTTOM_WIDTH} \
          -o initial_window_height=${WINDOW_HEIGHT} \
          bash -c "./tools/main-console.sh; exec bash" &
}

launch_xterm() {
    # Intelligence Feed (top-left)
    xterm -geometry 80x24+${TOP_LEFT_X}+${TOP_LEFT_Y} \
          -title "Inspector-G: Intelligence Feed" \
          -e "cd '$SCRIPT_DIR' && ./tools/intel-feed.sh; exec bash" &

    sleep 0.5

    # Status Monitor (top-right)
    xterm -geometry 80x24+${TOP_RIGHT_X}+${TOP_RIGHT_Y} \
          -title "Inspector-G: Status Monitor" \
          -e "cd '$SCRIPT_DIR' && ./tools/status-monitor.sh; exec bash" &

    sleep 0.5

    # Main Console (bottom)
    xterm -geometry 160x24+${BOTTOM_X}+${BOTTOM_Y} \
          -title "Inspector-G: Main Console" \
          -e "cd '$SCRIPT_DIR' && ./tools/main-console.sh; exec bash" &
}

# Launch based on detected terminal
case $TERMINAL in
    "gnome-terminal")
        launch_gnome_terminal
        ;;
    "kitty")
        launch_kitty
        ;;
    "konsole")
        # Konsole uses similar syntax to gnome-terminal
        launch_gnome_terminal
        ;;
    "alacritty")
        # Alacritty doesn't support geometry, use xterm fallback
        launch_xterm
        ;;
    "xterm")
        launch_xterm
        ;;
    *)
        echo "❌ Unsupported terminal: $TERMINAL"
        exit 1
        ;;
esac

echo "✅ Inspector-G Terminal Suite launched!"
echo "📋 Windows:"
echo "  - Intelligence Feed (top-left)"
echo "  - Status Monitor (top-right)"
echo "  - Main Console (bottom)"
echo ""
echo "💡 Close any window to end the session."