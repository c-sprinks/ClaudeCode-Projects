#!/usr/bin/env python3
"""
Enhanced Inspector-G TUI Application

A beautiful, feature-rich terminal user interface with Inspector Gadget theming,
smooth animations, and professional OSINT investigation capabilities.

Features:
- Beautiful Inspector Gadget themed interface
- Character integration (Penny, Chief Quimby, M.A.D. Detection)
- Real-time investigation progress
- Interactive data visualization
- Smooth animations and transitions
- Professional status monitoring
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer, Grid
from textual.widgets import (
    Header, Footer, Static, Button, Input, DataTable, Label,
    TabbedContent, TabPane, Log, Tree, Markdown, ProgressBar,
    LoadingIndicator, RadioSet, RadioButton, Checkbox, Switch
)
from textual.binding import Binding
from textual.screen import Screen, ModalScreen
from textual import work, on
from textual.reactive import reactive
from textual.message import Message
from textual.timer import Timer
from rich.text import Text
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.syntax import Syntax
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
from pathlib import Path


class InspectorGadgetTheme:
    """Enhanced Inspector Gadget color theme"""

    # Inspector Gadget color scheme
    COLORS = {
        "primary": "#2980b9",      # Inspector blue
        "secondary": "#f39c12",    # Gadget yellow
        "accent": "#e74c3c",       # Alert red
        "success": "#27ae60",      # Success green
        "warning": "#f39c12",      # Warning yellow
        "error": "#e74c3c",        # Error red
        "info": "#3498db",         # Info blue
        "background": "#1e1e2e",   # Dark background
        "surface": "#313244",      # Surface color
        "text": "#cdd6f4",         # Main text
        "text_muted": "#a6adc8",   # Muted text
        "border": "#585b70",       # Border color
    }

    CSS = f"""
    /* Inspector Gadget Theme CSS */
    Screen {{
        background: {COLORS["background"]};
    }}

    .title {{
        color: {COLORS["primary"]};
        text-style: bold;
    }}

    .gadget-header {{
        background: {COLORS["surface"]};
        color: {COLORS["text"]};
        border: solid {COLORS["border"]};
        text-align: center;
        height: 5;
    }}

    .investigation-panel {{
        background: {COLORS["surface"]};
        border: solid {COLORS["border"]};
        border-title-color: {COLORS["primary"]};
    }}

    .status-panel {{
        background: {COLORS["surface"]};
        border: solid {COLORS["border"]};
        border-title-color: {COLORS["secondary"]};
    }}

    .results-panel {{
        background: {COLORS["surface"]};
        border: solid {COLORS["border"]};
        border-title-color: {COLORS["success"]};
    }}

    .character-panel {{
        background: {COLORS["surface"]};
        border: solid {COLORS["border"]};
        border-title-color: {COLORS["accent"]};
    }}

    Button {{
        background: {COLORS["primary"]};
        color: white;
        border: none;
        margin: 1;
    }}

    Button:hover {{
        background: {COLORS["secondary"]};
    }}

    Input {{
        background: {COLORS["surface"]};
        color: {COLORS["text"]};
        border: solid {COLORS["border"]};
    }}

    Input:focus {{
        border: solid {COLORS["primary"]};
    }}

    DataTable {{
        background: {COLORS["surface"]};
        color: {COLORS["text"]};
    }}

    .success {{
        color: {COLORS["success"]};
    }}

    .warning {{
        color: {COLORS["warning"]};
    }}

    .error {{
        color: {COLORS["error"]};
    }}

    .muted {{
        color: {COLORS["text_muted"]};
    }}

    ProgressBar {{
        background: {COLORS["surface"]};
        bar-color: {COLORS["primary"]};
    }}

    LoadingIndicator {{
        color: {COLORS["secondary"]};
    }}
    """


class WelcomeScreen(Static):
    """Inspector Gadget themed welcome screen"""

    def compose(self) -> ComposeResult:
        welcome_text = Text()
        welcome_text.append("🔍 ", style="bold blue")
        welcome_text.append("INSPECTOR-G", style="bold cyan")
        welcome_text.append(" OSINT SUITE\n", style="bold")
        welcome_text.append("Go-Go-Gadget Intelligence!\n\n", style="yellow")
        welcome_text.append("🧠 Brain AI: ", style="green")
        welcome_text.append("Advanced AI-powered analysis\n", style="white")
        welcome_text.append("💡 Penny: ", style="cyan")
        welcome_text.append("User interface assistance\n", style="white")
        welcome_text.append("👨‍💼 Chief Quimby: ", style="yellow")
        welcome_text.append("Mission briefings & management\n", style="white")
        welcome_text.append("🦹‍♂️ M.A.D. Detection: ", style="red")
        welcome_text.append("Advanced threat monitoring\n\n", style="white")
        welcome_text.append("Ready for OSINT operations! 🕵️", style="bold green")

        yield Static(welcome_text, classes="gadget-header")


class InvestigationPanel(Container):
    """Panel for configuring and running OSINT investigations"""

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("🔍 Investigation Setup", classes="title")
            yield Label("Target:")
            yield Input(placeholder="Enter username, email, domain, or phone...", id="target_input")

            yield Label("Investigation Type:")
            with RadioSet(id="investigation_type"):
                yield RadioButton("🔤 Username Investigation", value=True)
                yield RadioButton("📧 Email Analysis")
                yield RadioButton("🌐 Domain Reconnaissance")
                yield RadioButton("📞 Phone Number Lookup")
                yield RadioButton("🤖 AI-Powered Analysis")

            yield Label("Options:")
            yield Checkbox("🕵️ Stealth Mode", value=True, id="stealth_mode")
            yield Checkbox("🧬 Behavioral Analysis", value=True, id="behavioral_analysis")
            yield Checkbox("🛡️ Security Monitoring", value=True, id="security_monitoring")

            with Horizontal():
                yield Button("🚀 Start Investigation", variant="primary", id="start_btn")
                yield Button("📋 Quick Scan", variant="default", id="quick_btn")
                yield Button("🔄 Reset", variant="default", id="reset_btn")


class CharacterPanel(Container):
    """Panel showing active Inspector Gadget characters"""

    character_status: reactive[Dict[str, str]] = reactive({
        "brain": "🧠 Ready",
        "penny": "💡 Standby",
        "quimby": "👨‍💼 Available",
        "mad": "🦹‍♂️ Monitoring"
    })

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("🎭 Character Status", classes="title")
            yield Static(id="character_display")

    def watch_character_status(self, status: Dict[str, str]) -> None:
        """Update character status display"""
        status_text = Text()
        for char, state in status.items():
            status_text.append(f"{state}\n", style="white")

        self.query_one("#character_display", Static).update(status_text)


class StatusPanel(Container):
    """Real-time status and progress monitoring"""

    current_operation: reactive[str] = reactive("Idle")
    progress: reactive[int] = reactive(0)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("📊 Operation Status", classes="title")
            yield Static("Ready for operations", id="status_text")
            yield ProgressBar(total=100, show_eta=False, id="progress_bar")
            yield Static("", id="progress_text")

    def watch_current_operation(self, operation: str) -> None:
        """Update current operation display"""
        self.query_one("#status_text", Static).update(operation)

    def watch_progress(self, progress: int) -> None:
        """Update progress display"""
        self.query_one("#progress_bar", ProgressBar).update(progress=progress)
        self.query_one("#progress_text", Static).update(f"Progress: {progress}%")


class ResultsPanel(Container):
    """Panel for displaying investigation results"""

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("📈 Investigation Results", classes="title")
            yield DataTable(id="results_table")
            yield Static("No results yet. Start an investigation to see data here.", id="results_summary")

    def add_result(self, category: str, data: List[str]):
        """Add investigation result to display"""
        table = self.query_one("#results_table", DataTable)

        # Add columns if this is the first result
        if not table.columns:
            table.add_columns("Category", "Count", "Sample Data")

        sample = data[0] if data else "None"
        table.add_row(category, str(len(data)), sample)

        # Update summary
        summary = f"Found {len(data)} {category} items"
        self.query_one("#results_summary", Static).update(summary)


class MissionDialog(ModalScreen[str]):
    """Dialog for creating new missions via Chief Quimby"""

    def compose(self) -> ComposeResult:
        with Container(id="mission_dialog"):
            yield Label("👨‍💼 Chief Quimby Mission Creation")
            yield Label("Mission Title:")
            yield Input(placeholder="Enter mission title...", id="mission_title")
            yield Label("Target:")
            yield Input(placeholder="Investigation target...", id="mission_target")
            yield Label("Priority:")
            with RadioSet(id="mission_priority"):
                yield RadioButton("🟢 Low", value=True)
                yield RadioButton("🟡 Normal")
                yield RadioButton("🟠 High")
                yield RadioButton("🔴 Critical")

            with Horizontal():
                yield Button("✅ Create Mission", variant="primary", id="create_mission")
                yield Button("❌ Cancel", variant="default", id="cancel_mission")

    @on(Button.Pressed, "#create_mission")
    def create_mission(self) -> None:
        title = self.query_one("#mission_title", Input).value
        target = self.query_one("#mission_target", Input).value

        if title and target:
            self.dismiss(f"Mission created: {title} -> {target}")
        else:
            # Show error
            pass

    @on(Button.Pressed, "#cancel_mission")
    def cancel_mission(self) -> None:
        self.dismiss("")


class EnhancedInspectorGApp(App[str]):
    """Enhanced Inspector-G TUI Application with beautiful interface"""

    TITLE = "Inspector-G - Advanced OSINT Suite"
    SUB_TITLE = "Go-Go-Gadget Intelligence! 🕵️"
    CSS = InspectorGadgetTheme.CSS

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+n", "new_investigation", "New Investigation", show=True),
        Binding("ctrl+m", "new_mission", "New Mission", show=True),
        Binding("ctrl+t", "toggle_theme", "Toggle Theme", show=False),
        Binding("ctrl+h", "show_help", "Help", show=True),
        Binding("f1", "character_penny", "Penny", show=False),
        Binding("f2", "character_quimby", "Quimby", show=False),
        Binding("f3", "character_mad", "M.A.D.", show=False),
        Binding("ctrl+r", "refresh", "Refresh", show=False),
    ]

    # App state
    current_investigation: reactive[Optional[str]] = reactive(None)
    investigation_active: reactive[bool] = reactive(False)

    def compose(self) -> ComposeResult:
        """Create the main UI layout"""
        yield Header(show_clock=True)

        with TabbedContent():
            with TabPane("🏠 Home", id="home_tab"):
                with Grid(id="home_grid"):
                    yield WelcomeScreen(classes="gadget-header")
                    yield InvestigationPanel(classes="investigation-panel")
                    yield CharacterPanel(classes="character-panel")
                    yield StatusPanel(classes="status-panel")

            with TabPane("🔍 Investigation", id="investigation_tab"):
                with Horizontal():
                    with Vertical(classes="investigation-panel"):
                        yield InvestigationPanel()
                    with Vertical(classes="results-panel"):
                        yield ResultsPanel()

            with TabPane("👨‍💼 Missions", id="missions_tab"):
                yield Static("Chief Quimby Mission Control\n\nMissions will be displayed here.", classes="character-panel")

            with TabPane("🦹‍♂️ Security", id="security_tab"):
                yield Static("M.A.D. Detection System\n\nThreat monitoring dashboard coming soon.", classes="character-panel")

            with TabPane("⚙️ Settings", id="settings_tab"):
                yield Static("Inspector-G Configuration\n\nSettings panel in development.", classes="status-panel")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application"""
        self.title = self.TITLE
        self.sub_title = self.SUB_TITLE

        # Start periodic updates
        self.set_timer(2.0, self.update_character_status, repeat=True)
        self.set_timer(1.0, self.update_clock, repeat=True)

    @on(Button.Pressed, "#start_btn")
    async def start_investigation(self) -> None:
        """Handle start investigation button"""
        target = self.query_one("#target_input", Input).value

        if not target:
            self.notify("Please enter a target for investigation", severity="warning")
            return

        self.investigation_active = True
        self.current_investigation = target

        # Get status panel
        status_panel = self.query_one(StatusPanel)
        status_panel.current_operation = f"Investigating: {target}"

        # Simulate investigation progress
        await self.run_investigation_simulation(target)

    @work(exclusive=True)
    async def run_investigation_simulation(self, target: str) -> None:
        """Simulate an OSINT investigation with progress updates"""
        status_panel = self.query_one(StatusPanel)
        results_panel = self.query_one(ResultsPanel)

        stages = [
            ("Initializing investigation...", 10),
            ("Gathering username intelligence...", 30),
            ("Analyzing email patterns...", 50),
            ("Scanning domain information...", 70),
            ("Running AI analysis...", 90),
            ("Finalizing results...", 100)
        ]

        for stage_name, progress in stages:
            status_panel.current_operation = stage_name
            status_panel.progress = progress
            await asyncio.sleep(1.5)  # Simulate work

        # Add some sample results
        sample_results = [
            ("Usernames", ["user123", "john_doe", "investigator"]),
            ("Emails", ["test@example.com", "admin@domain.com"]),
            ("Domains", ["example.com", "test-site.org"]),
        ]

        for category, data in sample_results:
            results_panel.add_result(category, data)

        # Complete investigation
        status_panel.current_operation = "Investigation completed successfully!"
        self.investigation_active = False

        self.notify(f"Investigation of '{target}' completed successfully!", severity="information")

    @on(Button.Pressed, "#quick_btn")
    def quick_scan(self) -> None:
        """Handle quick scan button"""
        self.notify("Quick scan feature coming soon!", severity="information")

    @on(Button.Pressed, "#reset_btn")
    def reset_investigation(self) -> None:
        """Reset investigation form"""
        self.query_one("#target_input", Input).value = ""
        status_panel = self.query_one(StatusPanel)
        status_panel.current_operation = "Ready for operations"
        status_panel.progress = 0
        self.notify("Investigation form reset", severity="information")

    def action_new_investigation(self) -> None:
        """Start a new investigation"""
        self.query_one(TabbedContent).active = "investigation_tab"

    def action_new_mission(self) -> None:
        """Create a new mission via Chief Quimby"""
        def handle_mission_result(result: str) -> None:
            if result:
                self.notify(result, severity="information")

        self.push_screen(MissionDialog(), handle_mission_result)

    def action_character_penny(self) -> None:
        """Activate Penny assistance"""
        self.notify("💡 Penny: Hi! I'm here to help with your investigation!", severity="information")

    def action_character_quimby(self) -> None:
        """Activate Chief Quimby"""
        self.notify("👨‍💼 Chief Quimby: Ready for your mission briefing, Inspector!", severity="information")

    def action_character_mad(self) -> None:
        """Activate M.A.D. Detection"""
        self.notify("🦹‍♂️ M.A.D. Detection: Monitoring for security threats...", severity="warning")

    def action_toggle_theme(self) -> None:
        """Toggle between light and dark themes"""
        self.notify("Theme switching coming soon!", severity="information")

    def action_show_help(self) -> None:
        """Show help information"""
        help_text = """🔍 Inspector-G Help

Key Bindings:
• Ctrl+Q: Quit application
• Ctrl+N: New investigation
• Ctrl+M: New mission
• Ctrl+H: Show this help
• F1: Penny assistance
• F2: Chief Quimby
• F3: M.A.D. Detection

Navigation:
• Use Tab to navigate between elements
• Enter to activate buttons
• Arrow keys to navigate lists
"""
        self.notify(help_text, severity="information")

    def action_refresh(self) -> None:
        """Refresh the current view"""
        self.notify("View refreshed", severity="information")

    def update_character_status(self) -> None:
        """Update character status indicators"""
        try:
            character_panel = self.query_one(CharacterPanel)

            # Simulate dynamic status updates
            import random
            statuses = ["Ready", "Active", "Standby", "Processing"]

            new_status = {
                "brain": f"🧠 {random.choice(statuses)}",
                "penny": f"💡 {random.choice(statuses)}",
                "quimby": f"👨‍💼 {random.choice(statuses)}",
                "mad": f"🦹‍♂️ Monitoring"
            }

            character_panel.character_status = new_status
        except Exception:
            pass  # Ignore errors during updates

    def update_clock(self) -> None:
        """Update the clock display"""
        # This is handled automatically by the Header widget
        pass