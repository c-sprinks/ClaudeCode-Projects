#!/bin/bash
#
# Inspector-G Kitty Splits Launcher
# Creates a single kitty window with 3 split panes
#

echo "🔍 Launching Inspector-G with kitty splits..."

# Check if kitty is available
if ! command -v kitty &> /dev/null; then
    echo "❌ Kitty terminal not found!"
    echo "Please install kitty: sudo apt install kitty"
    echo "Or use the general launcher: ./launch-splits.sh"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Launch kitty directly with splits
kitty --title="Inspector-G OSINT Suite" \
      bash -c "cd '$SCRIPT_DIR' && echo -e '\033[0;36m[MAIN CONSOLE]\033[0m Inspector-G OSINT Terminal' && ./tools/main-console.sh" \
      --hold &

sleep 1

# Add the other panes using kitty remote control
kitty @ launch --type=window --cwd="$SCRIPT_DIR" bash -c "./tools/intel-feed.sh; exec bash" 2>/dev/null &
kitty @ launch --type=window --cwd="$SCRIPT_DIR" bash -c "./tools/status-monitor.sh; exec bash" 2>/dev/null &

# Clean up session file after a moment
sleep 2
rm -f "$SESSION_FILE"

echo "✅ Inspector-G launched in kitty with splits!"
echo "💡 Use Ctrl+Shift+Enter to create new splits"
echo "💡 Use Ctrl+Shift+] and Ctrl+Shift+[ to navigate between panes"