#!/bin/bash
#
# Inspector-G Window Launcher
# Opens 3 separate windows you can arrange manually
#

echo "🔍 Launching Inspector-G with separate windows..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if kitty is available
if ! command -v kitty &> /dev/null; then
    echo "❌ Kitty terminal not found!"
    echo "Using fallback launcher..."
    ./launch-simple.sh
    exit 0
fi

echo "📱 Using kitty terminal"
echo "📋 Opening 3 windows..."

# Main Console - larger window
kitty --title="Inspector-G: Main Console" \
      bash -c "cd '$SCRIPT_DIR' && ./tools/main-console.sh; exec bash" &

sleep 0.5

# Intelligence Feed - smaller window
kitty --title="Inspector-G: Intel Feed" \
      bash -c "cd '$SCRIPT_DIR' && ./tools/intel-feed.sh; exec bash" &

sleep 0.5

# Status Monitor - smaller window
kitty --title="Inspector-G: Status Monitor" \
      bash -c "cd '$SCRIPT_DIR' && ./tools/status-monitor.sh; exec bash" &

echo "✅ Inspector-G launched with 3 windows!"
echo "💡 Arrange the windows as you like:"
echo "  - Main Console (large, bottom)"
echo "  - Intel Feed (small, top-left)"
echo "  - Status Monitor (small, top-right)"