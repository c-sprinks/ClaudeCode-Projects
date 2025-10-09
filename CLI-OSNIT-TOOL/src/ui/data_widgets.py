#!/usr/bin/env python3
"""
Advanced Data Visualization Widgets for Inspector-G TUI

Professional data visualization components with cybersecurity aesthetics,
real-time updates, and interactive features for OSINT intelligence display.

Features:
- Real-time metrics dashboard
- Interactive charts and graphs
- Intelligence correlation matrices
- Threat level indicators
- Network topology visualization
- Timeline analysis widgets
"""

from textual.widgets import Static, DataTable, ProgressBar
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.reactive import reactive
from textual import work, on
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import random
import math


class IntelligenceMetricsWidget(Container):
    """Real-time intelligence metrics dashboard"""

    total_investigations: reactive[int] = reactive(0)
    active_threats: reactive[int] = reactive(0)
    data_points: reactive[int] = reactive(0)
    success_rate: reactive[float] = reactive(0.0)

    def compose(self):
        with Container(classes="intelligence-panel"):
            yield Static("Intelligence Metrics", classes="title interactive")
            yield Static("", id="metrics_display", classes="metric-updating")

    def watch_total_investigations(self, count: int) -> None:
        self._update_metrics()

    def watch_active_threats(self, count: int) -> None:
        self._update_metrics()

    def watch_data_points(self, count: int) -> None:
        self._update_metrics()

    def watch_success_rate(self, rate: float) -> None:
        self._update_metrics()

    def _update_metrics(self) -> None:
        """Update the metrics display"""
        metrics_text = Text()

        # Format metrics with professional styling
        metrics_text.append("╭─ OSINT METRICS ───────────────────╮\n", style="dim cyan")

        metrics_text.append("│ ", style="dim cyan")
        metrics_text.append(f"Investigations: ", style="white")
        metrics_text.append(f"{self.total_investigations:,}", style="bold green")
        metrics_text.append(" " * (32 - len(f"Investigations: {self.total_investigations:,}")), style="white")
        metrics_text.append("│\n", style="dim cyan")

        metrics_text.append("│ ", style="dim cyan")
        metrics_text.append(f"Active Threats: ", style="white")
        color = "red" if self.active_threats > 5 else "yellow" if self.active_threats > 0 else "green"
        metrics_text.append(f"{self.active_threats}", style=f"bold {color}")
        metrics_text.append(" " * (32 - len(f"Active Threats: {self.active_threats}")), style="white")
        metrics_text.append("│\n", style="dim cyan")

        metrics_text.append("│ ", style="dim cyan")
        metrics_text.append(f"Data Points: ", style="white")
        metrics_text.append(f"{self.data_points:,}", style="bold cyan")
        metrics_text.append(" " * (32 - len(f"Data Points: {self.data_points:,}")), style="white")
        metrics_text.append("│\n", style="dim cyan")

        metrics_text.append("│ ", style="dim cyan")
        metrics_text.append(f"Success Rate: ", style="white")
        rate_color = "green" if self.success_rate >= 0.8 else "yellow" if self.success_rate >= 0.6 else "red"
        metrics_text.append(f"{self.success_rate:.1%}", style=f"bold {rate_color}")
        metrics_text.append(" " * (32 - len(f"Success Rate: {self.success_rate:.1%}")), style="white")
        metrics_text.append("│\n", style="dim cyan")

        metrics_text.append("╰───────────────────────────────────╯", style="dim cyan")

        self.query_one("#metrics_display", Static).update(metrics_text)


