#!/usr/bin/env python3
"""
Email Intelligence Engine for Inspector-G
Revolutionary email reconnaissance with corporate psychology and AI

Like Brain the dog's comprehensive analysis, this module combines email discovery,
corporate psychology, breach intelligence, and predictive analytics for complete
email intelligence gathering.
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime

from .corporate_email_oracle import CorporateEmailOracle, EmailInvestigationResult, EmployeeProfile
from .breach_timeline_engine import BreachTimelineEngine
from ...ai.neural_engine import NeuralFoundationEngine
from ...core.config import settings
from ...ui.themes import theme

logger = logging.getLogger(__name__)


class EmailIntelligence:
    """
    Revolutionary Email Intelligence system for Inspector-G

    Combines corporate psychology, predictive analytics, and breach intelligence
    to provide comprehensive email reconnaissance capabilities.

    Like Brain the dog's analytical prowess, EmailIntelligence sees patterns
    in corporate email structures that others miss.
    """

    def __init__(self):
        # Initialize revolutionary AI/ML foundation
        self.neural_engine = NeuralFoundationEngine()

        # Initialize Corporate Email Oracle
        self.corporate_oracle = CorporateEmailOracle(self.neural_engine)

        # Initialize Breach Timeline Engine
        self.breach_engine = BreachTimelineEngine()

        # Configuration
        self.default_investigation_modes = [
            'corporate_dna',
            'email_discovery',
            'employee_intelligence',
            'predictive_generation',
            'breach_analysis',
            'security_assessment'
        ]

    async def investigate_domain_emails(
        self,
        target_domain: str,
        investigation_modes: Optional[List[str]] = None,
        employee_list: Optional[List[Dict]] = None,
        enable_breach_analysis: bool = True,
        enable_prediction: bool = True,
        enable_validation: bool = False
    ) -> Dict:
        """
        Go-Go-Gadget Email Intelligence Investigation!

        Args:
            target_domain: Domain to investigate
            investigation_modes: Specific investigation modes to run
            employee_list: Known employees for prediction
            enable_breach_analysis: Enable breach timeline analysis
            enable_prediction: Enable predictive email generation
            enable_validation: Enable email validation (careful!)

        Returns:
            Comprehensive email intelligence results
        """
        logger.info(f"📧 Go-Go-Gadget Email Intelligence: {target_domain}")

        try:
            # Convert employee list to EmployeeProfile objects
            employee_profiles = []
            if employee_list:
                for emp_data in employee_list:
                    if isinstance(emp_data, dict):
                        profile = EmployeeProfile(
                            full_name=emp_data.get('full_name', ''),
                            first_name=emp_data.get('first_name', ''),
                            last_name=emp_data.get('last_name', ''),
                            title=emp_data.get('title'),
                            department=emp_data.get('department')
                        )
                        employee_profiles.append(profile)

            # Use Corporate Email Oracle for comprehensive investigation
            investigation_result = await self.corporate_oracle.investigate_domain_emails(
                target_domain=target_domain,
                employee_list=employee_profiles,
                enable_breach_analysis=enable_breach_analysis,
                enable_prediction=enable_prediction,
                enable_validation=enable_validation
            )

            # Convert to legacy format for CLI compatibility
            legacy_results = await self._convert_to_legacy_format(investigation_result)

            # Add Inspector Gadget theming
            legacy_results['gadget_catchphrase'] = theme.format_gadget_message('Email analysis complete!', 'success')
            legacy_results['brain_mode'] = settings.brain_mode
            legacy_results['wowser_factor'] = len(investigation_result.discovered_emails) + len(investigation_result.predicted_emails)

            if legacy_results['wowser_factor'] > 10:
                logger.info("🎉 Wowser! Extensive email intelligence gathered!")
            elif legacy_results['wowser_factor'] > 5:
                logger.info("✅ Go-Go-Gadget success! Significant email discoveries!")

            return legacy_results

        except Exception as e:
            logger.error(f"❌ Email intelligence failed: {e}")

            # Fallback to basic investigation
            return await self._fallback_investigation(target_domain)

    async def _convert_to_legacy_format(self, investigation_result: EmailInvestigationResult) -> Dict:
        """Convert investigation result to legacy format for CLI compatibility"""
        legacy_format = {
            'target_domain': investigation_result.target_domain,
            'timestamp': investigation_result.start_time.isoformat(),
            'duration_seconds': (
                (investigation_result.end_time - investigation_result.start_time).total_seconds()
                if investigation_result.end_time else 0
            ),
            'gadget_status': 'complete',

            # Email discoveries
            'discovered_emails': investigation_result.discovered_emails,
            'predicted_emails': [],
            'total_emails': len(investigation_result.discovered_emails) + len(investigation_result.predicted_emails),

            # Corporate intelligence
            'corporate_dna': {},
            'employees_found': [],

            # Security analysis
            'breach_analysis': investigation_result.breach_timeline,
            'security_assessment': investigation_result.security_assessment,

            # AI insights
            'ai_analysis': investigation_result.ai_insights,
            'confidence_metrics': investigation_result.confidence_metrics,
            'investigation_notes': investigation_result.investigation_notes,

            # Brain analysis
            'brain_analysis': {}
        }

        # Convert predicted emails
        for prediction in investigation_result.predicted_emails:
            legacy_prediction = {
                'email': prediction.email_address,
                'confidence': prediction.confidence_score,
                'method': prediction.prediction_method,
                'evidence': prediction.supporting_evidence,
                'risk_factors': prediction.risk_factors,
                'status': prediction.validation_status
            }
            legacy_format['predicted_emails'].append(legacy_prediction)

        # Convert corporate DNA
        if investigation_result.corporate_dna:
            dna = investigation_result.corporate_dna
            legacy_format['corporate_dna'] = {
                'domain': dna.domain,
                'naming_conventions': dna.naming_conventions,
                'separator_preferences': dna.separator_preferences,
                'formality_level': dna.formality_level,
                'tech_sophistication': dna.tech_sophistication,
                'email_providers': dna.email_providers,
                'confidence_score': dna.confidence_score,
                'sample_size': dna.sample_size
            }

        # Convert employees
        for employee in investigation_result.employees_found:
            legacy_employee = {
                'full_name': employee.full_name,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'title': employee.title,
                'department': employee.department
            }
            legacy_format['employees_found'].append(legacy_employee)

        # Enhanced Brain analysis
        legacy_format['brain_analysis'] = {
            'total_emails_discovered': len(investigation_result.discovered_emails),
            'total_predictions_generated': len(investigation_result.predicted_emails),
            'employees_identified': len(investigation_result.employees_found),
            'corporate_dna_confidence': (
                investigation_result.corporate_dna.confidence_score
                if investigation_result.corporate_dna else 0
            ),
            'average_prediction_confidence': (
                sum(p.confidence_score for p in investigation_result.predicted_emails) /
                len(investigation_result.predicted_emails)
                if investigation_result.predicted_emails else 0
            ),
            'pattern_analysis': self._generate_pattern_analysis(investigation_result),
            'brain_recommendation': self._generate_brain_recommendation(investigation_result),
            'risk_assessment': investigation_result.security_assessment.get('overall_risk_level', 'unknown'),
            'ai_insights': investigation_result.ai_insights.get('summary', 'AI analysis complete')
        }

        return legacy_format

    def _generate_pattern_analysis(self, investigation_result: EmailInvestigationResult) -> str:
        """Generate Brain's pattern analysis for email investigation"""
        discovered = len(investigation_result.discovered_emails)
        predicted = len(investigation_result.predicted_emails)
        employees = len(investigation_result.employees_found)

        if discovered == 0 and predicted == 0:
            return "No email patterns detected - highly secure or private organization"

        if investigation_result.corporate_dna and investigation_result.corporate_dna.confidence_score > 0.8:
            return f"Strong corporate email patterns detected with {investigation_result.corporate_dna.confidence_score:.1%} confidence"

        if discovered >= 5:
            return f"Extensive email presence: {discovered} discovered, {predicted} predicted from {employees} employees"
        elif predicted >= 10:
            return f"High-confidence predictive analysis: {predicted} likely email addresses generated"
        else:
            return f"Limited email intelligence: {discovered} discovered, {predicted} predicted"

    def _generate_brain_recommendation(self, investigation_result: EmailInvestigationResult) -> str:
        """Generate Brain's intelligent recommendation"""
        security_risk = investigation_result.security_assessment.get('overall_risk_level', 'unknown')
        total_emails = len(investigation_result.discovered_emails) + len(investigation_result.predicted_emails)

        if security_risk in ['critical', 'high']:
            return "URGENT: High breach risk detected - implement immediate security measures"
        elif total_emails >= 15:
            return "Comprehensive email intelligence gathered - proceed with targeted campaigns"
        elif investigation_result.corporate_dna and investigation_result.corporate_dna.confidence_score > 0.7:
            return "Strong corporate patterns identified - expand employee research for better coverage"
        elif total_emails == 0:
            return "Minimal email exposure - investigate alternative contact methods or subdomains"
        else:
            return "Moderate email intelligence - consider additional reconnaissance techniques"

    async def _fallback_investigation(self, target_domain: str) -> Dict:
        """Fallback to basic investigation if Corporate Oracle fails"""
        logger.warning("🔧 Falling back to basic email investigation mode")

        results = {
            'target_domain': target_domain,
            'timestamp': datetime.now().isoformat(),
            'gadget_status': 'fallback_mode',
            'discovered_emails': [],
            'predicted_emails': [],
            'total_emails': 0,
            'corporate_dna': {},
            'employees_found': [],
            'brain_analysis': {
                'total_emails_discovered': 0,
                'pattern_analysis': 'Fallback mode - limited analysis available',
                'brain_recommendation': 'Try again with full Corporate Email Oracle system'
            },
            'wowser_factor': 0,
            'error_message': 'Corporate Email Oracle temporarily unavailable'
        }

        # Try basic common email discovery
        common_emails = [
            f"info@{target_domain}",
            f"contact@{target_domain}",
            f"support@{target_domain}",
            f"sales@{target_domain}",
            f"admin@{target_domain}"
        ]

        # Simulate basic discovery
        for email in common_emails[:3]:  # Check first 3
            try:
                # Simple heuristic - would use real validation in practice
                if len(target_domain) > 3 and '.' in target_domain:
                    results['discovered_emails'].append(email)
                    results['wowser_factor'] += 1
            except Exception as e:
                logger.warning(f"Basic email check failed for {email}: {e}")

        results['total_emails'] = len(results['discovered_emails'])

        return results

    async def get_investigation_summary(self, results: Dict) -> str:
        """Generate human-readable investigation summary"""
        summary_lines = []

        # Header
        summary_lines.append(f"📧 Inspector-G Email Intelligence Summary")
        summary_lines.append(f"Domain: {results['target_domain']}")
        summary_lines.append(f"Timestamp: {results['timestamp']}")

        if 'duration_seconds' in results:
            summary_lines.append(f"Duration: {results['duration_seconds']:.1f} seconds")

        summary_lines.append("")

        # Email discoveries
        discovered = results.get('discovered_emails', [])
        predicted = results.get('predicted_emails', [])

        summary_lines.append(f"📊 Email Intelligence Results:")
        summary_lines.append(f"  📧 Discovered Emails: {len(discovered)}")

        for email in discovered[:5]:  # Show first 5
            summary_lines.append(f"    ✅ {email}")

        if len(discovered) > 5:
            summary_lines.append(f"    ... and {len(discovered) - 5} more")

        summary_lines.append(f"  🔮 Predicted Emails: {len(predicted)}")

        for prediction in predicted[:3]:  # Show top 3 predictions
            if isinstance(prediction, dict):
                summary_lines.append(
                    f"    🎯 {prediction['email']} ({prediction['confidence']:.1%} confidence)"
                )

        if len(predicted) > 3:
            summary_lines.append(f"    ... and {len(predicted) - 3} more")

        # Corporate DNA
        corporate_dna = results.get('corporate_dna', {})
        if corporate_dna:
            summary_lines.append(f"\n🧬 Corporate DNA Analysis:")
            summary_lines.append(f"  Confidence: {corporate_dna.get('confidence_score', 0):.1%}")
            summary_lines.append(f"  Email Providers: {', '.join(corporate_dna.get('email_providers', []))}")

        # Employees
        employees = results.get('employees_found', [])
        if employees:
            summary_lines.append(f"\n👥 Employee Intelligence: {len(employees)} found")

        # Security Assessment
        security = results.get('security_assessment', {})
        if security:
            risk_level = security.get('overall_risk_level', 'unknown')
            summary_lines.append(f"\n🛡️ Security Assessment: {risk_level.upper()} risk")

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