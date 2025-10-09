#!/usr/bin/env python3
"""
Brain - The Integrated AI Agent for Inspector-G

Like Brain the dog who secretly solved Inspector Gadget's cases,
this AI agent system coordinates all OSINT operations with intelligence,
strategy, and that characteristic "woof" of satisfaction when solving cases.

Brain handles:
- Natural language query interpretation
- Multi-module coordination and orchestration
- Intelligent analysis and synthesis
- Strategic investigation planning
- Cross-platform correlation and insights
- Case management and evidence compilation
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from .neural_engine import NeuralFoundationEngine
from ..core.config import settings
from ..ui.themes import theme

logger = logging.getLogger(__name__)


class BrainThoughtType(Enum):
    """Types of Brain's thought processes"""
    ANALYSIS = "analysis"
    STRATEGY = "strategy"
    CORRELATION = "correlation"
    INSIGHT = "insight"
    RECOMMENDATION = "recommendation"
    WARNING = "warning"
    DISCOVERY = "discovery"


@dataclass
class BrainThought:
    """A single thought from Brain's analysis"""
    thought_type: BrainThoughtType
    content: str
    confidence: float
    evidence: List[str]
    timestamp: datetime
    investigation_id: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            'thought_type': self.thought_type.value,
            'content': self.content,
            'confidence': self.confidence,
            'evidence': self.evidence,
            'timestamp': self.timestamp.isoformat(),
            'investigation_id': self.investigation_id
        }


@dataclass
class BrainInvestigation:
    """A complete investigation coordinated by Brain"""
    investigation_id: str
    target: str
    investigation_type: str
    start_time: datetime
    end_time: Optional[datetime] = None

    # OSINT Results
    username_results: Optional[Dict] = None
    email_results: Optional[Dict] = None
    phone_results: Optional[Dict] = None
    domain_results: Optional[Dict] = None

    # Brain's Analysis
    thoughts: List[BrainThought] = None
    final_assessment: Optional[str] = None
    risk_score: float = 0.0
    key_findings: List[str] = None
    recommendations: List[str] = None

    def __post_init__(self):
        if self.thoughts is None:
            self.thoughts = []
        if self.key_findings is None:
            self.key_findings = []
        if self.recommendations is None:
            self.recommendations = []


