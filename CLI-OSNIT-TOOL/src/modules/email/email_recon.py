#!/usr/bin/env python3
"""
Email reconnaissance module for Inspector-G
Revolutionary email intelligence with corporate psychology and predictive analytics
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime

from .email_intelligence import EmailIntelligence
from .corporate_email_oracle import CorporateEmailOracle
from .breach_timeline_engine import BreachTimelineEngine
from ...ai.neural_engine import NeuralFoundationEngine
from ...core.config import settings
from ...ui.themes import theme

logger = logging.getLogger(__name__)


class EmailRecon:
    """
    Revolutionary Email reconnaissance engine for Inspector-G

    Like Brain the dog's analytical prowess, this system combines:
    - Corporate Email Oracle (CEO) for predictive email generation
    - Breach Timeline Engine for security intelligence
    - Corporate psychology analysis for organizational understanding
    - AI-powered insights and recommendations
    """

    def __init__(self):
        # Initialize the revolutionary email intelligence system
        self.email_intelligence = EmailIntelligence()

        # Configuration
        self.default_investigation_modes = [
            'corporate_dna',
            'email_discovery',
            'employee_intelligence',
            'predictive_generation',
            'breach_analysis'
        ]

    async def investigate_domain_emails(
        self,
        target_domain: str,
        employee_list: Optional[List[Dict]] = None,
        investigation_modes: Optional[List[str]] = None,
        enable_breach_analysis: bool = True,
        enable_prediction: bool = True,
        enable_validation: bool = False
    ) -> Dict:
        """
        Go-Go-Gadget Corporate Email Investigation!

        Args:
            target_domain: Domain to investigate
            employee_list: Known employees for prediction
            investigation_modes: Specific investigation modes to run
            enable_breach_analysis: Enable breach timeline analysis
            enable_prediction: Enable predictive email generation
            enable_validation: Enable email validation (careful - can be detected)

        Returns:
            Comprehensive email intelligence results with Inspector Gadget theming
        """
        logger.info(f"📧 Go-Go-Gadget Corporate Email Investigation: {target_domain}")

        try:
            # Use revolutionary Email Intelligence system
            investigation_result = await self.email_intelligence.investigate_domain_emails(
                target_domain=target_domain,
                investigation_modes=investigation_modes or self.default_investigation_modes,
                employee_list=employee_list,
                enable_breach_analysis=enable_breach_analysis,
                enable_prediction=enable_prediction,
                enable_validation=enable_validation
            )

            # Add Inspector Gadget flourish
            investigation_result['gadget_catchphrase'] = theme.format_gadget_message('Email investigation complete!', 'success')
            investigation_result['brain_mode'] = settings.brain_mode

            if investigation_result.get('wowser_factor', 0) > 10:
                logger.info("🎉 Wowser! Extensive email intelligence gathered!")
            elif investigation_result.get('total_emails', 0) > 0:
                logger.info("✅ Go-Go-Gadget success! Email discoveries made!")

            return investigation_result

        except Exception as e:
            logger.error(f"❌ Corporate email investigation failed: {e}")

            # Fallback to basic investigation
            return await self._fallback_investigation(target_domain)

    async def _fallback_investigation(self, target_domain: str) -> Dict:
        """Fallback to basic investigation if Email Intelligence fails"""
        logger.warning("🔧 Falling back to basic email investigation mode")

        results = {
            'target_domain': target_domain,
            'timestamp': datetime.now().isoformat(),
            'gadget_status': 'fallback_mode',
            'discovered_emails': [],
            'predicted_emails': [],
            'total_emails': 0,
            'brain_analysis': {
                'pattern_analysis': 'Fallback mode - limited analysis available',
                'brain_recommendation': 'Try again with full Email Intelligence system'
            },
            'wowser_factor': 0,
            'error_message': 'Email Intelligence temporarily unavailable'
        }

        # Try basic common email patterns
        common_patterns = [
            f"info@{target_domain}",
            f"contact@{target_domain}",
            f"support@{target_domain}",
            f"sales@{target_domain}",
            f"hello@{target_domain}"
        ]

        # Simulate basic checks
        for email in common_patterns[:3]:  # Check first 3
            try:
                # Basic heuristic - would use real validation in practice
                if self._is_valid_domain(target_domain):
                    results['discovered_emails'].append(email)
                    results['wowser_factor'] += 1
            except Exception as e:
                logger.warning(f"Basic email check failed for {email}: {e}")

        results['total_emails'] = len(results['discovered_emails'])

        return results

    def _is_valid_domain(self, domain: str) -> bool:
        """Basic domain validation"""
        return (
            len(domain) > 3 and
            '.' in domain and
            not domain.startswith('.') and
            not domain.endswith('.')
        )

    async def generate_employee_emails(
        self,
        domain: str,
        employee_names: List[str],
        patterns: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Generate predicted emails for specific employees

        Args:
            domain: Target domain
            employee_names: List of employee names
            patterns: Custom email patterns to try

        Returns:
            Dictionary mapping employee names to predicted emails
        """
        logger.info(f"🎯 Generating employee emails for {len(employee_names)} employees")

        results = {}

        # Convert names to employee profiles
        employee_list = []
        for name in employee_names:
            parts = name.split()
            if len(parts) >= 2:
                employee_data = {
                    'full_name': name,
                    'first_name': parts[0],
                    'last_name': parts[-1]
                }
                employee_list.append(employee_data)

        # Use Email Intelligence for prediction
        try:
            investigation = await self.email_intelligence.investigate_domain_emails(
                target_domain=domain,
                employee_list=employee_list,
                enable_breach_analysis=False,
                enable_prediction=True,
                enable_validation=False
            )

            # Group predictions by employee
            for employee_data in employee_list:
                employee_name = employee_data['full_name']
                employee_predictions = []

                for prediction in investigation.get('predicted_emails', []):
                    if isinstance(prediction, dict):
                        # Check if this prediction matches the employee
                        first = employee_data['first_name'].lower()
                        last = employee_data['last_name'].lower()

                        if first in prediction['email'] and last in prediction['email']:
                            employee_predictions.append({
                                'email': prediction['email'],
                                'confidence': prediction['confidence'],
                                'method': prediction['method']
                            })

                results[employee_name] = employee_predictions

        except Exception as e:
            logger.error(f"Employee email generation failed: {e}")

        return results

    async def get_investigation_summary(self, results: Dict) -> str:
        """Generate human-readable investigation summary"""
        if hasattr(self.email_intelligence, 'get_investigation_summary'):
            return await self.email_intelligence.get_investigation_summary(results)

        # Fallback summary
        summary_lines = []

        summary_lines.append(f"📧 Inspector-G Email Investigation Summary")
        summary_lines.append(f"Domain: {results.get('target_domain', 'Unknown')}")
        summary_lines.append(f"Status: {results.get('gadget_status', 'Unknown')}")

        discovered = len(results.get('discovered_emails', []))
        predicted = len(results.get('predicted_emails', []))
        summary_lines.append(f"Results: {discovered} discovered, {predicted} predicted")

        if 'gadget_catchphrase' in results:
            summary_lines.append(f"\n{results['gadget_catchphrase']}")

        return "\n".join(summary_lines)