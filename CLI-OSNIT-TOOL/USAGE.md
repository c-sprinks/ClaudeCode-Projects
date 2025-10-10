# Inspector-G Usage Guide

## 🚀 **Quick Start**

### **Launch Inspector-G**
```bash
./launch-inspector-g.sh
```

This will open **3 native terminal windows**:

1. **Intelligence Feed** (top-left) - Real-time monitoring and updates
2. **Status Monitor** (top-right) - System status and target tracking
3. **Main Console** (bottom) - Interactive command interface

## 📋 **Available Commands** (in Main Console)

### **Investigation Commands**
- `username <target>` - Investigate username across platforms
- `email <domain>` - Analyze email domain patterns
- `domain <target>` - Scan domain infrastructure
- `brain <query>` - AI analysis of query

### **Character Interactions**
- `penny` - Penny assistance and tips
- `quimby` - Chief Quimby briefings
- `mad` - M.A.D. threat analysis

### **Utility Commands**
- `help` - Show available commands
- `clear` - Clear screen
- `status` - Show system status
- `quit` / `exit` - Exit Inspector-G

## 🖥️ **Example Session**

```bash
inspector-g> username john_doe
[07:15:32] • Starting username investigation: john_doe

Platform             Status               Profile              Confidence
─────────────────────────────────────────────────────────────────────────────
GitHub               Found                john_doe_profile     87%
Twitter              Not Found            -                    -
LinkedIn             Found                john_doe_profile     92%

[07:15:35] ✓ Username investigation complete

inspector-g> email example.com
[07:15:40] • Starting email investigation: example.com
[07:15:41] ✓ DNS lookup: Complete
[07:15:42] ✓ Email pattern analysis: Complete

Email Pattern                    Confidence    Risk Level
─────────────────────────────────────────────────────────────────
firstname.lastname@example.com  High          Low
admin@example.com               High          High

[07:15:45] ✓ Email investigation complete
```

## ✨ **Features**

- **No TUI library dependencies** - uses pure bash and ANSI colors
- **No mouse tracking issues** - native terminal experience
- **Works with any terminal** - gnome-terminal, kitty, alacritty, etc.
- **Real-time updates** - intelligence feed and status monitoring
- **Interactive commands** - full OSINT investigation suite
- **Character integration** - Inspector Gadget universe

## 🛠️ **Supported Terminals**

- gnome-terminal ✅
- kitty ✅
- konsole ✅
- alacritty ✅
- xterm ✅

The launcher automatically detects your terminal and adjusts accordingly.

## 🎯 **Why This Approach Works**

- ✅ **Simple and reliable** - no complex frameworks
- ✅ **Native terminal experience** - uses your settings
- ✅ **Independent windows** - resize and position as needed
- ✅ **Clean codebase** - easy to maintain and extend
- ✅ **No mouse issues** - standard terminal behavior