class ThreatLevelIndicator(Container):
    """Visual threat level indicator with animations"""

    threat_level: reactive[str] = reactive("LOW")
    threat_score: reactive[float] = reactive(0.0)

    def compose(self):
        with Container(classes="security-panel"):
            yield Static("Threat Assessment", classes="title")
            yield Static("", id="threat_display")
            yield ProgressBar(total=100, show_percentage=True, id="threat_bar")

    def watch_threat_level(self, level: str) -> None:
        self._update_threat_display()

    def watch_threat_score(self, score: float) -> None:
        self._update_threat_display()
        # Update progress bar
        self.query_one("#threat_bar", ProgressBar).update(progress=int(score * 100))

    def _update_threat_display(self) -> None:
        """Update threat level display with visual indicators"""
        threat_text = Text()

        # Threat level indicators
        indicators = {
            "LOW": ("🟢", "green", "MINIMAL RISK"),
            "MEDIUM": ("🟡", "yellow", "MODERATE RISK"),
            "HIGH": ("🟠", "orange", "ELEVATED RISK"),
            "CRITICAL": ("🔴", "red", "MAXIMUM ALERT")
        }

        emoji, color, description = indicators.get(self.threat_level, ("⚪", "white", "UNKNOWN"))

        threat_text.append("╭─ THREAT ASSESSMENT ──────────────╮\n", style="dim red")
        threat_text.append("│ ", style="dim red")
        threat_text.append(f"Level: {emoji} ", style="white")
        threat_text.append(f"{self.threat_level}", style=f"bold {color}")
        threat_text.append(" " * (30 - len(f"Level: {self.threat_level}")), style="white")
        threat_text.append("│\n", style="dim red")

        threat_text.append("│ ", style="dim red")
        threat_text.append(f"Score: ", style="white")
        threat_text.append(f"{self.threat_score:.2f}", style=f"bold {color}")
        threat_text.append(" " * (30 - len(f"Score: {self.threat_score:.2f}")), style="white")
        threat_text.append("│\n", style="dim red")

        threat_text.append("│ ", style="dim red")
        threat_text.append(f"Status: {description}", style=f"{color}")
        threat_text.append(" " * (31 - len(f"Status: {description}")), style="white")
        threat_text.append("│\n", style="dim red")

        threat_text.append("╰───────────────────────────────────╯", style="dim red")

        self.query_one("#threat_display", Static).update(threat_text)


class IntelligenceTimelineWidget(Container):
    """Timeline visualization for investigation progress"""

    timeline_events: reactive[List[Dict[str, Any]]] = reactive([])

    def compose(self):
        with Container(classes="intelligence-panel"):
            yield Static("Investigation Timeline", classes="title")
            yield Static("", id="timeline_display")

    def add_event(self, event_type: str, description: str, timestamp: Optional[datetime] = None):
        """Add an event to the timeline"""
        if timestamp is None:
            timestamp = datetime.now()

        event = {
            "type": event_type,
            "description": description,
            "timestamp": timestamp,
            "id": len(self.timeline_events)
        }

        new_events = list(self.timeline_events)
        new_events.append(event)
        self.timeline_events = new_events

    def watch_timeline_events(self, events: List[Dict[str, Any]]) -> None:
        """Update timeline display when events change"""
        timeline_text = Text()

        timeline_text.append("╭─ INVESTIGATION TIMELINE ─────────╮\n", style="dim cyan")

        if not events:
            timeline_text.append("│ No events recorded               │\n", style="dim white")
        else:
            # Show last 5 events
            recent_events = events[-5:]
            for i, event in enumerate(recent_events):
                time_str = event["timestamp"].strftime("%H:%M:%S")
                event_type = event["type"]
                description = event["description"]

                # Event type styling
                type_colors = {
                    "START": "green",
                    "PROGRESS": "cyan",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "COMPLETE": "green"
                }
                color = type_colors.get(event_type, "white")

                timeline_text.append("│ ", style="dim cyan")
                timeline_text.append(f"{time_str} ", style="dim white")
                timeline_text.append(f"[{event_type}]", style=f"bold {color}")

                # Truncate description if too long
                max_desc_len = 35 - len(f"{time_str} [{event_type}]")
                if len(description) > max_desc_len:
                    description = description[:max_desc_len-3] + "..."

                timeline_text.append(f" {description}", style="white")

                # Add padding
                total_len = len(f"{time_str} [{event_type}] {description}")
                padding = 35 - total_len
                if padding > 0:
                    timeline_text.append(" " * padding, style="white")

                timeline_text.append("│\n", style="dim cyan")

        timeline_text.append("╰───────────────────────────────────╯", style="dim cyan")

        self.query_one("#timeline_display", Static).update(timeline_text)


