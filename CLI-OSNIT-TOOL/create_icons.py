#!/usr/bin/env python3
"""
Icon Generator for Inspector-G OSINT Suite

Creates professional PNG icons for desktop integration inspired by
Inspector Gadget's tech aesthetic. Generates multiple sizes for
various desktop environments and use cases.

Icon Design Concept:
- Detective magnifying glass (🔍) as primary element
- Circuit board or tech pattern background
- Inspector Gadget blue/yellow color scheme
- Clean, professional appearance suitable for desktop use
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def create_simple_icon_fallback(size: int) -> Image.Image:
    """Create a simple fallback icon using ASCII art concept"""
    # This creates a simple colored square as fallback
    # In a real implementation, you'd want to use proper graphics

    # Create base image with gradient background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Inspector Gadget color scheme
    primary_color = (41, 128, 185)    # Blue
    secondary_color = (241, 196, 15)  # Yellow
    accent_color = (52, 73, 94)       # Dark blue-gray

    # Create circular background
    margin = size // 8
    circle_coords = [margin, margin, size - margin, size - margin]
    draw.ellipse(circle_coords, fill=primary_color)

    # Add inner circle for depth
    inner_margin = size // 6
    inner_coords = [inner_margin, inner_margin, size - inner_margin, size - inner_margin]
    draw.ellipse(inner_coords, outline=secondary_color, width=max(2, size // 32))

    # Add magnifying glass design
    glass_size = size // 3
    glass_x = size // 2 - glass_size // 2
    glass_y = size // 2 - glass_size // 2

    # Magnifying glass lens
    lens_coords = [glass_x, glass_y, glass_x + glass_size, glass_y + glass_size]
    draw.ellipse(lens_coords, outline=secondary_color, width=max(2, size // 24))

    # Magnifying glass handle
    handle_start_x = glass_x + glass_size - size // 16
    handle_start_y = glass_y + glass_size - size // 16
    handle_end_x = handle_start_x + size // 8
    handle_end_y = handle_start_y + size // 8

    draw.line([handle_start_x, handle_start_y, handle_end_x, handle_end_y],
              fill=secondary_color, width=max(2, size // 32))

    # Add small tech dots for circuit board feel
    dot_size = max(1, size // 64)
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:  # Skip center
                continue
            dot_x = margin + (size - 2 * margin) * i // 2
            dot_y = margin + (size - 2 * margin) * j // 2
            draw.ellipse([dot_x - dot_size, dot_y - dot_size,
                         dot_x + dot_size, dot_y + dot_size],
                        fill=accent_color)

    return img

def create_icon_set():
    """Create a complete set of icons for various desktop uses"""

    print("🎨 Creating Inspector-G Icon Set...")

    # Standard icon sizes for different uses
    icon_sizes = {
        16: "toolbar",      # Toolbar/menu icons
        24: "small",        # Small application icons
        32: "standard",     # Standard application icons
        48: "medium",       # Medium application icons
        64: "large",        # Large application icons
        128: "high_res",    # High resolution
        256: "very_high",   # Very high resolution
        512: "ultra_high"   # Ultra high resolution
    }

    # Create assets directory
    assets_dir = Path("assets/icons")
    assets_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0

    for size, description in icon_sizes.items():
        try:
            # Create icon
            if PIL_AVAILABLE:
                icon = create_simple_icon_fallback(size)
            else:
                # Even simpler fallback - create a basic colored square
                icon = Image.new('RGB', (size, size), (41, 128, 185))
                draw = ImageDraw.Draw(icon)
                # Simple design without PIL
                draw.rectangle([size//4, size//4, 3*size//4, 3*size//4],
                              fill=(241, 196, 15))

            # Save icon
            icon_path = assets_dir / f"inspector-g-{size}x{size}.png"
            icon.save(icon_path, "PNG")

            print(f"✅ Created {description} icon: {icon_path} ({size}x{size})")
            success_count += 1

        except Exception as e:
            print(f"❌ Failed to create {size}x{size} icon: {e}")

    # Create additional special icons
    special_icons = {
        "launcher": 256,    # Desktop launcher
        "notification": 48, # Notification icon
        "taskbar": 32      # Taskbar icon
    }

    for name, size in special_icons.items():
        try:
            if PIL_AVAILABLE:
                icon = create_simple_icon_fallback(size)
            else:
                icon = Image.new('RGB', (size, size), (41, 128, 185))

            icon_path = assets_dir / f"inspector-g-{name}.png"
            icon.save(icon_path, "PNG")
            print(f"✅ Created {name} icon: {icon_path}")
            success_count += 1

        except Exception as e:
            print(f"❌ Failed to create {name} icon: {e}")

    return success_count

def create_desktop_files():
    """Create .desktop files for Linux desktop integration"""

    desktop_dir = Path("assets/desktop")
    desktop_dir.mkdir(parents=True, exist_ok=True)

    # Main application desktop file
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=Inspector-G
Comment=Advanced OSINT Terminal User Interface
GenericName=OSINT Investigation Tool
Exec=python3 inspectorbrain.py
Icon=inspector-g-launcher
Terminal=false
StartupNotify=true
Categories=Network;Security;Development;System;
Keywords=osint;investigation;intelligence;security;reconnaissance;
MimeType=application/x-osint-data;
StartupWMClass=inspector-g
"""

    desktop_file_path = desktop_dir / "inspector-g.desktop"
    with open(desktop_file_path, 'w') as f:
        f.write(desktop_content)

    print(f"✅ Created desktop file: {desktop_file_path}")

    # TUI mode desktop file
    tui_desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=Inspector-G TUI
