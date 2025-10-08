"""
InspectorBrain Theme System

Inspector Gadget inspired themes with professional terminal aesthetics
and nostalgic color schemes that enhance the OSINT experience.
"""

from typing import Dict, Any
from textual.app import App
from rich.style import Style
from rich.theme import Theme as RichTheme

from src.core.config import settings

class InspectorGadgetTheme:
    """Inspector Gadget themed styling for InspectorBrain TUI"""

    def __init__(self):
        self.current_scheme = settings.color_scheme
        self.themes = self._load_theme_definitions()

    def _load_theme_definitions(self) -> Dict[str, Dict[str, str]]:
        """Load all available theme definitions"""
        return {
            "classic_terminal": {
                # Classic green-on-black terminal
                "primary": "#00FF00",
                "secondary": "#FFFF00",
                "accent": "#FF0000",
                "background": "#000000",
                "surface": "#111111",
                "text": "#FFFFFF",
                "text_muted": "#AAAAAA",
                "success": "#00FF00",
                "warning": "#FFFF00",
                "error": "#FF0000",
                "info": "#00FFFF"
            },
            "modern_dark": {
                # Modern dark theme with blue accents
                "primary": "#61DAFB",
                "secondary": "#F7931E",
                "accent": "#FF6B6B",
                "background": "#1E1E1E",
                "surface": "#2D2D2D",
                "text": "#FFFFFF",
                "text_muted": "#CCCCCC",
                "success": "#4CAF50",
                "warning": "#FF9800",
                "error": "#F44336",
                "info": "#2196F3"
            },
            "retro_green": {
                # Retro neon green theme
                "primary": "#39FF14",
                "secondary": "#FFFF00",
                "accent": "#FF1493",
                "background": "#000000",
                "surface": "#001100",
                "text": "#39FF14",
                "text_muted": "#228B22",
                "success": "#39FF14",
                "warning": "#FFFF00",
                "error": "#FF1493",
                "info": "#00FFFF"
            },
            "inspector_blue": {
                # Inspector Gadget's blue coat inspired
                "primary": "#0066CC",
                "secondary": "#FFD700",
                "accent": "#FF4500",
                "background": "#000033",
                "surface": "#001166",
                "text": "#FFFFFF",
                "text_muted": "#CCDDFF",
                "success": "#00CC66",
                "warning": "#FFD700",
                "error": "#FF4500",
                "info": "#66CCFF"
            }
        }

    def get_current_colors(self) -> Dict[str, str]:
        """Get the current color scheme"""
        return self.themes.get(self.current_scheme, self.themes["classic_terminal"])

    def apply_theme(self, app: App) -> None:
        """Apply the current theme to the Textual app"""
        colors = self.get_current_colors()

        # Create Rich theme for consistent styling
        rich_theme = RichTheme({
            "primary": colors["primary"],
            "secondary": colors["secondary"],
            "accent": colors["accent"],
            "success": colors["success"],
            "warning": colors["warning"],
            "error": colors["error"],
            "info": colors["info"],
            "muted": colors["text_muted"]
        })

        # Apply theme to app console
        app.console._theme = rich_theme

    def get_gadget_ascii_art(self) -> str:
        """Get Inspector Gadget themed ASCII art"""
        if not settings.ascii_art_enabled:
            return ""

        art_options = [
            # Brain the dog (simple)
            "     /\\_/\\\\n    ( o.o )\\n     > ^ <\\n    BRAIN",
            # Inspector Gadget hat
            "    ________\\n   |  _  _  |\\n   | |_||_| |\\n   |________|\\n   INSPECTOR",
            # Gadget gear
            "      ⚙️ ⚙️\\n    ⚙️ GADGET ⚙️\\n      ⚙️ ⚙️"
        ]

        import random
        return random.choice(art_options) if art_options else ""

    def get_progress_spinner(self) -> str:
        """Get Inspector Gadget themed progress spinner"""
        spinners = {
            "classic": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
            "gadget": "🔍🕵️🔍🕵️",
            "gears": "⚙️🔧⚙️🔧",
            "brain": "🧠💭🧠💭"
        }

        return spinners.get("gadget" if settings.gadget_commands else "classic")

    def get_status_icons(self) -> Dict[str, str]:
        """Get status icons for different states"""
        return {
            "investigating": "🔍",
            "complete": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "brain": "🧠",
            "gadget": "🕵️",
            "gear": "⚙️",
            "success": "🎉" if settings.wowser_notifications else "✅"
        }

    def format_gadget_message(self, message: str, message_type: str = "info") -> str:
        """Format message with Inspector Gadget theming"""
        if not settings.catchphrases_enabled:
            return message

        icons = self.get_status_icons()
        icon = icons.get(message_type, "ℹ️")

        prefixes = {
            "info": "Go-Go-Gadget Info:",
            "success": "Wowser!",
            "error": "Gadget malfunction!",
            "warning": "Brain says be careful:",
            "investigating": "Go-Go-Gadget Investigation:"
        }

        prefix = prefixes.get(message_type, "")
        return f"{icon} {prefix} {message}" if prefix else f"{icon} {message}"

    def get_welcome_banner(self) -> str:
        """Get the main welcome banner"""
        colors = self.get_current_colors()

        banner = f"""[bold {colors['primary']}]🔍 InspectorBrain - Advanced OSINT Suite 🕵️[/bold {colors['primary']}]

[{colors['accent']}]"Like Brain the dog who secretly solved Inspector Gadget's cases,
InspectorBrain works behind the scenes to uncover digital intelligence."[/{colors['accent']}]

[bold {colors['info']}]🔍 Go-Go-Gadget Intelligence! 🕵️[/bold {colors['info']}]"""

        return banner

    def get_module_headers(self) -> Dict[str, str]:
        """Get themed headers for different OSINT modules"""
        colors = self.get_current_colors()

        return {
            "username": f"[bold {colors['primary']}]🔍 Go-Go-Gadget Username Search![/bold {colors['primary']}]",
            "email": f"[bold {colors['primary']}]📧 Go-Go-Gadget Email Analysis![/bold {colors['primary']}]",
            "phone": f"[bold {colors['primary']}]📞 Go-Go-Gadget Phone Intel![/bold {colors['primary']}]",
            "domain": f"[bold {colors['primary']}]🌐 Go-Go-Gadget Domain Scan![/bold {colors['primary']}]",
            "ai": f"[bold {colors['primary']}]🤖 Go-Go-Gadget AI Assistant![/bold {colors['primary']}]"
        }

# Global theme instance
theme = InspectorGadgetTheme()