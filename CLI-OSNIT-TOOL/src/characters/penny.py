#!/usr/bin/env python3
"""
Penny - User Interface Assistant & Data Visualization Expert

Like Penny in Inspector Gadget who was the tech-savvy problem-solver,
this Penny provides intelligent user interface assistance, data visualization,
and user experience enhancements for Inspector-G.

Penny's Capabilities:
- Intelligent data visualization and charts
- User guidance and help system
- Investigation results presentation
- Interactive tutorials and tips
- Progress tracking and status updates
- User-friendly explanations of complex data
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)


class PennyMode(Enum):
    """Penny's different operational modes"""
    HELPER = "helper"           # General assistance and guidance
    VISUALIZER = "visualizer"   # Data visualization and charts
    TUTOR = "tutor"            # Educational mode with explanations
    ANALYST = "analyst"         # Analysis presentation and insights
    GUIDE = "guide"            # Step-by-step guidance


@dataclass
class PennyVisualization:
    """Data structure for Penny's visualizations"""
    viz_type: str              # table, chart, graph, timeline, network
    title: str
    data: Dict[str, Any]
    description: str
    insights: List[str]
    timestamp: datetime


@dataclass
class PennyTip:
    """Helpful tips from Penny"""
    category: str              # usage, technique, interpretation
    title: str
    content: str
    example: Optional[str]
    difficulty: str            # beginner, intermediate, advanced