Comment=Inspector-G Terminal User Interface
GenericName=OSINT Terminal Interface
Exec=python3 inspectorbrain.py tui
Icon=inspector-g-taskbar
Terminal=true
StartupNotify=true
Categories=Network;Security;Development;System;TerminalEmulator;
Keywords=osint;tui;terminal;investigation;
StartupWMClass=inspector-g-tui
"""

    tui_desktop_file_path = desktop_dir / "inspector-g-tui.desktop"
    with open(tui_desktop_file_path, 'w') as f:
        f.write(tui_desktop_content)

    print(f"✅ Created TUI desktop file: {tui_desktop_file_path}")

    return 2

def install_desktop_integration():
    """Create installation script for desktop integration"""

    install_script = """#!/bin/bash
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
"""

    install_script_path = Path("install_desktop.sh")
    with open(install_script_path, 'w') as f:
        f.write(install_script)

    # Make executable
    import stat
    install_script_path.chmod(install_script_path.stat().st_mode | stat.S_IEXEC)

    print(f"✅ Created installation script: {install_script_path}")
    return 1

def main():
    """Main icon creation function"""
    print("🔍 Inspector-G Icon Generator")
    print("=" * 40)

    if not PIL_AVAILABLE:
        print("⚠️ PIL/Pillow not available - using basic fallback icons")
        print("For best results, install Pillow: pip install Pillow")

    total_created = 0

    try:
        # Create icon set
        icon_count = create_icon_set()
        total_created += icon_count

        print("\n📱 Creating desktop integration files...")

        # Create desktop files
        desktop_count = create_desktop_files()
        total_created += desktop_count

        # Create installation script
        script_count = install_desktop_integration()
        total_created += script_count

        print(f"\n🎉 Icon generation completed!")
        print(f"📊 Total files created: {total_created}")
        print(f"📁 Icons location: assets/icons/")
        print(f"🖥️ Desktop files: assets/desktop/")
        print(f"⚙️ Installation script: install_desktop.sh")

        print("\n🚀 To install desktop integration:")
        print("./install_desktop.sh")

        return True

    except Exception as e:
        print(f"❌ Icon generation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)