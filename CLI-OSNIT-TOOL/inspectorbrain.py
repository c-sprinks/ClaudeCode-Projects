#!/usr/bin/env python3
"""
Inspector-G - Advanced OSINT Terminal User Interface

Like Brain the dog who secretly solved Inspector Gadget's cases,
Inspector-G works behind the scenes to uncover digital intelligence.

Usage:
    python inspectorbrain.py                    # Launch TUI interface
    python inspectorbrain.py username john.doe  # Direct username search
    python inspectorbrain.py email target.com   # Direct email analysis
    python inspectorbrain.py domain example.com # Direct domain scan
    python inspectorbrain.py ai "search query"  # AI-powered analysis
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.core.app import InspectorGApp
from src.core.config import Settings, settings
from src.ui.themes import theme

console = Console()
app = typer.Typer(
    name="inspector-g",
    help="🧠 Inspector-G - Advanced OSINT TUI inspired by Inspector Gadget",
    rich_markup_mode="rich"
)

def display_gadget_banner():
    """Display Inspector Gadget themed banner"""
    banner = Text.assemble(
        ("🔍 ", "bright_blue"),
        ("Go-Go-Gadget Intelligence!", "bold bright_green"),
        (" 🕵️", "bright_blue"),
        "\n",
        ("Like Brain the dog, Inspector-G works behind the scenes", "dim"),
        "\n",
        ("to uncover digital intelligence and solve complex cases.", "dim")
    )

    panel = Panel(
        banner,
        title="[bold blue]Inspector-G OSINT Suite[/bold blue]",
        border_style="bright_blue",
        padding=(1, 2)
    )

    console.print(panel)

@app.command()
def tui():
    """Launch the advanced TUI interface"""
    display_gadget_banner()
    console.print("\n[yellow]Launching Inspector-G TUI...[/yellow]")

    try:
        brain_app = InspectorGApp()
        brain_app.run()
    except KeyboardInterrupt:
        console.print("\n[red]Operation cancelled by user[/red]")
    except Exception as e:
        console.print(f"\n[red]Error launching TUI: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def username(
    target: str = typer.Argument(..., help="Username to investigate"),
    platforms: Optional[str] = typer.Option(None, "--platforms", "-p", help="Comma-separated list of platforms (github,twitter,linkedin,reddit,instagram,youtube,tiktok,twitch)"),
    stealth: bool = typer.Option(True, "--stealth/--no-stealth", help="Enable stealth mode"),
    behavioral: bool = typer.Option(True, "--behavioral/--no-behavioral", help="Enable behavioral analysis"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file (JSON format)")
):
    """🔍 Go-Go-Gadget Quantum Username Investigation! Revolutionary username reconnaissance with behavioral fingerprinting"""

    try:
        console.print(f"[green]🧠 Go-Go-Gadget Quantum Username Investigation![/green]")
        console.print(f"[blue]Target:[/blue] {target}")

        if stealth:
            console.print(f"[yellow]🕵️ Stealth Mode:[/yellow] Maximum stealth protocols engaged")
        if behavioral:
            console.print(f"[yellow]🧬 Behavioral DNA:[/yellow] Cross-platform correlation enabled")

        console.print(f"[yellow]Status:[/yellow] Initializing Quantum Intelligence...")

        # Parse platform list
        platform_list = None
        if platforms:
            platform_list = [p.strip().lower() for p in platforms.split(',')]
            console.print(f"[blue]Platforms:[/blue] {', '.join(platform_list)}")

        # Run investigation asynchronously
        from src.modules.username import UsernameRecon

        async def run_investigation():
            username_recon = UsernameRecon()
            results = await username_recon.investigate_username(
                target_username=target,
                platforms=platform_list,
                enable_behavioral_analysis=behavioral,
                enable_stealth_mode=stealth,
                stealth_level=3 if stealth else 1
            )
            return results

        # Execute investigation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Running Quantum Investigation...", total=None)
            results = asyncio.run(run_investigation())
            progress.remove_task(task)

        # Display results
        console.print(f"\n[green]✅ Investigation Complete![/green]")

        # Summary display
        discoveries = results.get('discoveries', [])
        correlations = results.get('correlations', [])
        brain_analysis = results.get('brain_analysis', {})

        console.print(f"[blue]📊 Platform Discoveries:[/blue] {len(discoveries)}")
        for discovery in discoveries:
            confidence_color = "green" if discovery['confidence'] > 0.8 else "yellow" if discovery['confidence'] > 0.6 else "red"
            verification_emoji = "✅" if discovery['verification_status'] == 'verified' else "🔍"
            dna_emoji = "🧬" if discovery.get('behavioral_dna_available') else ""

            console.print(
                f"  {verification_emoji} [{confidence_color}]{discovery['platform']}[/{confidence_color}]: "
                f"{discovery['username']} ({discovery['confidence']:.1%}) {dna_emoji}"
            )

        if correlations:
            console.print(f"\n[blue]🔗 Cross-Platform Correlations:[/blue] {len(correlations)}")
            for correlation in correlations:
                console.print(
                    f"  🧬 {correlation['primary_username']}: "
                    f"{len(correlation['correlated_platforms'])} platforms "
                    f"({correlation['correlation_confidence']:.1%} confidence)"
                )

        # Brain's Analysis
        if brain_analysis:
            console.print(f"\n[blue]🧠 Brain's Analysis:[/blue]")
            console.print(f"  Pattern: {brain_analysis.get('pattern_analysis', 'Unknown')}")
            console.print(f"  Recommendation: {brain_analysis.get('brain_recommendation', 'None')}")

            if brain_analysis.get('ai_insights'):
                console.print(f"  🤖 AI Insights: {brain_analysis['ai_insights']}")

        # Duration and performance
        if 'duration_seconds' in results:
            console.print(f"\n[dim]Duration: {results['duration_seconds']:.1f} seconds[/dim]")

        # Output to file if requested
        if output:
            import json
            with open(output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            console.print(f"[green]📄 Results saved to {output}[/green]")

        # Inspector Gadget flourish
        console.print(f"\n[yellow]{results.get('gadget_catchphrase', theme.format_gadget_message('Investigation complete!', 'success'))}[/yellow]")

        if results.get('wowser_factor', 0) > 3:
            console.print(f"[bold green]🎉 Wowser! Outstanding discovery results![/bold green]")

    except KeyboardInterrupt:
        console.print(f"\n[yellow]⚠️ Investigation interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Investigation failed: {str(e)}[/red]")
        if settings.debug:
            console.print_exception()

@app.command()
def email(
    domain: str = typer.Argument(..., help="Domain to analyze for email patterns"),
    employees: Optional[str] = typer.Option(None, "--employees", "-e", help="File with employee names (one per line) or comma-separated list"),
    breach_analysis: bool = typer.Option(True, "--breach/--no-breach", help="Enable breach timeline analysis"),
    prediction: bool = typer.Option(True, "--predict/--no-predict", help="Enable predictive email generation"),
    validation: bool = typer.Option(False, "--validate/--no-validate", help="Enable email validation (careful - can be detected)"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file (JSON format)")
):
    """📧 Go-Go-Gadget Corporate Email Oracle! Revolutionary email intelligence with corporate psychology"""

    try:
        console.print(f"[green]🏢 Go-Go-Gadget Corporate Email Oracle![/green]")
        console.print(f"[blue]Domain:[/blue] {domain}")

        if breach_analysis:
            console.print(f"[yellow]🕰️ Breach Analysis:[/yellow] Timeline reconstruction enabled")
        if prediction:
            console.print(f"[yellow]🔮 Prediction Mode:[/yellow] Corporate psychology email generation")
        if validation:
            console.print(f"[yellow]⚠️ Validation Mode:[/yellow] Live email validation (stealth protocols)")

        console.print(f"[yellow]Status:[/yellow] Initializing Corporate Email Oracle...")

        # Parse employee list
        employee_list = None
        if employees:
            if employees.endswith('.txt'):
                # Read from file
                try:
                    with open(employees, 'r') as f:
                        employee_names = [line.strip() for line in f if line.strip()]
                    employee_list = []
                    for name in employee_names:
                        parts = name.split()
                        if len(parts) >= 2:
                            employee_list.append({
                                'full_name': name,
                                'first_name': parts[0],
                                'last_name': parts[-1]
                            })
                    console.print(f"[blue]Employees:[/blue] {len(employee_list)} loaded from file")
                except Exception as e:
                    console.print(f"[red]❌ Failed to read employee file: {e}[/red]")
            else:
                # Parse comma-separated list
                employee_names = [name.strip() for name in employees.split(',')]
                employee_list = []
                for name in employee_names:
                    parts = name.split()
                    if len(parts) >= 2:
                        employee_list.append({
                            'full_name': name,
                            'first_name': parts[0],
                            'last_name': parts[-1]
                        })
                console.print(f"[blue]Employees:[/blue] {len(employee_list)} provided")

        # Run investigation asynchronously
        from src.modules.email import EmailRecon

        async def run_investigation():
            email_recon = EmailRecon()
            results = await email_recon.investigate_domain_emails(
                target_domain=domain,
                employee_list=employee_list,
                enable_breach_analysis=breach_analysis,
                enable_prediction=prediction,
                enable_validation=validation
            )
            return results

        # Execute investigation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Running Corporate Email Oracle...", total=None)
            results = asyncio.run(run_investigation())
            progress.remove_task(task)

        # Display results
        console.print(f"\n[green]✅ Corporate Email Investigation Complete![/green]")

        # Summary display
        discovered = results.get('discovered_emails', [])
        predicted = results.get('predicted_emails', [])
        employees_found = results.get('employees_found', [])
        corporate_dna = results.get('corporate_dna', {})

        console.print(f"[blue]📧 Email Intelligence Results:[/blue]")
        console.print(f"  📬 Discovered Emails: {len(discovered)}")

        for email in discovered[:5]:  # Show first 5
            console.print(f"    ✅ {email}")

        if len(discovered) > 5:
            console.print(f"    ... and {len(discovered) - 5} more")

        console.print(f"  🔮 Predicted Emails: {len(predicted)}")

        for pred in predicted[:3]:  # Show top 3 predictions
            if isinstance(pred, dict):
                confidence_color = "green" if pred['confidence'] > 0.8 else "yellow" if pred['confidence'] > 0.6 else "red"
                console.print(
                    f"    🎯 [{confidence_color}]{pred['email']}[/{confidence_color}] "
                    f"({pred['confidence']:.1%} confidence)"
                )

        if len(predicted) > 3:
            console.print(f"    ... and {len(predicted) - 3} more predictions")

        # Corporate DNA
        if corporate_dna:
            console.print(f"\n[blue]🧬 Corporate DNA Analysis:[/blue]")
            console.print(f"  Confidence: {corporate_dna.get('confidence_score', 0):.1%}")
            console.print(f"  Email Providers: {', '.join(corporate_dna.get('email_providers', []))}")
            console.print(f"  Tech Sophistication: {corporate_dna.get('tech_sophistication', 0):.1%}")

        # Employee Intelligence
        if employees_found:
            console.print(f"\n[blue]👥 Employee Intelligence:[/blue] {len(employees_found)} identified")

        # Security Assessment
        security = results.get('security_assessment', {})
        if security:
            risk_level = security.get('overall_risk_level', 'unknown')
            risk_color = "red" if risk_level in ['critical', 'high'] else "yellow" if risk_level == 'medium' else "green"
            console.print(f"\n[blue]🛡️ Security Assessment:[/blue] [{risk_color}]{risk_level.upper()}[/{risk_color}] risk")

        # Brain's Analysis
        brain_analysis = results.get('brain_analysis', {})
        if brain_analysis:
            console.print(f"\n[blue]🧠 Brain's Analysis:[/blue]")
            console.print(f"  Pattern: {brain_analysis.get('pattern_analysis', 'Unknown')}")
            console.print(f"  Recommendation: {brain_analysis.get('brain_recommendation', 'None')}")

        # Duration and performance
        if 'duration_seconds' in results:
            console.print(f"\n[dim]Duration: {results['duration_seconds']:.1f} seconds[/dim]")

        # Output to file if requested
        if output:
            import json
            with open(output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            console.print(f"[green]📄 Results saved to {output}[/green]")

        # Inspector Gadget flourish
        console.print(f"\n[yellow]{results.get('gadget_catchphrase', theme.format_gadget_message('Email investigation complete!', 'success'))}[/yellow]")

        if results.get('wowser_factor', 0) > 10:
            console.print(f"[bold green]🎉 Wowser! Extensive email intelligence gathered![/bold green]")

    except KeyboardInterrupt:
        console.print(f"\n[yellow]⚠️ Investigation interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Corporate Email investigation failed: {str(e)}[/red]")
        if settings.debug:
            console.print_exception()

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
    """⚙️  Configuration management for Inspector-G"""
    if show:
        settings = Settings()
        console.print("[blue]Inspector-G Configuration:[/blue]")
        console.print(f"[dim]Config file: {settings.config_file}[/dim]")
        # TODO: Display actual configuration
    elif edit:
        console.print("[yellow]⚠️  Configuration editor under development[/yellow]")
    else:
        console.print("[red]Please specify --show or --edit[/red]")

@app.command()
def version():
    """Display Inspector-G version information"""
    console.print("[bold blue]Inspector-G OSINT Suite[/bold blue]")
    console.print("[dim]Version: 1.0.0-alpha[/dim]")
    console.print("[dim]Phase: Core Infrastructure Development[/dim]")
    console.print("\n[yellow]'Wowser! Go-Go-Gadget Intelligence!'[/yellow]")

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # No arguments - launch TUI by default
        display_gadget_banner()
        console.print("\n[yellow]Launching Inspector-G TUI... (use --help for CLI commands)[/yellow]")
        try:
            brain_app = InspectorGApp()
            brain_app.run()
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            console.print("[dim]Try: python inspectorbrain.py --help[/dim]")
    else:
        # CLI arguments provided - use typer
        app()

if __name__ == "__main__":
    main()