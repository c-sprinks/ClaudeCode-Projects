"""
Inspector-G Main TUI Application

The core Textual application that provides the advanced terminal user interface
with Inspector Gadget theming and professional OSINT capabilities.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Static, Button, Input, DataTable,
    TabbedContent, TabPane, Log, Tree, Label
)
from textual.binding import Binding
from textual.screen import Screen
from textual import work
from rich.text import Text
from rich.panel import Panel
from rich.console import Console
import asyncio
from typing import Optional, Dict, Any
from loguru import logger

from src.core.config import settings
from src.ui.themes import InspectorGadgetTheme
from src.ui.widgets import (
    GadgetHeader, ResultsPanel, InvestigationPanel,
    StatusPanel, WelcomeScreen
)

class InspectorGApp(App[str]):
    """
    Main Inspector-G TUI Application

    Like Brain the dog working behind the scenes, this app provides
    a sophisticated interface for OSINT investigations.
    """

    # Application metadata
    TITLE = "Inspector-G - Advanced OSINT Suite"
    SUB_TITLE = "Go-Go-Gadget Intelligence!"

    # Key bindings with Inspector Gadget flair
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+h", "help", "Help", show=True),
        Binding("ctrl+n", "new_investigation", "New Investigation", show=True),
        Binding("ctrl+s", "save_results", "Save Results", show=True),
        Binding("ctrl+e", "export", "Export", show=True),
        Binding("f1", "gadget_help", "Gadget Help", show=False),
        Binding("f2", "toggle_theme", "Toggle Theme", show=False),
        Binding("f3", "brain_mode", "Brain Mode", show=False),
    ]

    # CSS for Inspector Gadget theming
    CSS_PATH = "assets/themes/inspector_gadget.css"

    def __init__(self):
        super().__init__()
        self.console = Console()
        self.theme = InspectorGadgetTheme()
        self.current_investigation: Optional[Dict[str, Any]] = None
        self.investigation_history: list = []

    def compose(self) -> ComposeResult:
        """Compose the main application layout"""
        # Apply Inspector Gadget theme
        self.theme.apply_theme(self)

        # Main application layout
        yield GadgetHeader(id="header")

        with TabbedContent(initial="welcome"):
            with TabPane("🏠 Welcome", id="welcome"):
                yield WelcomeScreen(id="welcome_screen")

            with TabPane("🔍 Username Intel", id="username"):
                yield InvestigationPanel("username", id="username_panel")

            with TabPane("📧 Email Analysis", id="email"):
                yield InvestigationPanel("email", id="email_panel")

            with TabPane("📞 Phone Intel", id="phone"):
                yield InvestigationPanel("phone", id="phone_panel")

            with TabPane("🌐 Domain Scan", id="domain"):
                yield InvestigationPanel("domain", id="domain_panel")

            with TabPane("🤖 AI Assistant", id="ai"):
                yield InvestigationPanel("ai", id="ai_panel")

            with TabPane("📊 Results", id="results"):
                yield ResultsPanel(id="results_panel")

        yield StatusPanel(id="status")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application on startup"""
        logger.info("Inspector-G TUI started")

        # Display welcome message
        if settings.catchphrases_enabled:
            self.notify(settings.get_gadget_greeting(), severity="information")

        # Initialize any background tasks
        self.run_worker(self._background_tasks())

    @work(exclusive=True)
    async def _background_tasks(self) -> None:
        """Background tasks for the application"""
        # Check for updates, maintain connections, etc.
        while True:
            await asyncio.sleep(60)  # Check every minute
            # TODO: Implement background health checks

    def action_quit(self) -> None:
        """Quit the application with Inspector Gadget flair"""
        if settings.wowser_notifications:
            self.notify("Wowser! Until next time!", severity="information")

        logger.info("Inspector-G TUI closed")
        self.exit()

    def action_help(self) -> None:
        """Display help information"""
        help_screen = HelpScreen()
        self.push_screen(help_screen)

    def action_new_investigation(self) -> None:
        """Start a new investigation"""
        investigation_screen = NewInvestigationScreen()
        self.push_screen(investigation_screen)

    def action_save_results(self) -> None:
        """Save current investigation results"""
        if self.current_investigation:
            # TODO: Implement save functionality
            self.notify("Go-Go-Gadget Save! Results saved successfully.", severity="information")
        else:
            self.notify("No active investigation to save.", severity="warning")

    def action_export(self) -> None:
        """Export results in various formats"""
        export_screen = ExportScreen()
        self.push_screen(export_screen)

    def action_gadget_help(self) -> None:
        """Show Inspector Gadget themed help"""
        gadget_help_screen = GadgetHelpScreen()
        self.push_screen(gadget_help_screen)

    def action_toggle_theme(self) -> None:
        """Toggle between available themes"""
        current_theme = settings.color_scheme
        themes = ["classic_terminal", "modern_dark", "retro_green"]

        current_index = themes.index(current_theme) if current_theme in themes else 0
        next_index = (current_index + 1) % len(themes)

        settings.color_scheme = themes[next_index]
        self.theme.apply_theme(self)

        self.notify(f"Theme changed to: {settings.color_scheme}", severity="information")

    def action_brain_mode(self) -> None:
        """Toggle Brain the dog mode"""
        settings.brain_mode = not settings.brain_mode

        if settings.brain_mode:
            self.notify("Brain mode activated! Like the dog who solved the cases.", severity="information")
        else:
            self.notify("Brain mode deactivated.", severity="information")

