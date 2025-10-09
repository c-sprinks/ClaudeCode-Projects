#!/bin/bash
# Inspector-G Desktop Integration Installer

echo "🔍 Installing Inspector-G Desktop Integration..."

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$SCRIPT_DIR/assets"

# Install icons
echo "📱 Installing icons..."
if [ -d "$HOME/.local/share/icons" ]; then
    ICON_DIR="$HOME/.local/share/icons"
else
    mkdir -p "$HOME/.local/share/icons"
    ICON_DIR="$HOME/.local/share/icons"
fi

# Copy icons
cp "$ASSETS_DIR/icons/"*.png "$ICON_DIR/"
echo "✅ Icons installed to $ICON_DIR"

# Install desktop files
echo "🖥️ Installing desktop files..."
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

cp "$ASSETS_DIR/desktop/"*.desktop "$DESKTOP_DIR/"
chmod +x "$DESKTOP_DIR/"*.desktop

echo "✅ Desktop files installed to $DESKTOP_DIR"

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR"
    echo "✅ Desktop database updated"
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache "$ICON_DIR" 2>/dev/null || true
    echo "✅ Icon cache updated"
fi

echo "🎉 Inspector-G desktop integration installed successfully!"
echo "You can now launch Inspector-G from your application menu."
