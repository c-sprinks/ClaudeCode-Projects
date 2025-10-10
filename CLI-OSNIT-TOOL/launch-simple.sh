#!/bin/bash
#
# Inspector-G Simple Launcher
# Opens 3 terminal windows without positioning (let user arrange them)
#

echo "🔍 Launching Inspector-G Terminal Suite (Simple Mode)..."

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
echo "📋 Opening 3 windows (arrange them as you like)..."

launch_simple_windows() {
    case $TERMINAL in
        "gnome-terminal")
            # Intelligence Feed
            gnome-terminal --title="Inspector-G: Intelligence Feed" \
                           --working-directory="$SCRIPT_DIR" \
                           -- bash -c "./tools/intel-feed.sh; exec bash" &

            sleep 1

            # Status Monitor
            gnome-terminal --title="Inspector-G: Status Monitor" \
                           --working-directory="$SCRIPT_DIR" \
                           -- bash -c "./tools/status-monitor.sh; exec bash" &

            sleep 1

            # Main Console
            gnome-terminal --title="Inspector-G: Main Console" \
                           --working-directory="$SCRIPT_DIR" \
                           -- bash -c "./tools/main-console.sh; exec bash" &
            ;;

        "kitty")
            # Intelligence Feed
            kitty --title="Inspector-G: Intelligence Feed" \
                  bash -c "cd '$SCRIPT_DIR' && ./tools/intel-feed.sh; exec bash" &

            sleep 1

            # Status Monitor
            kitty --title="Inspector-G: Status Monitor" \
                  bash -c "cd '$SCRIPT_DIR' && ./tools/status-monitor.sh; exec bash" &

            sleep 1

            # Main Console
            kitty --title="Inspector-G: Main Console" \
                  bash -c "cd '$SCRIPT_DIR' && ./tools/main-console.sh; exec bash" &
            ;;

        "konsole")
            # Intelligence Feed
            konsole --title="Inspector-G: Intelligence Feed" \
                    --workdir "$SCRIPT_DIR" \
                    -e bash -c "./tools/intel-feed.sh; exec bash" &

            sleep 1

            # Status Monitor
            konsole --title="Inspector-G: Status Monitor" \
                    --workdir "$SCRIPT_DIR" \
                    -e bash -c "./tools/status-monitor.sh; exec bash" &

            sleep 1

            # Main Console
            konsole --title="Inspector-G: Main Console" \
                    --workdir "$SCRIPT_DIR" \
                    -e bash -c "./tools/main-console.sh; exec bash" &
            ;;

        "alacritty")
            # Intelligence Feed
            alacritty --title "Inspector-G: Intelligence Feed" \
                      --working-directory "$SCRIPT_DIR" \
                      -e bash -c "./tools/intel-feed.sh; exec bash" &

            sleep 1

            # Status Monitor
            alacritty --title "Inspector-G: Status Monitor" \
                      --working-directory "$SCRIPT_DIR" \
                      -e bash -c "./tools/status-monitor.sh; exec bash" &

            sleep 1

            # Main Console
            alacritty --title "Inspector-G: Main Console" \
                      --working-directory "$SCRIPT_DIR" \
                      -e bash -c "./tools/main-console.sh; exec bash" &
            ;;

        "xterm")
            # Intelligence Feed
            xterm -title "Inspector-G: Intelligence Feed" \
                  -e "cd '$SCRIPT_DIR' && ./tools/intel-feed.sh; exec bash" &

            sleep 1

            # Status Monitor
            xterm -title "Inspector-G: Status Monitor" \
                  -e "cd '$SCRIPT_DIR' && ./tools/status-monitor.sh; exec bash" &

            sleep 1

            # Main Console
            xterm -title "Inspector-G: Main Console" \
                  -e "cd '$SCRIPT_DIR' && ./tools/main-console.sh; exec bash" &
            ;;

        *)
            echo "❌ Unsupported terminal: $TERMINAL"
            exit 1
            ;;
    esac
}

# Launch the windows
launch_simple_windows

echo "✅ Inspector-G Terminal Suite launched!"
echo "📋 Windows opened:"
echo "  - Intelligence Feed"
echo "  - Status Monitor"
echo "  - Main Console"
echo ""
echo "💡 Arrange the windows as you like, then start investigating!"
echo "💡 Use the Main Console window for commands."