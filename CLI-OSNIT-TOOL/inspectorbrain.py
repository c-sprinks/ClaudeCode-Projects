#!/usr/bin/env python3
"""
InspectorBrain - Advanced OSINT Terminal User Interface

Like Brain the dog who secretly solved Inspector Gadget's cases,
InspectorBrain works behind the scenes to uncover digital intelligence.

Usage:
    python inspectorbrain.py                    # Launch TUI interface
    python inspectorbrain.py username john.doe  # Direct username search
    python inspectorbrain.py email target.com   # Direct email analysis
    python inspectorbrain.py domain example.com # Direct domain scan
    python inspectorbrain.py ai "search query"  # AI-powered analysis
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.core.app import InspectorBrainApp
from src.core.config import Settings

console = Console()
app = typer.Typer(
    name="inspectorbrain",
    help="🧠 InspectorBrain - Advanced OSINT TUI inspired by Inspector Gadget",
    rich_markup_mode="rich"
)

def display_gadget_banner():
    """Display Inspector Gadget themed banner"""
    banner = Text.assemble(
        ("🔍 ", "bright_blue"),
        ("Go-Go-Gadget Intelligence!", "bold bright_green"),
        (" 🕵️", "bright_blue"),
        "\n",
        ("Like Brain the dog, InspectorBrain works behind the scenes", "dim"),
        "\n",
        ("to uncover digital intelligence and solve complex cases.", "dim")
    )

    panel = Panel(
        banner,
        title="[bold blue]InspectorBrain OSINT Suite[/bold blue]",
        border_style="bright_blue",
        padding=(1, 2)
    )

    console.print(panel)

@app.command()
def tui():
    """Launch the advanced TUI interface"""
    display_gadget_banner()
    console.print("\n[yellow]Launching InspectorBrain TUI...[/yellow]")

    try:
        brain_app = InspectorBrainApp()
        brain_app.run()
    except KeyboardInterrupt:
        console.print("\n[red]Operation cancelled by user[/red]")
    except Exception as e:
        console.print(f"\n[red]Error launching TUI: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def username(
    target: str = typer.Argument(..., help="Username to investigate"),
    platforms: Optional[str] = typer.Option(None, "--platforms", "-p", help="Comma-separated platforms to check"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for results")
):
    """🔍 Go-Go-Gadget Username Search! Investigate usernames across platforms"""
    console.print(f"[green]🔍 Go-Go-Gadget Username Search![/green]")
    console.print(f"[blue]Target:[/blue] {target}")

    # TODO: Implement custom username reconnaissance
    console.print("[yellow]⚠️  Custom username reconnaissance module under development[/yellow]")
    console.print("[dim]This will search across social media, forums, and public databases[/dim]")

@app.command()
def email(
    domain: str = typer.Argument(..., help="Domain to analyze for email patterns"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for results")
):
    """📧 Go-Go-Gadget Email Analysis! Discover email patterns and addresses"""
    console.print(f"[green]📧 Go-Go-Gadget Email Analysis![/green]")
    console.print(f"[blue]Domain:[/blue] {domain}")

    # TODO: Implement custom email harvesting
    console.print("[yellow]⚠️  Custom email intelligence module under development[/yellow]")
    console.print("[dim]This will harvest emails and analyze patterns[/dim]")

@app.command()
def phone(
    number: str = typer.Argument(..., help="Phone number to analyze"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for results")
):
    """📞 Go-Go-Gadget Phone Analysis! Investigate phone numbers"""
    console.print(f"[green]📞 Go-Go-Gadget Phone Analysis![/green]")
    console.print(f"[blue]Number:[/blue] {number}")

    # TODO: Implement custom phone intelligence
    console.print("[yellow]⚠️  Custom phone intelligence module under development[/yellow]")
    console.print("[dim]This will analyze carrier, location, and social media footprints[/dim]")

@app.command()
def domain(
    target: str = typer.Argument(..., help="Domain to investigate"),
    deep: bool = typer.Option(False, "--deep", help="Perform deep reconnaissance"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for results")
):
    """🌐 Go-Go-Gadget Domain Scan! Comprehensive domain reconnaissance"""
    console.print(f"[green]🌐 Go-Go-Gadget Domain Scan![/green]")
    console.print(f"[blue]Target:[/blue] {target}")

    # TODO: Implement custom domain reconnaissance
    console.print("[yellow]⚠️  Custom domain reconnaissance module under development[/yellow]")
    console.print("[dim]This will perform subdomain discovery, port scanning, and analysis[/dim]")

@app.command()
def ai(
    query: str = typer.Argument(..., help="Natural language OSINT query"),
    model: Optional[str] = typer.Option("llama3.1", "--model", "-m", help="AI model to use")
):
    """🤖 Go-Go-Gadget AI Analysis! Natural language OSINT queries"""
    console.print(f"[green]🤖 Go-Go-Gadget AI Analysis![/green]")
    console.print(f"[blue]Query:[/blue] {query}")

    # TODO: Implement AI query processing
    console.print("[yellow]⚠️  AI integration module under development[/yellow]")
    console.print("[dim]This will process natural language queries and route to appropriate tools[/dim]")

@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    edit: bool = typer.Option(False, "--edit", help="Edit configuration file")
):
    """⚙️  Configuration management for InspectorBrain"""
    if show:
        settings = Settings()
        console.print("[blue]InspectorBrain Configuration:[/blue]")
        console.print(f"[dim]Config file: {settings.config_file}[/dim]")
        # TODO: Display actual configuration
    elif edit:
        console.print("[yellow]⚠️  Configuration editor under development[/yellow]")
    else:
        console.print("[red]Please specify --show or --edit[/red]")

@app.command()
def version():
    """Display InspectorBrain version information"""
    console.print("[bold blue]InspectorBrain OSINT Suite[/bold blue]")
    console.print("[dim]Version: 1.0.0-alpha[/dim]")
    console.print("[dim]Phase: Core Infrastructure Development[/dim]")
    console.print("\n[yellow]'Wowser! Go-Go-Gadget Intelligence!'[/yellow]")

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # No arguments - launch TUI by default
        display_gadget_banner()
        console.print("\n[yellow]Launching InspectorBrain TUI... (use --help for CLI commands)[/yellow]")
        try:
            brain_app = InspectorBrainApp()
            brain_app.run()
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            console.print("[dim]Try: python inspectorbrain.py --help[/dim]")
    else:
        # CLI arguments provided - use typer
        app()

if __name__ == "__main__":
    main()