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

        # Penny's assistance for better understanding
        try:
            from src.characters.penny import penny

            # Create visualization data for Penny
            penny_data = {}
            if 'predicted_emails' in results and results['predicted_emails']:
                penny_data['emails'] = results['predicted_emails'][:10]  # First 10 for display
            if 'employees' in results:
                penny_data['employees'] = list(results['employees'].keys()) if isinstance(results['employees'], dict) else results['employees']

            if penny_data:
                console.print(f"\n[blue]💡 Penny's Analysis:[/blue]")
                explanation = penny.explain_results(penny_data, complexity="beginner")
                console.print(explanation)

                # Get next step suggestions
                suggestions = penny.suggest_next_steps(penny_data)
                if suggestions:
                    console.print(f"\n[green]🎯 Penny's Suggestions:[/green]")
                    for suggestion in suggestions[:3]:  # Show first 3 suggestions
                        console.print(f"• {suggestion}")

                # Offer Penny tip
                tip = penny.provide_tip("email")
                console.print(f"\n[yellow]💡 Penny's Tip:[/yellow] {tip.content}")

        except Exception as penny_error:
            # Don't let Penny errors break the main functionality
            pass

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
    execute: bool = typer.Option(False, "--execute", "-x", help="Execute the investigation plan"),
    model: Optional[str] = typer.Option("llama3.1", "--model", "-m", help="AI model to use")
):
    """🧠 Go-Go-Gadget Brain Analysis! Natural language OSINT queries with AI intelligence"""
    console.print(f"[green]🧠 Go-Go-Gadget Brain Analysis![/green]")
    console.print(f"[blue]Query:[/blue] {query}")
    console.print(f"[yellow]Brain Mode:[/yellow] {'Active' if settings.brain_mode else 'Passive'}")

    async def run_brain_analysis():
        from src.ai.brain import brain

        # Brain thinks about the query
        console.print(f"[yellow]Status:[/yellow] Brain is thinking...")
        with Progress(SpinnerColumn(), TextColumn("[yellow]Brain analyzing query...")) as progress:
            task = progress.add_task("thinking", total=None)
            investigation_plan = await brain.think_about_query(query)
            progress.update(task, completed=100)

        # Display Brain's analysis
        console.print(f"\n[green]✅ Brain's Strategic Analysis Complete![/green]")
        console.print(f"[blue]Investigation Type:[/blue] {investigation_plan['investigation_type']}")
        console.print(f"[blue]Complexity:[/blue] {investigation_plan['estimated_complexity']}")
        console.print(f"[blue]Risk Assessment:[/blue] {investigation_plan['risk_assessment']}")

        console.print(f"\n[yellow]🧠 Brain's Strategic Insight:[/yellow]")
        console.print(f"[dim]{investigation_plan['brain_insight']}[/dim]")

        console.print(f"\n[yellow]📋 Recommended Modules:[/yellow]")
        for module in investigation_plan['recommended_modules']:
            console.print(f"  • {module}")

        console.print(f"\n[yellow]🎯 Analysis Focus:[/yellow]")
        for focus in investigation_plan['analysis_focus']:
            console.print(f"  • {focus}")

        # Show Brain's thoughts
        if investigation_plan.get('brain_thoughts'):
            console.print(f"\n[yellow]💭 Brain's Thoughts:[/yellow]")
            for thought in investigation_plan['brain_thoughts']:
                confidence = f"({thought['confidence']:.0%})" if thought['confidence'] else ""
                console.print(f"  🧠 {thought['content']} {confidence}")

        # Execute if requested
        if execute:
            console.print(f"\n[green]🚀 Executing Brain's Investigation Plan...[/green]")

            # Extract target from query (prioritize domains and emails)
            import re
            # Look for domains and emails first (better targeting)
            email_targets = re.findall(r'[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}', query)
            domain_targets = re.findall(r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b', query)

            # Use entities from Brain's analysis if available
            entities = investigation_plan.get('entities', [])
            entity_targets = [e['value'] for e in entities if e['type'] in ['domain', 'email', 'username']]

            # Priority: entities > emails > domains > first meaningful word
            if entity_targets:
                target = entity_targets[0]
            elif email_targets:
                target = email_targets[0]
            elif domain_targets:
                target = domain_targets[0]
            else:
                # Fallback to extracting meaningful words (skip common words)
                words = query.split()
                skip_words = {'investigate', 'analyze', 'find', 'search', 'for', 'the', 'a', 'an', 'patterns', 'in', 'on'}
                meaningful_words = [word.strip('.,!?') for word in words if word.lower() not in skip_words and len(word) > 2]
                target = meaningful_words[0] if meaningful_words else "unknown"

            with Progress(SpinnerColumn(), TextColumn("[yellow]Brain coordinating investigation...")) as progress:
                task = progress.add_task("investigating", total=None)
                investigation = await brain.coordinate_investigation(
                    target,
                    investigation_plan['investigation_type'],
                    investigation_plan['recommended_modules']
                )
                progress.update(task, completed=100)

            # Display investigation results
            summary = await brain.get_investigation_summary(investigation)
            console.print(f"\n{summary}")
        else:
            console.print(f"\n[dim]Use --execute to run Brain's investigation plan[/dim]")

        console.print(f"\n{investigation_plan.get('brain_catchphrase', '🧠 Woof!')}")

    try:
        asyncio.run(run_brain_analysis())
    except KeyboardInterrupt:
        console.print("\n[red]Brain analysis interrupted by user[/red]")
    except Exception as e:
        console.print(f"\n[red]Brain analysis error: {e}[/red]")

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
def penny(
    action: str = typer.Argument(help="Action: greet, tip, help, visualize"),
    data: Optional[str] = typer.Option(None, "--data", help="JSON data for visualization"),
    complexity: str = typer.Option("beginner", "--complexity", help="Explanation complexity: beginner, intermediate, advanced"),
    category: str = typer.Option("general", "--category", help="Tip category: general, username, email, domain")
):
    """💡 Go-Go-Gadget Penny! User interface assistance and data visualization"""

    from src.characters.penny import penny

    console.print("[bold blue]💡 Penny - Your OSINT Assistant[/bold blue]")
    console.print("=" * 50)

    if action == "greet":
        greeting = penny.greet_user()
        console.print(f"\n[green]{greeting}[/green]")

    elif action == "tip":
        tip = penny.provide_tip(category)
        console.print(f"\n[yellow]💡 {tip.title}[/yellow]")
        console.print(f"[dim]Category: {tip.category} | Difficulty: {tip.difficulty}[/dim]")
        console.print(f"\n{tip.content}")
        if tip.example:
            console.print(f"\n[blue]Example:[/blue] {tip.example}")

    elif action == "help":
        console.print("\n[green]How I can help you:[/green]")
        console.print("• 📊 Create visualizations from your OSINT data")
        console.print("• 💡 Provide helpful tips and techniques")
        console.print("• 📋 Explain investigation results in simple terms")
        console.print("• 🎯 Suggest next steps for your investigations")
        console.print("• 📈 Generate progress reports")

        console.print(f"\n[blue]Available commands:[/blue]")
        console.print("• penny greet - Get a friendly greeting")
        console.print("• penny tip --category [general|username|email] - Get helpful tips")
        console.print("• penny help - Show this help message")
        console.print("• penny visualize --data '{...}' - Create visualizations")

    elif action == "visualize":
        if not data:
            console.print("[red]Please provide data with --data option[/red]")
            console.print("[dim]Example: penny visualize --data '{\"usernames\": [\"user1\", \"user2\"], \"emails\": [\"test@example.com\"]}'[/dim]")
            return

        try:
            import json
            parsed_data = json.loads(data)

            # Create visualization
            viz = penny.create_visualization(parsed_data)

            console.print(f"\n[yellow]📊 {viz.title}[/yellow]")
            console.print(f"[dim]Type: {viz.viz_type}[/dim]")
            console.print(f"\n{viz.description}")

            # Display formatted data
            formatted = penny.format_for_display(parsed_data)
            console.print(f"\n{formatted}")

            # Show insights
            if viz.insights:
                console.print(f"\n[blue]💡 Penny's Insights:[/blue]")
                for insight in viz.insights:
                    console.print(f"• {insight}")

            # Suggest next steps
            suggestions = penny.suggest_next_steps(parsed_data)
            if suggestions:
                console.print(f"\n[green]🎯 Suggested Next Steps:[/green]")
                for suggestion in suggestions:
                    console.print(f"• {suggestion}")

        except json.JSONDecodeError:
            console.print("[red]Invalid JSON data provided[/red]")
        except Exception as e:
            console.print(f"[red]Visualization error: {e}[/red]")

    else:
        console.print(f"[red]Unknown action: {action}[/red]")
        console.print("[dim]Available actions: greet, tip, help, visualize[/dim]")

    # Penny's signature
    console.print(f"\n[yellow]💡 Penny says: \"Always happy to help with your investigations!\"[/yellow]")

@app.command()
def quimby(
    action: str = typer.Argument(help="Action: brief, mission, status, list"),
    target: Optional[str] = typer.Option(None, "--target", help="Investigation target"),
    case_type: Optional[str] = typer.Option("individual", "--type", help="Case type: individual, corporate, infrastructure, threat_intel"),
    priority: Optional[str] = typer.Option("normal", "--priority", help="Priority: low, normal, high, critical"),
    mission_id: Optional[str] = typer.Option(None, "--mission-id", help="Mission ID for status/updates")
):
    """👨‍💼 Go-Go-Gadget Chief Quimby! Mission briefings and case management"""

    from src.characters.chief_quimby import chief_quimby, CaseType, MissionPriority

    console.print("[bold blue]👨‍💼 Chief Quimby - Mission Control[/bold blue]")
    console.print("=" * 50)

    if action == "brief":
        greeting = chief_quimby.greet_agent("Inspector")
        console.print(f"\n[yellow]{greeting}[/yellow]")

        console.print(f"\n[green]How Chief Quimby can assist:[/green]")
        console.print("• 📋 Create mission briefings for OSINT operations")
        console.print("• 📊 Track investigation progress and status")
        console.print("• 🎯 Manage multiple cases and priorities")
        console.print("• 📈 Provide strategic oversight and guidance")
        console.print("• 📝 Generate detailed mission reports")

        console.print(f"\n[blue]Available commands:[/blue]")
        console.print("• quimby mission --target [TARGET] --type [TYPE] - Create new mission")
        console.print("• quimby status --mission-id [ID] - Check mission status")
        console.print("• quimby list - List all active missions")

    elif action == "mission":
        if not target:
            console.print("[red]Target required for mission creation[/red]")
            console.print("[dim]Example: quimby mission --target john_doe --type individual --priority high[/dim]")
            return

        try:
            # Parse case type
            case_type_map = {
                "individual": CaseType.INDIVIDUAL,
                "corporate": CaseType.CORPORATE,
                "infrastructure": CaseType.INFRASTRUCTURE,
                "threat_intel": CaseType.THREAT_INTEL,
                "background": CaseType.BACKGROUND,
                "surveillance": CaseType.SURVEILLANCE,
                "forensic": CaseType.FORENSIC
            }
            case_enum = case_type_map.get(case_type.lower(), CaseType.INDIVIDUAL)

            # Parse priority
            priority_map = {
                "low": MissionPriority.LOW,
                "normal": MissionPriority.NORMAL,
                "high": MissionPriority.HIGH,
                "critical": MissionPriority.CRITICAL,
                "classified": MissionPriority.CLASSIFIED
            }
            priority_enum = priority_map.get(priority.lower(), MissionPriority.NORMAL)

            # Create mission
            title = f"OSINT Investigation: {target}"
            mission = chief_quimby.create_mission(
                title=title,
                target=target,
                case_type=case_enum,
                priority=priority_enum,
                deadline_hours=24 if priority_enum in [MissionPriority.HIGH, MissionPriority.CRITICAL] else None
            )

            # Generate initial briefing
            briefing = chief_quimby.generate_briefing(mission, "initial")

            console.print(f"\n[green]✅ Mission Created: {mission.mission_id}[/green]")
            console.print(f"[dim]Target: {target} | Type: {case_type} | Priority: {priority}[/dim]")

            # Display briefing
            formatted_briefing = chief_quimby.format_briefing_display(briefing)
            console.print(formatted_briefing)

        except Exception as e:
            console.print(f"[red]Mission creation error: {e}[/red]")

    elif action == "status":
        if not mission_id:
            console.print("[red]Mission ID required for status check[/red]")
            console.print("[dim]Example: quimby status --mission-id MISSION-ABC123[/dim]")
            return

        status = chief_quimby.get_mission_status(mission_id)
        if not status:
            console.print(f"[red]Mission {mission_id} not found[/red]")
            return

        console.print(f"\n[yellow]📊 Mission Status Report[/yellow]")
        console.print(f"Mission ID: [blue]{status['mission_id']}[/blue]")
        console.print(f"Title: {status['title']}")
        console.print(f"Target: [green]{status['target']}[/green]")
        console.print(f"Status: [yellow]{status['status'].title()}[/yellow]")
        console.print(f"Progress: [blue]{status['progress']}%[/blue]")
        console.print(f"Priority: [red]{status['priority'].upper()}[/red]")
        console.print(f"Findings: {status['findings_count']} categories")
        console.print(f"Notes: {status['notes_count']} entries")

        if status['deadline']:
            console.print(f"Deadline: {status['deadline']}")
            if status['time_remaining']:
                time_color = "red" if "OVERDUE" in status['time_remaining'] else "yellow"
                console.print(f"Time Remaining: [{time_color}]{status['time_remaining']}[/{time_color}]")

    elif action == "list":
        missions = chief_quimby.list_active_missions()

        if not missions:
            console.print("[yellow]No active missions found[/yellow]")
            console.print("[dim]Create a new mission with: quimby mission --target [TARGET][/dim]")
            return

        console.print(f"\n[yellow]📋 Active Missions ({len(missions)})[/yellow]")
        console.print("=" * 80)

        for mission in missions:
            status_color = {
                "assigned": "blue",
                "in_progress": "yellow",
                "completed": "green",
                "cancelled": "red"
            }.get(mission['status'], "white")

            priority_emoji = {
                "low": "📝",
                "normal": "📋",
                "high": "⚠️",
                "critical": "🚨",
                "classified": "🔒"
            }.get(mission['priority'], "📋")

            console.print(f"{priority_emoji} [blue]{mission['mission_id']}[/blue] - {mission['title']}")
            console.print(f"   Target: [green]{mission['target']}[/green] | Status: [{status_color}]{mission['status'].title()}[/{status_color}] | Progress: {mission['progress']}%")

            if mission['time_remaining']:
                time_color = "red" if "OVERDUE" in mission['time_remaining'] else "yellow"
                console.print(f"   Deadline: [{time_color}]{mission['time_remaining']}[/{time_color}]")

            console.print("")

    else:
        console.print(f"[red]Unknown action: {action}[/red]")
        console.print("[dim]Available actions: brief, mission, status, list[/dim]")

    # Chief Quimby's signature
    console.print(f"\n[yellow]👨‍💼 Chief Quimby: \"Remember, Inspector - the success of this operation depends on your expertise!\"[/yellow]")

@app.command()
def mad(
    action: str = typer.Argument(..., help="Action: analyze, alerts, summary, indicators"),
    target: Optional[str] = typer.Option(None, "--target", help="Target for threat analysis"),
    data: Optional[str] = typer.Option(None, "--data", help="JSON data file for analysis"),
    alert_id: Optional[str] = typer.Option(None, "--alert-id", help="Alert ID for specific operations")
):
    """🦹‍♂️ Go-Go-Gadget M.A.D. Detection! Advanced threat analysis and security monitoring"""

    console.print("[bold red]🦹‍♂️ M.A.D. Detection System[/bold red]")
    console.print("=" * 50)

    try:
        from src.characters.mad_detection import mad_detection

        if action == "analyze":
            if not target:
                console.print("[red]❌ Target required for threat analysis[/red]")
                console.print("[dim]Usage: python inspectorbrain.py mad analyze --target example.com[/dim]")
                return

            # Greeting
            greeting = mad_detection.greet_agent("Inspector-G")
            console.print(f"[yellow]{greeting}[/yellow]\n")

            console.print(f"[blue]🔍 Analyzing target:[/blue] {target}")
            console.print("[yellow]🔄 Running comprehensive threat analysis...[/yellow]")

            # Create sample OSINT data for demonstration
            # In a real implementation, this would come from actual OSINT gathering
            sample_osint_data = {
                "target": target,
                "domains": [target] if "." in target else [f"{target}.com", f"{target}.org"],
                "emails": [f"admin@{target}", f"contact@{target}"] if "." in target else [f"{target}@gmail.com", f"{target}@yahoo.com"],
                "usernames": [target.split('.')[0] if "." in target else target]
            }

            # Perform threat analysis
            analysis_results = mad_detection.analyze_target(target, sample_osint_data)

            # Display formatted report
            threat_report = mad_detection.format_threat_report(analysis_results)
            console.print(threat_report)

        elif action == "alerts":
            console.print("[blue]🚨 Security Alerts Dashboard[/blue]\n")

            active_alerts = [alert for alert in mad_detection.security_alerts if alert.status == "open"]

            if active_alerts:
                console.print(f"[red]Active Alerts: {len(active_alerts)}[/red]\n")

                for alert in active_alerts[-5:]:  # Show last 5 alerts
                    risk_color = "red" if alert.risk_score >= 7.0 else "yellow" if alert.risk_score >= 4.0 else "green"
                    level_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "informational": "ℹ️"}.get(alert.threat_level.value, "❓")

                    console.print(f"{level_emoji} [blue]{alert.alert_id}[/blue] - {alert.title}")
                    console.print(f"   Risk Score: [{risk_color}]{alert.risk_score:.1f}/10.0[/{risk_color}] | Status: {alert.status}")
                    console.print(f"   Created: {alert.created_at.strftime('%Y-%m-%d %H:%M')}")
                    console.print(f"   Indicators: {len(alert.indicators)} identified\n")
            else:
                console.print("[green]✅ No active security alerts[/green]")

        elif action == "summary":
            console.print("[blue]📊 M.A.D. Detection System Summary[/blue]\n")

            summary = mad_detection.get_threat_summary()

            console.print(f"[blue]Total Threat Indicators:[/blue] {summary['total_indicators']}")
            console.print(f"[red]Active Security Alerts:[/red] {summary['active_alerts']}")
            console.print(f"[blue]Risk Assessments:[/blue] {summary['total_assessments']}")
            console.print(f"[orange]High-Risk Indicators:[/orange] {summary['high_risk_indicators']}")
            console.print(f"[yellow]Recent Alerts (7 days):[/yellow] {summary['recent_alerts']}")

            # System status
            if summary['active_alerts'] > 0:
                console.print(f"\n[red]🚨 System Status: {summary['active_alerts']} active threat(s) require attention[/red]")
            else:
                console.print(f"\n[green]✅ System Status: All clear - no active threats detected[/green]")

        elif action == "indicators":
            console.print("[blue]🔍 Threat Indicators Database[/blue]\n")

            if mad_detection.threat_indicators:
                # Group by threat level
                by_level = {}
                for indicator in mad_detection.threat_indicators:
                    level = indicator.threat_level.value
                    if level not in by_level:
                        by_level[level] = []
                    by_level[level].append(indicator)

                for level in ["critical", "high", "medium", "low", "informational"]:
                    if level in by_level:
                        level_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "informational": "ℹ️"}[level]
                        console.print(f"{level_emoji} [bold]{level.upper()}[/bold] ({len(by_level[level])} indicators)")

                        for indicator in by_level[level][:3]:  # Show first 3 per level
                            console.print(f"   • {indicator.indicator_type.upper()}: {indicator.indicator_value}")
                            console.print(f"     {indicator.description} (Confidence: {indicator.confidence:.1%})")

                        if len(by_level[level]) > 3:
                            console.print(f"     ... and {len(by_level[level]) - 3} more")
                        console.print("")
            else:
                console.print("[green]No threat indicators in database[/green]")

        else:
            console.print(f"[red]Unknown action: {action}[/red]")
            console.print("[dim]Available actions: analyze, alerts, summary, indicators[/dim]")

    except Exception as e:
        console.print(f"[red]❌ M.A.D. Detection System error: {str(e)}[/red]")
        if settings.debug:
            console.print_exception()

    # M.A.D. Detection signature
    console.print(f"\n[red]🦹‍♂️ M.A.D. Detection: \"Threat analysis complete. Stay vigilant, Inspector.\"[/red]")

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