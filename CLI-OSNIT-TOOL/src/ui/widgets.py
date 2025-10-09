"""
Inspector-G Custom TUI Widgets

Custom Textual widgets with Inspector Gadget theming and advanced OSINT functionality.
Each widget represents a different aspect of the intelligence gathering interface.
"""

from textual.widgets import Static, Button, Input, DataTable, Log, Tree, Label, LoadingIndicator
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual import work
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional, Dict, Any, List
import asyncio
from datetime import datetime

from src.core.config import settings
from src.ui.themes import theme

class GadgetHeader(Static):
    """Inspector Gadget themed header with status and branding"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.brain_mode = settings.brain_mode

    def compose(self):
        colors = theme.get_current_colors()

        header_text = Text()
        header_text.append("🔍 ", style=f"bold {colors['accent']}")
        header_text.append("Inspector-G", style=f"bold {colors['primary']}")
        header_text.append(" - Advanced OSINT Suite", style=colors['text_muted'])

        if self.brain_mode:
            header_text.append(" 🧠", style=f"bold {colors['secondary']}")

        return Static(header_text)

    def update_status(self, status: str):
        """Update header with current operation status"""
        formatted_status = theme.format_gadget_message(status, "investigating")
        # TODO: Update header display with status

class WelcomeScreen(Container):
    """Welcome screen with Inspector Gadget branding and quick actions"""

    def compose(self):
        yield Static(theme.get_welcome_banner(), id="welcome_banner")

        yield Vertical(
            Static("[bold]Quick Start - Choose Your Investigation:[/bold]", id="quick_start_title"),
            Horizontal(
                Button("🔍 Username Search", id="btn_quick_username", variant="primary"),
                Button("📧 Email Analysis", id="btn_quick_email", variant="primary"),
                Button("📞 Phone Intel", id="btn_quick_phone", variant="primary"),
                Button("🌐 Domain Scan", id="btn_quick_domain", variant="primary"),
                id="quick_buttons"
            ),
            Static("\\n[dim]💡 Tip: Press F3 to toggle Brain mode for enhanced intelligence![/dim]"),
            id="welcome_content"
        )

    def on_button_pressed(self, event: Button.Pressed):
        """Handle quick start button presses"""
        button_map = {
            "btn_quick_username": "username",
            "btn_quick_email": "email",
            "btn_quick_phone": "phone",
            "btn_quick_domain": "domain"
        }

        tab_id = button_map.get(event.button.id)
        if tab_id:
            # Switch to the appropriate tab
            tabbed_content = self.app.query_one("TabbedContent")
            tabbed_content.active = tab_id

class InvestigationPanel(Container):
    """Main investigation panel for different OSINT modules"""

    def __init__(self, investigation_type: str, **kwargs):
        super().__init__(**kwargs)
        self.investigation_type = investigation_type
        self.is_investigating = reactive(False)
        self.results_data = []

    def compose(self):
        headers = theme.get_module_headers()
        header_text = headers.get(self.investigation_type, "Investigation Panel")

        yield Static(header_text, id=f"{self.investigation_type}_header")

        yield Horizontal(
            Vertical(
                Label("Target:"),
                Input(placeholder=f"Enter {self.investigation_type} target...", id=f"{self.investigation_type}_input"),
                Button(f"🚀 Go-Go-Gadget {self.investigation_type.title()}!", id=f"btn_{self.investigation_type}_start", variant="success"),
                Static("", id=f"{self.investigation_type}_status"),
                id=f"{self.investigation_type}_controls"
            ),
            Vertical(
                Label("Investigation Results:"),
                DataTable(id=f"{self.investigation_type}_results"),
                id=f"{self.investigation_type}_results_container"
            ),
            id=f"{self.investigation_type}_layout"
        )

    def on_mount(self):
        """Initialize the investigation panel"""
        results_table = self.query_one(f"#{self.investigation_type}_results", DataTable)

        # Setup table columns based on investigation type
        if self.investigation_type == "username":
            results_table.add_columns("Platform", "Username", "Status", "Profile URL")
        elif self.investigation_type == "email":
            results_table.add_columns("Email", "Domain", "Valid", "Source")
        elif self.investigation_type == "phone":
            results_table.add_columns("Number", "Carrier", "Location", "Social Media")
        elif self.investigation_type == "domain":
            results_table.add_columns("Subdomain", "IP Address", "Status", "Technologies")
        elif self.investigation_type == "ai":
            results_table.add_columns("Query", "Analysis", "Confidence", "Sources")

    def on_button_pressed(self, event: Button.Pressed):
        """Handle investigation start button"""
        if event.button.id == f"btn_{self.investigation_type}_start":
            target_input = self.query_one(f"#{self.investigation_type}_input", Input)
            target = target_input.value.strip()

            if target:
                self.start_investigation(target)
            else:
                self.notify("Please enter a target for investigation", severity="warning")

    @work(exclusive=True)
    async def start_investigation(self, target: str):
        """Start the investigation process"""
        self.is_investigating = True

        status_widget = self.query_one(f"#{self.investigation_type}_status", Static)
        status_widget.update(f"🔍 Investigating {target}...")

        # TODO: Implement actual investigation logic
        await self._simulate_investigation(target)

        self.is_investigating = False
        status_widget.update(theme.format_gadget_message("Investigation complete!", "success"))

    async def _simulate_investigation(self, target: str):
        """Simulate investigation process (to be replaced with real modules)"""
        results_table = self.query_one(f"#{self.investigation_type}_results", DataTable)

        # Simulate progressive results
        for i in range(3):
            await asyncio.sleep(2)  # Simulate processing time

            if self.investigation_type == "username":
                results_table.add_row(
                    f"Platform{i+1}",
                    target,
                    "Found" if i < 2 else "Not Found",
                    f"https://platform{i+1}.com/{target}" if i < 2 else "N/A"
                )
            elif self.investigation_type == "email":
                results_table.add_row(
                    f"{target}@example{i+1}.com",
                    f"example{i+1}.com",
                    "Valid" if i < 2 else "Invalid",
                    "OSINT Database"
                )
            # Add more simulation cases as needed

            self.notify(f"Found {i+1} results for {target}", severity="info")

class ResultsPanel(Container):
    """Panel for displaying and managing investigation results"""

    def compose(self):
        yield Static("📊 Investigation Results Archive", id="results_header")

        yield Horizontal(
            Vertical(
                Label("Recent Investigations:"),
                Tree("Investigations", id="investigations_tree"),
                id="investigations_sidebar"
            ),
            Vertical(
                Label("Selected Results:"),
                DataTable(id="selected_results"),
                Horizontal(
                    Button("📄 Export JSON", id="btn_export_json"),
                    Button("📊 Export CSV", id="btn_export_csv"),
                    Button("📋 Export PDF", id="btn_export_pdf"),
                    id="export_buttons"
                ),
                id="results_viewer"
            ),
            id="results_layout"
        )

    def on_mount(self):
        """Initialize results panel"""
        tree = self.query_one("#investigations_tree", Tree)
        results_table = self.query_one("#selected_results", DataTable)

        # Setup results table
        results_table.add_columns("Type", "Target", "Results", "Timestamp")

        # Add sample investigation history
        tree.root.add("🔍 Username Investigations")
        tree.root.add("📧 Email Investigations")
        tree.root.add("📞 Phone Investigations")
        tree.root.add("🌐 Domain Investigations")

    def on_button_pressed(self, event: Button.Pressed):
        """Handle export button presses"""
        export_map = {
            "btn_export_json": "JSON",
            "btn_export_csv": "CSV",
            "btn_export_pdf": "PDF"
        }

        format_type = export_map.get(event.button.id)
        if format_type:
            self.export_results(format_type)

    def export_results(self, format_type: str):
        """Export results in specified format"""
        # TODO: Implement actual export functionality
        message = f"Exporting results as {format_type}..."
        self.notify(theme.format_gadget_message(message, "info"), severity="info")

class StatusPanel(Container):
    """Bottom status panel with system information and progress"""

    def compose(self):
        yield Horizontal(
            Static(f"🧠 Brain Mode: {'ON' if settings.brain_mode else 'OFF'}", id="brain_status"),
            Static(f"🎨 Theme: {settings.color_scheme}", id="theme_status"),
            Static(f"🤖 AI: {settings.default_ai_model}", id="ai_status"),
            Static(f"⚙️ Status: Ready", id="system_status"),
            id="status_items"
        )

    def update_status(self, key: str, value: str):
        """Update a specific status item"""
        status_map = {
            "brain": "brain_status",
            "theme": "theme_status",
            "ai": "ai_status",
            "system": "system_status"
        }

        widget_id = status_map.get(key)
        if widget_id:
            widget = self.query_one(f"#{widget_id}", Static)
            # Update widget with new value
            # TODO: Implement status update logic