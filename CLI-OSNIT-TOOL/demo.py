#!/usr/bin/env python3
"""
Inspector-G Demo Script
Shows off the current functionality and Inspector Gadget theming
"""

import sys
import time
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from src.ui.themes import theme
from src.core.config import settings

console = Console()

def show_banner():
    """Display the Inspector-G banner"""
    banner = theme.get_welcome_banner()
    console.print(Panel(banner, title="[bold blue]Inspector-G Demo[/bold blue]", border_style="bright_blue"))

def show_gadget_features():
    """Demonstrate Inspector Gadget features"""
    console.print("\n[bold yellow]🔍 Inspector Gadget Features Demo[/bold yellow]")

    # Show catchphrases
    console.print("\n[bold green]Gadget Catchphrases:[/bold green]")
    for msg_type in ["info", "success", "investigating", "warning"]:
        message = theme.format_gadget_message(f"This is a {msg_type} message", msg_type)
        console.print(f"  {message}")

    # Show ASCII art
    console.print("\n[bold green]Gadget ASCII Art:[/bold green]")
    art = theme.get_gadget_ascii_art()
    console.print(f"[cyan]{art}[/cyan]")

def show_available_commands():
    """Show available CLI commands"""
    console.print("\n[bold yellow]🚀 Available CLI Commands[/bold yellow]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Status", style="green")

    commands = [
        ("python inspectorbrain.py --help", "Show all commands with Inspector Gadget theming", "✅ Working"),
        ("python inspectorbrain.py version", "Version info with 'Wowser!' message", "✅ Working"),
        ("python inspectorbrain.py username <target>", "Username reconnaissance (stub)", "✅ Working"),
        ("python inspectorbrain.py email <domain>", "Email analysis (stub)", "✅ Working"),
        ("python inspectorbrain.py phone <number>", "Phone intelligence (stub)", "✅ Working"),
        ("python inspectorbrain.py domain <target>", "Domain scanning (stub)", "✅ Working"),
        ("python inspectorbrain.py ai '<query>'", "AI-powered analysis (stub)", "✅ Working"),
        ("python inspectorbrain.py tui", "Advanced TUI interface", "🔧 Needs fix"),
    ]

    for cmd, desc, status in commands:
        table.add_row(cmd, desc, status)

    console.print(table)

def show_theme_demo():
    """Demonstrate theme system"""
    console.print("\n[bold yellow]🎨 Theme System Demo[/bold yellow]")

    colors = theme.get_current_colors()
    console.print(f"\n[bold green]Current Theme:[/bold green] {settings.color_scheme}")

    # Show color palette
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Color", style="cyan")
    table.add_column("Hex Value", style="white")
    table.add_column("Preview", style="white")

    for name, color in colors.items():
        table.add_row(name.replace('_', ' ').title(), color, f"[{color}]████[/{color}]")

    console.print(table)

def simulate_investigation():
    """Simulate an OSINT investigation"""
    console.print("\n[bold yellow]🔍 Simulated Investigation Demo[/bold yellow]")

    target = "john.doe"
    console.print(f"\n[bold cyan]Go-Go-Gadget Username Search![/bold cyan]")
    console.print(f"[blue]Target:[/blue] {target}")

    # Simulate progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        platforms = ["GitHub", "Twitter", "LinkedIn", "Reddit", "Instagram"]

        for platform in platforms:
            task = progress.add_task(f"[cyan]Searching {platform}...", total=None)
            time.sleep(1)  # Simulate search time

            # Simulate result
            if platform in ["GitHub", "LinkedIn"]:
                console.print(f"  [green]✅ Found on {platform}[/green]")
            else:
                console.print(f"  [red]❌ Not found on {platform}[/red]")

            progress.remove_task(task)

    console.print(f"\n[bold green]🎉 Wowser! Investigation complete![/bold green]")

def show_configuration():
    """Show current configuration"""
    console.print("\n[bold yellow]⚙️ Configuration Demo[/bold yellow]")

    config_table = Table(show_header=True, header_style="bold magenta")
    config_table.add_column("Setting", style="cyan")
    config_table.add_column("Value", style="white")

    config_items = [
        ("App Name", settings.app_name),
        ("Theme", settings.color_scheme),
        ("Brain Mode", "ON" if settings.brain_mode else "OFF"),
        ("Gadget Commands", "ON" if settings.gadget_commands else "OFF"),
        ("Catchphrases", "ON" if settings.catchphrases_enabled else "OFF"),
        ("Wowser Notifications", "ON" if settings.wowser_notifications else "OFF"),
        ("AI Model", settings.default_ai_model),
    ]

    for setting, value in config_items:
        config_table.add_row(setting, str(value))

    console.print(config_table)

def show_project_status():
    """Show current project development status"""
    console.print("\n[bold yellow]📊 Project Status[/bold yellow]")

    status_table = Table(show_header=True, header_style="bold magenta")
    status_table.add_column("Phase", style="cyan")
    status_table.add_column("Component", style="white")
    status_table.add_column("Status", style="green")

    components = [
        ("Phase 1", "Project Structure", "✅ Complete"),
        ("Phase 1", "CLI Framework", "✅ Complete"),
        ("Phase 1", "Inspector Gadget Theming", "✅ Complete"),
        ("Phase 1", "Configuration System", "✅ Complete"),
        ("Phase 1", "Database Models", "✅ Complete"),
        ("Phase 1", "Development Environment", "✅ Complete"),
        ("Phase 1", "TUI Framework", "🔧 Needs theme fix"),
        ("Phase 2", "Username Reconnaissance", "🔧 Ready to implement"),
        ("Phase 2", "Email Intelligence", "🔧 Ready to implement"),
        ("Phase 2", "Phone Analysis", "🔧 Ready to implement"),
        ("Phase 2", "Domain Scanning", "🔧 Ready to implement"),
        ("Phase 3", "AI Integration", "🔧 Framework ready"),
    ]

    for phase, component, status in components:
        status_table.add_row(phase, component, status)

    console.print(status_table)

def main():
    """Main demo function"""
    try:
        show_banner()
        show_gadget_features()
        show_available_commands()
        show_theme_demo()
        show_configuration()
        show_project_status()

        console.print("\n[bold yellow]🎬 Live Investigation Demo[/bold yellow]")
        console.print("[dim]Press Ctrl+C to skip...[/dim]")

        try:
            simulate_investigation()
        except KeyboardInterrupt:
            console.print("\n[yellow]Demo skipped by user[/yellow]")

        console.print("\n" + "="*80)
        console.print("[bold green]🎉 Inspector-G Demo Complete![/bold green]")
        console.print("[bold blue]Like Brain the dog solving cases behind the scenes![/bold blue]")
        console.print("\nTry these commands:")
        console.print("  [cyan]python inspectorbrain.py --help[/cyan]")
        console.print("  [cyan]python inspectorbrain.py version[/cyan]")
        console.print("  [cyan]python inspectorbrain.py username testuser[/cyan]")
        console.print("\n[bold yellow]Go-Go-Gadget OSINT Investigation![/bold yellow] 🔍🕵️")

    except Exception as e:
        console.print(f"[red]Demo error: {e}[/red]")
        console.print("[yellow]Try: python inspectorbrain.py --help[/yellow]")

if __name__ == "__main__":
    main()