class NetworkTopologyWidget(Container):
    """Network topology visualization for connected entities"""

    connections: reactive[List[Tuple[str, str]]] = reactive([])
    nodes: reactive[List[str]] = reactive([])

    def compose(self):
        with Container(classes="intelligence-panel"):
            yield Static("Network Topology", classes="title")
            yield Static("", id="topology_display")

    def add_connection(self, node1: str, node2: str):
        """Add a connection between two nodes"""
        # Add nodes if they don't exist
        new_nodes = list(self.nodes)
        if node1 not in new_nodes:
            new_nodes.append(node1)
        if node2 not in new_nodes:
            new_nodes.append(node2)
        self.nodes = new_nodes

        # Add connection
        new_connections = list(self.connections)
        connection = (node1, node2)
        if connection not in new_connections and (node2, node1) not in new_connections:
            new_connections.append(connection)
            self.connections = new_connections

    def watch_connections(self, connections: List[Tuple[str, str]]) -> None:
        self._update_topology()

    def watch_nodes(self, nodes: List[str]) -> None:
        self._update_topology()

    def _update_topology(self) -> None:
        """Update topology visualization"""
        topology_text = Text()

        topology_text.append("╭─ NETWORK ANALYSIS ───────────────╮\n", style="dim blue")

        if not self.nodes:
            topology_text.append("│ No network data available        │\n", style="dim white")
        else:
            topology_text.append("│ ", style="dim blue")
            topology_text.append(f"Nodes: {len(self.nodes)}", style="bold cyan")
            topology_text.append(f" | Connections: {len(self.connections)}", style="bold green")
            padding = 35 - len(f"Nodes: {len(self.nodes)} | Connections: {len(self.connections)}")
            topology_text.append(" " * max(0, padding), style="white")
            topology_text.append("│\n", style="dim blue")

            topology_text.append("│ ", style="dim blue")
            topology_text.append("─" * 33, style="dim white")
            topology_text.append("│\n", style="dim blue")

            # Show sample connections
            for i, (node1, node2) in enumerate(self.connections[:3]):
                # Truncate node names if too long
                n1 = node1[:12] + "..." if len(node1) > 15 else node1
                n2 = node2[:12] + "..." if len(node2) > 15 else node2

                topology_text.append("│ ", style="dim blue")
                topology_text.append(f"{n1}", style="yellow")
                topology_text.append(" ↔ ", style="white")
                topology_text.append(f"{n2}", style="yellow")

                connection_str = f"{n1} ↔ {n2}"
                padding = 33 - len(connection_str)
                topology_text.append(" " * max(0, padding), style="white")
                topology_text.append("│\n", style="dim blue")

            if len(self.connections) > 3:
                remaining = len(self.connections) - 3
                topology_text.append("│ ", style="dim blue")
                topology_text.append(f"... and {remaining} more connections", style="dim white")
                padding = 33 - len(f"... and {remaining} more connections")
                topology_text.append(" " * max(0, padding), style="white")
                topology_text.append("│\n", style="dim blue")

        topology_text.append("╰───────────────────────────────────╯", style="dim blue")

        self.query_one("#topology_display", Static).update(topology_text)


class IntelligenceDataTable(Container):
    """Advanced data table with sorting and filtering"""

    def compose(self):
        with Container(classes="results-panel"):
            yield Static("Intelligence Data", classes="title")
            yield DataTable(id="intel_table")

    def initialize_table(self):
        """Initialize the data table with columns"""
        table = self.query_one("#intel_table", DataTable)
        table.add_columns(
            "Type",
            "Value",
            "Confidence",
            "Source",
            "Timestamp"
        )

    def add_intelligence_item(self, intel_type: str, value: str, confidence: float, source: str):
        """Add an intelligence item to the table"""
        table = self.query_one("#intel_table", DataTable)

        # Ensure table is initialized
        if not table.columns:
            self.initialize_table()

        # Format confidence as percentage
        confidence_str = f"{confidence:.1%}"

        # Truncate long values
        display_value = value[:30] + "..." if len(value) > 33 else value

        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")

        table.add_row(
            intel_type,
            display_value,
            confidence_str,
            source,
            timestamp
        )


