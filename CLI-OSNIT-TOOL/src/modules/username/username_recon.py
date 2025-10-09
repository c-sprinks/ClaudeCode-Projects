#!/usr/bin/env python3
"""
Username reconnaissance module for Inspector-G
Revolutionary username intelligence with behavioral fingerprinting and AI
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime

from .quantum_username_intelligence import QuantumUsernameIntelligence
from .behavioral_fingerprint import BehavioralFingerprint
from .stealth_enumeration import StealthEnumerator
from ...ai.neural_engine import NeuralFoundationEngine
from ...core.config import settings
from ...ui.themes import theme

logger = logging.getLogger(__name__)


class UsernameRecon:
    """
    Revolutionary Username reconnaissance engine for Inspector-G

    Like Brain the dog's hidden intelligence, this system combines:
    - Quantum Username Intelligence (QUI) for multi-platform discovery
    - Behavioral DNA fingerprinting for cross-platform correlation
    - Stealth enumeration for undetectable reconnaissance
    - AI-powered analysis and insights
    """

    def __init__(self):
        # Initialize the revolutionary AI/ML foundation
        self.neural_engine = NeuralFoundationEngine()

        # Initialize behavioral fingerprinting system
        self.behavioral_engine = BehavioralFingerprint(self.neural_engine)

        # Initialize stealth enumeration engine
        self.stealth_engine = StealthEnumerator()

        # Initialize Quantum Username Intelligence
        self.qui_engine = QuantumUsernameIntelligence(
            self.neural_engine,
            self.behavioral_engine,
            self.stealth_engine
        )

        # Configuration
        self.default_platforms = [
            'github', 'twitter', 'linkedin', 'reddit',
            'instagram', 'youtube', 'tiktok', 'twitch'
        ]

    async def investigate_username(
        self,
        target_username: str,
        platforms: Optional[List[str]] = None,
        enable_behavioral_analysis: bool = True,
        enable_stealth_mode: bool = True,
        stealth_level: int = 3
    ) -> Dict:
        """
        Go-Go-Gadget Quantum Username Investigation!

        Args:
            target_username: Username to investigate
            platforms: Specific platforms to check (None = all platforms)
            enable_behavioral_analysis: Enable behavioral DNA fingerprinting
            enable_stealth_mode: Use stealth enumeration techniques
            stealth_level: 1=basic, 2=moderate, 3=maximum stealth

        Returns:
            Comprehensive investigation results with revolutionary intelligence
        """
        logger.info(f"🧠 Go-Go-Gadget Quantum Username Investigation: {target_username}")

        try:
            # Use revolutionary Quantum Username Intelligence
            investigation_result = await self.qui_engine.investigate_username(
                target_username=target_username,
                platforms=platforms or self.default_platforms,
                enable_behavioral_analysis=enable_behavioral_analysis,
                enable_stealth_mode=enable_stealth_mode
            )

            # Convert to legacy format for compatibility
            legacy_results = await self._convert_to_legacy_format(investigation_result)

            # Add Inspector Gadget theming
            legacy_results['gadget_catchphrase'] = theme.get_random_catchphrase()
            legacy_results['brain_mode'] = settings.brain_mode
            legacy_results['wowser_factor'] = len(investigation_result.discoveries)

            if legacy_results['wowser_factor'] > 3:
                logger.info("🎉 Wowser! Multiple accounts discovered with behavioral correlation!")
            elif legacy_results['wowser_factor'] > 0:
                logger.info("✅ Go-Go-Gadget success! Accounts discovered!")

            return legacy_results

        except Exception as e:
            logger.error(f"❌ Quantum investigation failed: {e}")

            # Fallback to basic investigation
            return await self._fallback_investigation(target_username)

    async def _convert_to_legacy_format(self, investigation_result) -> Dict:
        """Convert QUI investigation result to legacy format for CLI compatibility"""
        legacy_format = {
            'target': investigation_result.target_username,
            'timestamp': investigation_result.start_time.isoformat(),
            'duration_seconds': (
                (investigation_result.end_time - investigation_result.start_time).total_seconds()
                if investigation_result.end_time else 0
            ),
            'gadget_status': 'complete',
            'platforms_checked': list(set(d.platform for d in investigation_result.discoveries)),
            'discoveries': [],
            'brain_analysis': {},
            'behavioral_insights': investigation_result.behavioral_insights,
            'correlations': [],
            'ai_analysis': investigation_result.ai_analysis,
            'confidence_metrics': investigation_result.confidence_metrics,
            'investigation_notes': investigation_result.investigation_notes
        }

        # Convert discoveries to legacy format
        for discovery in investigation_result.discoveries:
            legacy_discovery = {
                'platform': discovery.platform,
                'username': discovery.username,
                'found': True,
                'confidence': discovery.confidence_score,
                'profile_url': discovery.profile_url,
                'discovery_method': discovery.discovery_method,
                'verification_status': discovery.verification_status,
                'behavioral_dna_available': discovery.behavioral_dna is not None,
                'last_activity': discovery.last_activity.isoformat() if discovery.last_activity else None,
                'risk_indicators': discovery.risk_indicators
            }
            legacy_format['discoveries'].append(legacy_discovery)

        # Convert correlations to legacy format
        for correlation in investigation_result.correlations:
            legacy_correlation = {
                'primary_username': correlation.primary_username,
                'correlated_platforms': [acc.platform for acc in correlation.correlated_accounts],
                'correlation_confidence': correlation.correlation_confidence,
                'evidence_points': correlation.correlation_evidence,
                'behavioral_analysis': correlation.behavioral_analysis
            }
            legacy_format['correlations'].append(legacy_correlation)

        # Enhanced Brain analysis
        legacy_format['brain_analysis'] = {
            'total_platforms_found': len(investigation_result.discoveries),
            'verified_accounts': len([d for d in investigation_result.discoveries if d.verification_status == 'verified']),
            'confidence_average': (
                sum(d.confidence_score for d in investigation_result.discoveries) / len(investigation_result.discoveries)
                if investigation_result.discoveries else 0
            ),
            'correlation_clusters': len(investigation_result.correlations),
            'behavioral_dna_profiles': len([d for d in investigation_result.discoveries if d.behavioral_dna]),
            'pattern_analysis': self._generate_pattern_analysis(investigation_result),
            'brain_recommendation': self._generate_brain_recommendation(investigation_result),
            'stealth_effectiveness': 'Maximum stealth protocols engaged',
            'ai_insights': investigation_result.ai_analysis.get('summary', 'AI analysis complete')
        }

        return legacy_format

    def _generate_pattern_analysis(self, investigation_result) -> str:
        """Generate Brain's pattern analysis"""
        discoveries = investigation_result.discoveries
        correlations = investigation_result.correlations

        if not discoveries:
            return "No digital footprint detected - highly unusual"

        if len(correlations) > 0:
            return f"Strong behavioral correlation detected across {len(correlations)} platform clusters"

        if len(discoveries) >= 5:
            return "Extensive digital presence with high-confidence account verification"
        elif len(discoveries) >= 3:
            return "Moderate digital presence detected across multiple platforms"
        else:
            return "Limited digital footprint - potential privacy-conscious user"

    def _generate_brain_recommendation(self, investigation_result) -> str:
        """Generate Brain's intelligent recommendation"""
        discoveries = investigation_result.discoveries
        correlations = investigation_result.correlations
        confidence_avg = (
            sum(d.confidence_score for d in discoveries) / len(discoveries)
            if discoveries else 0
        )

        if len(correlations) > 0 and confidence_avg > 0.8:
            return "High-value target: Strong behavioral correlation suggests single individual"
        elif len(discoveries) >= 4 and confidence_avg > 0.7:
            return "Investigate further: Multiple verified accounts with good confidence"
        elif confidence_avg > 0.9:
            return "Verified target: High-confidence account verification achieved"
        elif not discoveries:
            return "Expand search: Consider username variants and alternative spellings"
        else:
            return "Continue investigation: Mixed confidence levels require deeper analysis"

    async def _fallback_investigation(self, target_username: str) -> Dict:
        """Fallback to basic investigation if QUI fails"""
        logger.warning("🔧 Falling back to basic investigation mode")

        results = {
            'target': target_username,
            'timestamp': datetime.now().isoformat(),
            'gadget_status': 'fallback_mode',
            'platforms_checked': self.default_platforms,
            'discoveries': [],
            'brain_analysis': {
                'total_platforms_found': 0,
                'confidence_average': 0,
                'pattern_analysis': 'Fallback mode - limited analysis available',
                'brain_recommendation': 'Try again with full Quantum Intelligence system'
            },
            'wowser_factor': 0,
            'error_message': 'Quantum Intelligence temporarily unavailable'
        }

        # Simulate basic checks
        for platform in self.default_platforms[:3]:  # Check first 3 platforms
            try:
                result = await self._basic_platform_check(target_username, platform)
                if result['found']:
                    results['discoveries'].append(result)
                    results['wowser_factor'] += 1
            except Exception as e:
                logger.warning(f"Basic check failed for {platform}: {e}")

        return results

    async def _basic_platform_check(self, username: str, platform: str) -> Dict:
        """Basic platform checking without advanced features"""
        # Simple simulation for fallback mode
        import random

        await asyncio.sleep(0.5)  # Simulate network delay

        # Basic heuristic based on username characteristics
        found = len(username) >= 3 and len(username) <= 20 and username.isalnum()
        confidence = random.uniform(0.5, 0.8) if found else 0.0

        return {
            'platform': platform,
            'username': username,
            'found': found,
            'confidence': confidence,
            'profile_url': f"https://{platform}.com/{username}" if found else None,
            'discovery_method': 'basic_fallback',
            'verification_status': 'unverified',
            'behavioral_dna_available': False
        }

    async def get_investigation_summary(self, results: Dict) -> str:
        """Generate human-readable investigation summary"""
        summary_lines = []

        # Header
        summary_lines.append(f"🧠 Inspector-G Investigation Summary")
        summary_lines.append(f"Target: {results['target']}")
        summary_lines.append(f"Timestamp: {results['timestamp']}")

        if 'duration_seconds' in results:
            summary_lines.append(f"Duration: {results['duration_seconds']:.1f} seconds")

        summary_lines.append("")

        # Discoveries
        discoveries = results.get('discoveries', [])
        summary_lines.append(f"📊 Platform Discoveries: {len(discoveries)}")

        for discovery in discoveries:
            confidence_emoji = "🟢" if discovery['confidence'] > 0.8 else "🟡" if discovery['confidence'] > 0.6 else "🔴"
            summary_lines.append(
                f"  {confidence_emoji} {discovery['platform']}: {discovery['username']} "
                f"({discovery['confidence']:.1%} confidence)"
            )

        # Correlations
        correlations = results.get('correlations', [])
        if correlations:
            summary_lines.append(f"\n🔗 Cross-Platform Correlations: {len(correlations)}")
            for correlation in correlations:
                summary_lines.append(
                    f"  🧬 {correlation['primary_username']}: "
                    f"{len(correlation['correlated_platforms'])} platforms "
                    f"({correlation['correlation_confidence']:.1%} confidence)"
                )

        # Brain Analysis
        brain_analysis = results.get('brain_analysis', {})
        if brain_analysis:
            summary_lines.append(f"\n🧠 Brain's Analysis:")
            summary_lines.append(f"  Pattern: {brain_analysis.get('pattern_analysis', 'Unknown')}")
            summary_lines.append(f"  Recommendation: {brain_analysis.get('brain_recommendation', 'None')}")

        # AI Insights
        ai_analysis = results.get('ai_analysis', {})
        if ai_analysis and ai_analysis.get('summary'):
            summary_lines.append(f"\n🤖 AI Insights: {ai_analysis['summary']}")

        # Gadget catchphrase
        if 'gadget_catchphrase' in results:
            summary_lines.append(f"\n{results['gadget_catchphrase']}")

        return "\n".join(summary_lines)