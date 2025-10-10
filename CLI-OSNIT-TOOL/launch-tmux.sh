#!/bin/bash
#
# Inspector-G Tmux Launcher
# Opens one terminal window with 3 split panes
#

echo "🔍 Launching Inspector-G with tmux splits..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "❌ tmux is not installed!"
    echo "Please install tmux: sudo apt install tmux"
    exit 1
fi

# Kill any existing inspector-g session
tmux kill-session -t inspector-g 2>/dev/null || true

# Create new tmux session with splits
tmux new-session -d -s inspector-g -x 120 -y 40

# Split horizontally (top and bottom)
tmux split-window -h -t inspector-g:0

# Split the left pane vertically (top-left and bottom-left)
tmux split-window -v -t inspector-g:0.0

# Set up the panes:
# Pane 0 (top-left): Intelligence Feed
tmux send-keys -t inspector-g:0.0 "cd '$SCRIPT_DIR' && ./tools/intel-feed.sh" Enter

# Pane 1 (bottom-left): Status Monitor
tmux send-keys -t inspector-g:0.1 "cd '$SCRIPT_DIR' && ./tools/status-monitor.sh" Enter

# Pane 2 (right): Main Console
tmux send-keys -t inspector-g:0.2 "cd '$SCRIPT_DIR' && ./tools/main-console.sh" Enter

# Set pane titles
tmux select-pane -t inspector-g:0.0 -T "Intelligence Feed"
tmux select-pane -t inspector-g:0.1 -T "Status Monitor"
tmux select-pane -t inspector-g:0.2 -T "Main Console"

# Focus on the main console pane
tmux select-pane -t inspector-g:0.2

# Attach to the session
tmux attach-session -t inspector-g

echo "✅ Inspector-G tmux session started!"