class Penny:
    """
    Penny - The User Interface Assistant

    Penny enhances the user experience by providing intelligent assistance,
    data visualization, and user-friendly explanations of OSINT operations.
    """

    def __init__(self):
        self.mode = PennyMode.HELPER
        self.personality_traits = {
            "helpful": True,
            "tech_savvy": True,
            "patient": True,
            "encouraging": True,
            "detail_oriented": True
        }
        self.visualization_cache = {}
        logger.info("💡 Penny initialized - User interface assistant ready!")

    def greet_user(self, username: Optional[str] = None) -> str:
        """Penny's friendly greeting"""
        if username:
            return f"Hi {username}! I'm Penny, your OSINT assistant. I'm here to help make your investigations easier and more visual. What would you like to explore today?"
        return "Hi there! I'm Penny, your friendly OSINT assistant. I can help visualize data, explain results, and guide you through investigations. How can I help?"

    def create_visualization(self, data: Dict[str, Any], viz_type: str = "auto") -> PennyVisualization:
        """
        Create intelligent data visualizations
        """
        if viz_type == "auto":
            viz_type = self._determine_best_visualization(data)

        visualization = PennyVisualization(
            viz_type=viz_type,
            title=self._generate_title(data, viz_type),
            data=data,
            description=self._generate_description(data, viz_type),
            insights=self._generate_insights(data, viz_type),
            timestamp=datetime.now()
        )

        # Cache for potential reuse
        cache_key = f"{viz_type}_{hash(str(data))}"
        self.visualization_cache[cache_key] = visualization

        return visualization

    def _determine_best_visualization(self, data: Dict[str, Any]) -> str:
        """Smart visualization type selection"""
        if "timeline" in str(data).lower() or "timestamp" in str(data).lower():
            return "timeline"
        elif "network" in str(data).lower() or "connections" in str(data).lower():
            return "network"
        elif "count" in str(data).lower() or "frequency" in str(data).lower():
            return "chart"
        elif isinstance(data, dict) and all(isinstance(v, (int, float)) for v in data.values()):
            return "chart"
        else:
            return "table"

    def _generate_title(self, data: Dict[str, Any], viz_type: str) -> str:
        """Generate descriptive titles"""
        titles = {
            "timeline": "Investigation Timeline",
            "network": "Connection Analysis",
            "chart": "Data Distribution",
            "table": "Detailed Results",
            "graph": "Relationship Mapping"
        }
        return titles.get(viz_type, "OSINT Analysis Results")

    def _generate_description(self, data: Dict[str, Any], viz_type: str) -> str:
        """Generate user-friendly descriptions"""
        descriptions = {
            "timeline": "This timeline shows the chronological sequence of events and data points discovered during the investigation.",
            "network": "This network diagram visualizes the relationships and connections between different entities.",
            "chart": "This chart displays the distribution and frequency of data points to help identify patterns.",
            "table": "This table provides a detailed breakdown of all discovered information.",
            "graph": "This graph illustrates the relationships and correlations in the data."
        }
        return descriptions.get(viz_type, "This visualization presents the investigation results in an easy-to-understand format.")

    def _generate_insights(self, data: Dict[str, Any], viz_type: str) -> List[str]:
        """Generate analytical insights"""
        insights = []

        if viz_type == "timeline":
            insights.append("Look for patterns in timing - clustered activities might indicate coordinated behavior")
            insights.append("Pay attention to gaps in the timeline - these might reveal operational security")
        elif viz_type == "network":
            insights.append("Central nodes often represent key entities or communication hubs")
            insights.append("Isolated clusters might indicate separate operational groups")
        elif viz_type == "chart":
            insights.append("High-frequency items often indicate primary activities or interests")
            insights.append("Outliers in the data might reveal unusual or significant events")
        elif viz_type == "table":
            insights.append("Sort by different columns to discover patterns and correlations")
            insights.append("Look for consistent patterns across different data fields")

        return insights

    def explain_results(self, results: Dict[str, Any], complexity: str = "beginner") -> str:
        """
        Provide user-friendly explanations of OSINT results
        """
        explanations = {
            "beginner": self._explain_for_beginners,
            "intermediate": self._explain_for_intermediate,
            "advanced": self._explain_for_advanced
        }

        explain_func = explanations.get(complexity, self._explain_for_beginners)
        return explain_func(results)

    def _explain_for_beginners(self, results: Dict[str, Any]) -> str:
        """Simple explanations for beginners"""
        explanation = "Here's what I found in simple terms:\n\n"

        if "usernames" in results:
            explanation += f"🔍 Found {len(results['usernames'])} usernames across different platforms. "
            explanation += "This helps us understand what online accounts might belong to the same person.\n\n"

        if "emails" in results:
            explanation += f"📧 Discovered {len(results['emails'])} email addresses. "
            explanation += "These can help identify communication patterns and account registrations.\n\n"

        if "domains" in results:
            explanation += f"🌐 Found {len(results['domains'])} domains. "
            explanation += "These show what websites or services might be connected to our target.\n\n"

        explanation += "💡 Tip: Look for patterns and connections between different pieces of information!"
        return explanation

    def _explain_for_intermediate(self, results: Dict[str, Any]) -> str:
        """Detailed explanations for intermediate users"""
        explanation = "Analysis Summary:\n\n"

        for key, value in results.items():
            if isinstance(value, list):
                explanation += f"• {key.title()}: {len(value)} items discovered\n"
                if len(value) > 0:
                    explanation += f"  Sample: {value[0] if len(value) > 0 else 'N/A'}\n"
            elif isinstance(value, dict):
                explanation += f"• {key.title()}: Complex data structure with {len(value)} fields\n"
            else:
                explanation += f"• {key.title()}: {value}\n"

        explanation += "\n🎯 Next Steps: Consider cross-referencing these findings with additional OSINT techniques."
        return explanation

    def _explain_for_advanced(self, results: Dict[str, Any]) -> str:
        """Technical explanations for advanced users"""
        explanation = "Technical Analysis Report:\n\n"
        explanation += f"Dataset contains {len(results)} primary data categories.\n"
        explanation += f"Total data points: {sum(len(v) if isinstance(v, list) else 1 for v in results.values())}\n\n"

        explanation += "Data Quality Assessment:\n"
        for key, value in results.items():
            if isinstance(value, list):
                explanation += f"• {key}: {len(value)} items (confidence varies by source)\n"

        explanation += "\n🔬 Recommended correlation analysis and temporal mapping for enhanced insights."
        return explanation

    def provide_tip(self, category: str = "general") -> PennyTip:
        """Provide helpful OSINT tips"""
        tips_database = {
            "general": [
                PennyTip("usage", "Start Broad, Then Focus",
                        "Begin investigations with general searches, then narrow down based on initial findings.",
                        "Search for 'john_doe' first, then focus on specific platforms where you find matches.",
                        "beginner"),
                PennyTip("technique", "Cross-Reference Everything",
                        "Always verify findings across multiple sources and platforms.",
                        "If you find an email on one platform, search for it on others to build a complete profile.",
                        "intermediate"),
            ],
            "username": [
                PennyTip("technique", "Username Variations",
                        "Try common variations like adding numbers, underscores, or dots.",
                        "If 'johndoe' doesn't work, try 'john_doe', 'john.doe', 'johndoe123'",
                        "beginner"),
            ],
            "email": [
                PennyTip("technique", "Corporate Email Patterns",
                        "Most companies follow predictable email formats.",
                        "firstname.lastname@company.com or first.last@company.com",
                        "intermediate"),
            ]
        }

        category_tips = tips_database.get(category, tips_database["general"])
        import random
        return random.choice(category_tips)

    def create_progress_report(self, investigation_data: Dict[str, Any]) -> str:
        """Generate user-friendly progress reports"""
        report = "📊 Investigation Progress Report\n"
        report += "=" * 40 + "\n\n"

        total_findings = sum(len(v) if isinstance(v, list) else 1 for v in investigation_data.values())
        report += f"🔍 Total Findings: {total_findings}\n"

        for category, data in investigation_data.items():
            if isinstance(data, list):
                report += f"• {category.title()}: {len(data)} items\n"
            else:
                report += f"• {category.title()}: 1 item\n"

        report += "\n💡 Analysis Status: "
        if total_findings < 5:
            report += "Just getting started - try expanding your search criteria!"
        elif total_findings < 20:
            report += "Good progress - consider cross-referencing findings!"
        else:
            report += "Excellent coverage - time for deep analysis!"

        return report

    def suggest_next_steps(self, current_results: Dict[str, Any]) -> List[str]:
        """Intelligent suggestions for next investigation steps"""
        suggestions = []

        if "usernames" in current_results and len(current_results["usernames"]) > 0:
            suggestions.append("🔍 Try searching these usernames on additional platforms")
            suggestions.append("📧 Look for email patterns based on discovered usernames")

        if "emails" in current_results and len(current_results["emails"]) > 0:
            suggestions.append("🌐 Search for domains associated with these email addresses")
            suggestions.append("🔒 Check if these emails appear in data breach databases")

        if "domains" in current_results and len(current_results["domains"]) > 0:
            suggestions.append("🏢 Research the organizations behind these domains")
            suggestions.append("📱 Look for social media accounts associated with these domains")

        if not suggestions:
            suggestions.append("🎯 Try broadening your search with related keywords")
            suggestions.append("🔄 Consider alternative search strategies")

        return suggestions

    def format_for_display(self, data: Any, format_type: str = "rich") -> str:
        """Format data for beautiful terminal display"""
        if format_type == "rich":
            return self._format_rich_display(data)
        elif format_type == "simple":
            return self._format_simple_display(data)
        else:
            return str(data)

    def _format_rich_display(self, data: Any) -> str:
        """Rich terminal formatting with colors and symbols"""
        if isinstance(data, dict):
            formatted = "📋 Results:\n"
            for key, value in data.items():
                if isinstance(value, list):
                    formatted += f"  🔹 {key.title()}: {len(value)} items\n"
                    for item in value[:3]:  # Show first 3 items
                        formatted += f"    • {item}\n"
                    if len(value) > 3:
                        formatted += f"    ... and {len(value) - 3} more\n"
                else:
                    formatted += f"  🔹 {key.title()}: {value}\n"
            return formatted
        elif isinstance(data, list):
            formatted = f"📝 List ({len(data)} items):\n"
            for i, item in enumerate(data[:5], 1):
                formatted += f"  {i}. {item}\n"
            if len(data) > 5:
                formatted += f"  ... and {len(data) - 5} more items\n"
            return formatted
        else:
            return f"💫 Result: {data}"

    def _format_simple_display(self, data: Any) -> str:
        """Simple text formatting"""
        return json.dumps(data, indent=2, ensure_ascii=False)


# Global Penny instance
penny = Penny()