class Brain:
    """
    Brain - The Central AI Agent for Inspector-G

    Like Brain the dog, this AI system works intelligently behind the scenes
    to coordinate OSINT operations and provide strategic analysis.

    "Woof! Leave the thinking to me, Inspector!" - Brain's motto
    """

    def __init__(self):
        # Initialize Brain's neural core
        self.neural_engine = NeuralFoundationEngine()

        # Brain's personality and capabilities
        self.brain_mode = settings.brain_mode
        self.catchphrases_enabled = settings.catchphrases_enabled

        # Investigation tracking
        self.active_investigations: Dict[str, BrainInvestigation] = {}
        self.investigation_counter = 0

        # Brain's knowledge base
        self.osint_strategies = self._load_osint_strategies()
        self.correlation_patterns = self._load_correlation_patterns()

        logger.info("🧠 Brain activated - Ready to solve cases!")

    def _load_osint_strategies(self) -> Dict[str, Dict]:
        """Load Brain's OSINT investigation strategies"""
        return {
            "username_investigation": {
                "primary_modules": ["quantum_username_intelligence", "behavioral_fingerprint"],
                "analysis_focus": ["cross_platform_correlation", "behavioral_patterns"],
                "risk_factors": ["privacy_exposure", "account_linking"],
                "brain_insight": "Look for behavioral DNA patterns across platforms"
            },
            "email_investigation": {
                "primary_modules": ["corporate_email_oracle", "breach_timeline_engine"],
                "analysis_focus": ["corporate_psychology", "breach_correlation"],
                "risk_factors": ["data_breaches", "corporate_exposure"],
                "brain_insight": "Corporate email patterns reveal organizational vulnerabilities"
            },
            "domain_investigation": {
                "primary_modules": ["subdomain_discovery", "infrastructure_analysis"],
                "analysis_focus": ["attack_surface", "technology_stack"],
                "risk_factors": ["exposed_services", "misconfigurations"],
                "brain_insight": "Infrastructure topology reveals security posture"
            },
            "comprehensive_target": {
                "primary_modules": ["all_modules"],
                "analysis_focus": ["full_spectrum_analysis", "cross_domain_correlation"],
                "risk_factors": ["aggregated_exposure", "identity_correlation"],
                "brain_insight": "Complete digital footprint analysis requires multi-vector approach"
            }
        }

    def _load_correlation_patterns(self) -> Dict[str, List[str]]:
        """Load Brain's correlation pattern recognition"""
        return {
            "email_username_correlation": [
                "matching_naming_conventions",
                "timestamp_overlap",
                "shared_domains"
            ],
            "cross_platform_indicators": [
                "consistent_usernames",
                "similar_profile_data",
                "linked_accounts"
            ],
            "corporate_exposure_patterns": [
                "employee_email_patterns",
                "organizational_structure",
                "technology_preferences"
            ]
        }

    async def think_about_query(self, query: str) -> Dict[str, Any]:
        """
        Brain analyzes a natural language query and develops investigation strategy

        "Woof! Let me think about this..." - Brain processing mode
        """
        logger.info(f"🧠 Brain thinking about: {query}")

        try:
            # Use Neural Foundation Engine to understand query
            query_analysis = await self.neural_engine.analyze_query(query)

            # Determine investigation type and strategy
            investigation_type = await self._classify_investigation_type(query, query_analysis)
            strategy = self.osint_strategies.get(investigation_type, self.osint_strategies["comprehensive_target"])

            # Generate Brain's strategic thoughts
            brain_thoughts = await self._generate_strategic_thoughts(query, investigation_type, strategy)

            # Create investigation plan
            investigation_plan = {
                'query': query,
                'investigation_type': investigation_type,
                'strategy': strategy,
                'brain_thoughts': [thought.to_dict() for thought in brain_thoughts],
                'recommended_modules': strategy['primary_modules'],
                'analysis_focus': strategy['analysis_focus'],
                'brain_insight': strategy['brain_insight'],
                'estimated_complexity': self._estimate_complexity(query_analysis),
                'risk_assessment': await self._assess_query_risk(query),
                'brain_catchphrase': self._get_brain_catchphrase("thinking")
            }

            if self.brain_mode:
                logger.info(f"🧠 Brain's insight: {strategy['brain_insight']}")

            return investigation_plan

        except Exception as e:
            logger.error(f"🧠 Brain thinking error: {e}")
            return await self._fallback_analysis(query)

    async def coordinate_investigation(self, target: str, investigation_type: str, modules: List[str]) -> BrainInvestigation:
        """
        Brain coordinates a multi-module OSINT investigation

        "Woof! I'll handle the coordination!" - Brain management mode
        """
        investigation_id = f"BRAIN-{self.investigation_counter:04d}"
        self.investigation_counter += 1

        investigation = BrainInvestigation(
            investigation_id=investigation_id,
            target=target,
            investigation_type=investigation_type,
            start_time=datetime.now()
        )

        self.active_investigations[investigation_id] = investigation

        logger.info(f"🧠 Brain coordinating investigation {investigation_id} for target: {target}")

        try:
            # Import modules dynamically to avoid circular imports
            if "quantum_username_intelligence" in modules:
                from ..modules.username import UsernameRecon
                username_recon = UsernameRecon()
                investigation.username_results = await username_recon.investigate_username(target)
                await self._analyze_username_results(investigation)

            if "corporate_email_oracle" in modules:
                from ..modules.email import EmailRecon
                email_recon = EmailRecon()
                investigation.email_results = await email_recon.investigate_domain_emails(target)
                await self._analyze_email_results(investigation)

            # Cross-correlation analysis
            await self._perform_cross_correlation(investigation)

            # Generate Brain's final assessment
            await self._generate_final_assessment(investigation)

            investigation.end_time = datetime.now()

            if self.brain_mode:
                logger.info(f"🧠 Brain completed investigation {investigation_id}")
                logger.info(f"🧠 Brain's assessment: {investigation.final_assessment}")

            return investigation

        except Exception as e:
            logger.error(f"🧠 Brain coordination error: {e}")
            investigation.end_time = datetime.now()
            investigation.final_assessment = f"Investigation encountered error: {e}"
            return investigation

    async def _classify_investigation_type(self, query: str, analysis: Dict) -> str:
        """Brain classifies the type of investigation needed"""
        query_lower = query.lower()

        # Username investigation indicators
        if any(keyword in query_lower for keyword in ["username", "user", "account", "profile", "social"]):
            return "username_investigation"

        # Email investigation indicators
        if any(keyword in query_lower for keyword in ["email", "corporate", "company", "domain", "@"]):
            return "email_investigation"

        # Domain investigation indicators
        if any(keyword in query_lower for keyword in ["domain", "website", "infrastructure", "subdomain"]):
            return "domain_investigation"

        # Default to comprehensive
        return "comprehensive_target"

    async def _generate_strategic_thoughts(self, query: str, investigation_type: str, strategy: Dict) -> List[BrainThought]:
        """Generate Brain's strategic thoughts about the investigation"""
        thoughts = []

        # Strategic analysis thought
        strategic_thought = BrainThought(
            thought_type=BrainThoughtType.STRATEGY,
            content=f"Investigation requires {investigation_type} approach. {strategy['brain_insight']}",
            confidence=0.85,
            evidence=["query_analysis", "strategy_matching"],
            timestamp=datetime.now()
        )
        thoughts.append(strategic_thought)

        # Risk assessment thought
        risk_factors = strategy.get('risk_factors', [])
        if risk_factors:
            risk_thought = BrainThought(
                thought_type=BrainThoughtType.WARNING,
                content=f"Potential risk factors: {', '.join(risk_factors)}",
                confidence=0.70,
                evidence=["risk_pattern_analysis"],
                timestamp=datetime.now()
            )
            thoughts.append(risk_thought)

        # Methodology recommendation
        modules = strategy.get('primary_modules', [])
        if modules:
            method_thought = BrainThought(
                thought_type=BrainThoughtType.RECOMMENDATION,
                content=f"Recommended approach: Use {', '.join(modules)} for optimal coverage",
                confidence=0.90,
                evidence=["methodology_analysis"],
                timestamp=datetime.now()
            )
            thoughts.append(method_thought)

        return thoughts

    async def _analyze_username_results(self, investigation: BrainInvestigation):
        """Brain analyzes username investigation results"""
        if not investigation.username_results:
            return

        results = investigation.username_results
        platforms_found = len(results.get('discoveries', []))

        if platforms_found > 5:
            thought = BrainThought(
                thought_type=BrainThoughtType.DISCOVERY,
                content=f"Significant username presence across {platforms_found} platforms - high digital footprint",
                confidence=0.85,
                evidence=["platform_count_analysis"],
                timestamp=datetime.now(),
                investigation_id=investigation.investigation_id
            )
            investigation.thoughts.append(thought)
            investigation.key_findings.append(f"Username found on {platforms_found} platforms")

    async def _analyze_email_results(self, investigation: BrainInvestigation):
        """Brain analyzes email investigation results"""
        if not investigation.email_results:
            return

        results = investigation.email_results
        total_emails = results.get('total_emails', 0)

        if total_emails > 10:
            thought = BrainThought(
                thought_type=BrainThoughtType.ANALYSIS,
                content=f"Extensive email intelligence gathered: {total_emails} emails identified",
                confidence=0.80,
                evidence=["email_count_analysis"],
                timestamp=datetime.now(),
                investigation_id=investigation.investigation_id
            )
            investigation.thoughts.append(thought)
            investigation.key_findings.append(f"Corporate email intelligence: {total_emails} emails")

    async def _perform_cross_correlation(self, investigation: BrainInvestigation):
        """Brain performs cross-correlation analysis between results"""
        correlations_found = []

        # Check for username-email correlations
        if investigation.username_results and investigation.email_results:
            target = investigation.target
            email_count = investigation.email_results.get('total_emails', 0)
            username_platforms = len(investigation.username_results.get('discoveries', []))

            if email_count > 0 and username_platforms > 0:
                correlations_found.append("username_email_correlation")

                correlation_thought = BrainThought(
                    thought_type=BrainThoughtType.CORRELATION,
                    content=f"Cross-correlation detected between username presence and email patterns",
                    confidence=0.75,
                    evidence=["cross_domain_analysis"],
                    timestamp=datetime.now(),
                    investigation_id=investigation.investigation_id
                )
                investigation.thoughts.append(correlation_thought)

        if correlations_found:
            investigation.key_findings.append(f"Cross-correlations found: {', '.join(correlations_found)}")

    async def _generate_final_assessment(self, investigation: BrainInvestigation):
        """Brain generates final investigation assessment"""
        total_discoveries = 0
        risk_factors = []

        # Count total discoveries
        if investigation.username_results:
            total_discoveries += len(investigation.username_results.get('discoveries', []))

        if investigation.email_results:
            total_discoveries += investigation.email_results.get('total_emails', 0)

        # Assess risk level
        if total_discoveries > 20:
            risk_level = "HIGH"
            risk_factors.append("extensive_digital_footprint")
        elif total_discoveries > 10:
            risk_level = "MEDIUM"
            risk_factors.append("moderate_exposure")
        else:
            risk_level = "LOW"

        investigation.risk_score = min(total_discoveries / 50.0, 1.0)  # Normalize to 0-1

        # Generate assessment
        assessment_parts = [
            f"Investigation completed with {total_discoveries} total discoveries.",
            f"Risk assessment: {risk_level} exposure level.",
            f"Brain's analysis identified {len(investigation.key_findings)} key findings."
        ]

        if investigation.thoughts:
            insights_count = len([t for t in investigation.thoughts if t.thought_type == BrainThoughtType.INSIGHT])
            assessment_parts.append(f"Generated {insights_count} strategic insights.")

        investigation.final_assessment = " ".join(assessment_parts)

        # Generate recommendations
        if risk_level == "HIGH":
            investigation.recommendations.append("Consider privacy hardening measures")
            investigation.recommendations.append("Review digital footprint exposure")

        if total_discoveries > 0:
            investigation.recommendations.append("Implement monitoring for mentioned platforms/domains")

    def _estimate_complexity(self, query_analysis: Dict) -> str:
        """Estimate investigation complexity"""
        # Simple heuristic based on query analysis
        if len(query_analysis.get('entities', [])) > 3:
            return "HIGH"
        elif len(query_analysis.get('entities', [])) > 1:
            return "MEDIUM"
        else:
            return "LOW"

    async def _assess_query_risk(self, query: str) -> str:
        """Assess potential risk level of the query"""
        high_risk_indicators = ["breach", "hack", "exploit", "vulnerability"]
        medium_risk_indicators = ["corporate", "employee", "organization"]

        query_lower = query.lower()

        if any(indicator in query_lower for indicator in high_risk_indicators):
            return "HIGH"
        elif any(indicator in query_lower for indicator in medium_risk_indicators):
            return "MEDIUM"
        else:
            return "LOW"

    def _get_brain_catchphrase(self, context: str) -> str:
        """Get appropriate Brain catchphrase for the context"""
        if not self.catchphrases_enabled:
            return ""

        catchphrases = {
            "thinking": ["🧠 Woof! Let me think about this...", "🧠 Brain analyzing...", "🧠 Processing with dog-like intelligence!"],
            "discovery": ["🧠 Woof! Found something interesting!", "🧠 Aha! Brain's got it!", "🧠 Excellent discovery!"],
            "completion": ["🧠 Woof! Case solved!", "🧠 Another mystery unraveled!", "🧠 Brain's work is done!"],
            "error": ["🧠 Woof? Something's not right...", "🧠 Brain needs to investigate this error!", "🧠 Hmm, unexpected result..."]
        }

        import random
        phrases = catchphrases.get(context, ["🧠 Woof!"])
        return random.choice(phrases)

    async def _fallback_analysis(self, query: str) -> Dict[str, Any]:
        """Fallback analysis when main processing fails"""
        return {
            'query': query,
            'investigation_type': 'basic_analysis',
            'brain_thoughts': [{
                'thought_type': 'analysis',
                'content': 'Basic query processing - limited analysis available',
                'confidence': 0.3,
                'evidence': ['fallback_mode'],
                'timestamp': datetime.now().isoformat()
            }],
            'recommended_modules': ['manual_investigation'],
            'brain_insight': 'Simple investigation approach recommended',
            'estimated_complexity': 'UNKNOWN',
            'risk_assessment': 'UNKNOWN',
            'brain_catchphrase': self._get_brain_catchphrase("error")
        }

    async def get_investigation_summary(self, investigation: BrainInvestigation) -> str:
        """Generate human-readable investigation summary"""
        summary_parts = [
            f"🧠 Brain's Investigation Report - {investigation.investigation_id}",
            f"Target: {investigation.target}",
            f"Type: {investigation.investigation_type}",
            f"Duration: {(investigation.end_time - investigation.start_time).total_seconds():.1f} seconds",
            "",
            "📊 Key Findings:"
        ]

        for finding in investigation.key_findings:
            summary_parts.append(f"  • {finding}")

        if investigation.thoughts:
            summary_parts.extend(["", "🧠 Brain's Strategic Thoughts:"])
            for thought in investigation.thoughts[-3:]:  # Show last 3 thoughts
                summary_parts.append(f"  💭 {thought.content} ({thought.confidence:.0%} confidence)")

        if investigation.recommendations:
            summary_parts.extend(["", "🎯 Brain's Recommendations:"])
            for rec in investigation.recommendations:
                summary_parts.append(f"  • {rec}")

        summary_parts.extend([
            "",
            f"🛡️ Risk Score: {investigation.risk_score:.1%}",
            f"🧠 Brain's Final Assessment: {investigation.final_assessment}",
            "",
            f"{self._get_brain_catchphrase('completion')}"
        ])

        return "\n".join(summary_parts)


# Global Brain instance
brain = Brain()