class OperationalDashboard(Container):
    """Combined operational dashboard with all widgets"""

    def compose(self):
        with Grid(id="dashboard_grid"):
            yield IntelligenceMetricsWidget()
            yield ThreatLevelIndicator()
            yield IntelligenceTimelineWidget()
            yield NetworkTopologyWidget()

    def on_mount(self):
        """Configure the dashboard grid layout"""
        grid = self.query_one("#dashboard_grid", Grid)
        grid.styles.grid_template_columns = "1fr 1fr"
        grid.styles.grid_template_rows = "auto auto"

    def update_metrics(self, investigations: int, threats: int, data_points: int, success_rate: float):
        """Update intelligence metrics"""
        metrics = self.query_one(IntelligenceMetricsWidget)
        metrics.total_investigations = investigations
        metrics.active_threats = threats
        metrics.data_points = data_points
        metrics.success_rate = success_rate

    def update_threat_level(self, level: str, score: float):
        """Update threat assessment"""
        threat_widget = self.query_one(ThreatLevelIndicator)
        threat_widget.threat_level = level
        threat_widget.threat_score = score

    def add_timeline_event(self, event_type: str, description: str):
        """Add event to investigation timeline"""
        timeline = self.query_one(IntelligenceTimelineWidget)
        timeline.add_event(event_type, description)

    def add_network_connection(self, node1: str, node2: str):
        """Add network connection"""
        network = self.query_one(NetworkTopologyWidget)
        network.add_connection(node1, node2)


class RealTimeChart(Container):
    """Real-time chart widget for metrics visualization"""

    data_points: reactive[List[float]] = reactive([])
    max_points: int = 20

    def compose(self):
        with Container(classes="intelligence-panel"):
            yield Static("Real-Time Analysis", classes="title")
            yield Static("", id="chart_display")

    def add_data_point(self, value: float):
        """Add a new data point to the chart"""
        new_points = list(self.data_points)
        new_points.append(value)

        # Keep only the last max_points
        if len(new_points) > self.max_points:
            new_points = new_points[-self.max_points:]

        self.data_points = new_points

    def watch_data_points(self, points: List[float]) -> None:
        """Update chart display when data changes"""
        chart_text = Text()

        chart_text.append("╭─ REAL-TIME METRICS ──────────────╮\n", style="dim green")

        if not points:
            chart_text.append("│ No data available                │\n", style="dim white")
        else:
            # Simple ASCII chart
            max_val = max(points) if points else 1
            min_val = min(points) if points else 0
            range_val = max_val - min_val if max_val != min_val else 1

            chart_text.append("│ ", style="dim green")
            chart_text.append(f"Max: {max_val:.2f} | Min: {min_val:.2f}", style="cyan")
            padding = 33 - len(f"Max: {max_val:.2f} | Min: {min_val:.2f}")
            chart_text.append(" " * max(0, padding), style="white")
            chart_text.append("│\n", style="dim green")

            # Chart bars
            for i, point in enumerate(points[-8:]):  # Show last 8 points
                normalized = (point - min_val) / range_val
                bar_length = int(normalized * 25)

                chart_text.append("│ ", style="dim green")
                chart_text.append("█" * bar_length, style="cyan")
                chart_text.append("░" * (25 - bar_length), style="dim white")
                chart_text.append(f" {point:.1f}", style="white")
                chart_text.append("│\n", style="dim green")

        chart_text.append("╰───────────────────────────────────╯", style="dim green")

        self.query_one("#chart_display", Static).update(chart_text)