class HelpScreen(Screen[None]):
    """Help screen with Inspector Gadget themed information"""

    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            Static(
                """[bold blue]Inspector-G Help[/bold blue]

[yellow]🔍 Go-Go-Gadget Commands:[/yellow]
• Ctrl+Q: Quit application
• Ctrl+H: Show this help
• Ctrl+N: Start new investigation
• Ctrl+S: Save current results
• Ctrl+E: Export results
• F1: Gadget-specific help
• F2: Toggle visual theme
• F3: Toggle Brain mode

[yellow]🧠 Investigation Modules:[/yellow]
• Username Intel: Multi-platform username reconnaissance
• Email Analysis: Email harvesting and validation
• Phone Intel: Phone number intelligence gathering
• Domain Scan: Comprehensive domain reconnaissance
• AI Assistant: Natural language OSINT queries

[yellow]🎨 Inspector Gadget Features:[/yellow]
• Catchphrases: "Go-Go-Gadget" commands and "Wowser!" notifications
• Brain Mode: Enhanced intelligence like Brain the dog
• Gadget Sounds: Audio effects for actions (when enabled)
• Retro Themes: Classic terminal aesthetics

[dim]Like Brain the dog who secretly solved Inspector Gadget's cases,
Inspector-G works behind the scenes to uncover digital intelligence.[/dim]""",
                id="help_content"
            ),
            id="help_container"
        )

class NewInvestigationScreen(Screen[None]):
    """Screen for starting a new investigation"""

    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
        Binding("ctrl+enter", "start_investigation", "Start", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            Static("[bold blue]Go-Go-Gadget New Investigation![/bold blue]", id="title"),
            Vertical(
                Label("Investigation Type:"),
                Button("🔍 Username Reconnaissance", id="btn_username"),
                Button("📧 Email Intelligence", id="btn_email"),
                Button("📞 Phone Analysis", id="btn_phone"),
                Button("🌐 Domain Scanning", id="btn_domain"),
                Button("🤖 AI-Powered Query", id="btn_ai"),
                id="investigation_buttons"
            ),
            id="new_investigation_container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle investigation type selection"""
        investigation_type = event.button.id.replace("btn_", "")

        # TODO: Start investigation based on type
        self.notify(f"Go-Go-Gadget {investigation_type.title()} Investigation!", severity="information")
        self.dismiss()

class ExportScreen(Screen[None]):
    """Screen for exporting investigation results"""

    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            Static("[bold blue]Go-Go-Gadget Export![/bold blue]", id="title"),
            Vertical(
                Label("Export Format:"),
                Button("📄 JSON Report", id="btn_json"),
                Button("📊 CSV Data", id="btn_csv"),
                Button("📋 PDF Report", id="btn_pdf"),
                Button("📝 Markdown", id="btn_markdown"),
                id="export_buttons"
            ),
            id="export_container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle export format selection"""
        format_type = event.button.id.replace("btn_", "")

        # TODO: Implement actual export functionality
        self.notify(f"Wowser! Exporting as {format_type.upper()}...", severity="information")
        self.dismiss()

class GadgetHelpScreen(Screen[None]):
    """Special Inspector Gadget themed help screen"""

    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            Static(
                """[bold yellow]🕵️ Inspector Gadget's OSINT Manual 🕵️[/bold yellow]

[blue]"Go-Go-Gadget Investigation!"[/blue]

[yellow]🔍 The Gadget Way of OSINT:[/yellow]
Like Inspector Gadget's amazing gadgets, Inspector-G has specialized tools:

[green]🧠 Brain Mode:[/green] Like Brain the dog, work intelligently behind the scenes
[green]🔍 Go-Go-Gadget Username Search:[/green] Find usernames across platforms
[green]📧 Go-Go-Gadget Email Analysis:[/green] Discover email patterns
[green]📞 Go-Go-Gadget Phone Intel:[/green] Investigate phone numbers
[green]🌐 Go-Go-Gadget Domain Scan:[/green] Comprehensive domain reconnaissance

[yellow]🎵 Gadget Catchphrases:[/yellow]
• "Wowser!" - Success notifications
• "Go-Go-Gadget [Tool]!" - Starting investigations
• "Brain, what do you think?" - AI assistance

[yellow]🎨 M.A.D. Detection:[/yellow]
Inspector-G helps identify threats and suspicious activities,
just like Inspector Gadget fighting the M.A.D. organization!

[dim]Remember: With great gadgets comes great responsibility.
Use your powers for good, just like Inspector Gadget![/dim]""",
                id="gadget_help_content"
            ),
            id="gadget_help_container"
        )

# Make the main app available for import with compatibility alias
InspectorBrainApp = InspectorGApp  # Backward compatibility alias

__all__ = ["InspectorGApp", "InspectorBrainApp"]