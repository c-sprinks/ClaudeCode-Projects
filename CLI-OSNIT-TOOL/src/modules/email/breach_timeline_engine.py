#!/usr/bin/env python3
"""
Breach Timeline Engine for Inspector-G
Advanced breach analysis and timeline reconstruction

Like Brain the dog's memory for past events, this engine tracks email
exposure across time to build comprehensive breach intelligence.
"""

import asyncio
import aiohttp
import hashlib
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class BreachEvent:
    """Single breach event"""
    breach_name: str
    breach_date: datetime
    domain: str
    emails_affected: List[str]
    breach_type: str  # credential, email_only, full_profile, etc.
    data_types: List[str]  # passwords, emails, names, etc.
    severity_score: float  # 0-1 scale
    source: str  # hibp, manual, etc.
    verified: bool = False


@dataclass
class EmailTimeline:
    """Timeline for a specific email address"""
    email_address: str
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    breach_events: List[BreachEvent] = field(default_factory=list)
    total_breaches: int = 0
    risk_score: float = 0.0
    exposure_years: int = 0


@dataclass
class DomainBreachAnalysis:
    """Complete breach analysis for a domain"""
    domain: str
    analysis_date: datetime
    email_timelines: Dict[str, EmailTimeline] = field(default_factory=dict)
    breach_summary: Dict[str, Any] = field(default_factory=dict)
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class BreachTimelineEngine:
    """
    Advanced breach timeline analysis for Inspector-G

    Tracks email exposure across time using multiple data sources
    to build comprehensive breach intelligence with timeline reconstruction.
    """

    def __init__(self):
        # Configuration
        self.request_delay = 2.0  # Respectful rate limiting
        self.max_concurrent_requests = 3

        # Known breach data sources
        self.breach_sources = {
            'hibp': {
                'api_url': 'https://haveibeenpwned.com/api/v3',
                'rate_limit': 1.5,  # seconds between requests
                'requires_key': False  # For basic breach checking
            }
        }

        # Breach severity weights
        self.severity_weights = {
            'passwords': 1.0,
            'emails': 0.6,
            'names': 0.4,
            'addresses': 0.7,
            'phone_numbers': 0.8,
            'financial': 1.0,
            'social_security': 1.0,
            'credit_cards': 1.0
        }

    async def analyze_domain_breaches(
        self,
        domain: str,
        known_emails: List[str] = None
    ) -> DomainBreachAnalysis:
        """
        Analyze breach timeline for domain and associated emails

        Args:
            domain: Target domain to analyze
            known_emails: List of known emails to check

        Returns:
            Complete domain breach analysis
        """
        logger.info(f"🕰️ Analyzing breach timeline for domain: {domain}")

        analysis = DomainBreachAnalysis(
            domain=domain,
            analysis_date=datetime.now()
        )

        try:
            # If no emails provided, try to discover some
            if not known_emails:
                known_emails = await self._discover_domain_emails(domain)

            # Analyze each email
            for email in known_emails:
                timeline = await self._analyze_email_timeline(email)
                analysis.email_timelines[email] = timeline

            # Generate domain summary
            analysis.breach_summary = await self._generate_domain_summary(analysis)

            # Risk assessment
            analysis.risk_assessment = await self._assess_domain_risk(analysis)

            # Generate recommendations
            analysis.recommendations = await self._generate_recommendations(analysis)

            logger.info(f"✅ Breach analysis complete: {len(analysis.email_timelines)} emails analyzed")
            return analysis

        except Exception as e:
            logger.error(f"❌ Breach timeline analysis failed: {e}")
            raise

    async def _discover_domain_emails(self, domain: str) -> List[str]:
        """Discover emails for domain from various sources"""
        emails = []

        # Common email patterns to check
        common_emails = [
            f"info@{domain}",
            f"contact@{domain}",
            f"support@{domain}",
            f"admin@{domain}",
            f"sales@{domain}",
            f"hello@{domain}"
        ]

        # Check which ones exist in breach databases
        for email in common_emails:
            try:
                has_breaches = await self._check_email_in_breaches(email)
                if has_breaches:
                    emails.append(email)
            except:
                continue

        return emails

    async def _analyze_email_timeline(self, email: str) -> EmailTimeline:
        """Analyze complete timeline for a specific email address"""
        logger.info(f"📧 Analyzing timeline for: {email}")

        timeline = EmailTimeline(email_address=email)

        try:
            # Check Have I Been Pwned
            hibp_breaches = await self._check_hibp_breaches(email)
            timeline.breach_events.extend(hibp_breaches)

            # Calculate timeline metrics
            if timeline.breach_events:
                dates = [event.breach_date for event in timeline.breach_events if event.breach_date]
                if dates:
                    timeline.first_seen = min(dates)
                    timeline.last_seen = max(dates)
                    timeline.exposure_years = (timeline.last_seen - timeline.first_seen).days // 365

                timeline.total_breaches = len(timeline.breach_events)
                timeline.risk_score = await self._calculate_email_risk_score(timeline)

            logger.info(f"✅ Email timeline: {timeline.total_breaches} breaches, risk score: {timeline.risk_score:.2f}")
            return timeline

        except Exception as e:
            logger.warning(f"Email timeline analysis failed for {email}: {e}")
            return timeline

    async def _check_email_in_breaches(self, email: str) -> bool:
        """Quick check if email exists in any breach database"""
        try:
            hibp_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email.lower()}"

            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Inspector-G/1.0 (Educational OSINT Tool)'
                }

                await asyncio.sleep(self.request_delay)

                async with session.get(hibp_url, headers=headers) as response:
                    return response.status == 200

        except Exception:
            return False

    async def _check_hibp_breaches(self, email: str) -> List[BreachEvent]:
        """Check Have I Been Pwned for email breaches"""
        breach_events = []

        try:
            hibp_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email.lower()}"

            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Inspector-G/1.0 (Educational OSINT Tool)'
                }

                await asyncio.sleep(self.request_delay)

                async with session.get(hibp_url, headers=headers) as response:
                    if response.status == 200:
                        breaches = await response.json()

                        for breach_data in breaches:
                            breach_event = self._parse_hibp_breach(email, breach_data)
                            breach_events.append(breach_event)

                    elif response.status == 404:
                        # Email not found in breaches (good news!)
                        logger.info(f"✅ Email {email} not found in HIBP breaches")

        except Exception as e:
            logger.warning(f"HIBP breach check failed for {email}: {e}")

        return breach_events

    def _parse_hibp_breach(self, email: str, breach_data: Dict) -> BreachEvent:
        """Parse HIBP breach data into BreachEvent"""
        # Parse breach date
        breach_date = None
        if breach_data.get('BreachDate'):
            try:
                breach_date = datetime.strptime(breach_data['BreachDate'], '%Y-%m-%d')
            except:
                pass

        # Parse data types
        data_types = breach_data.get('DataClasses', [])

        # Calculate severity score
        severity_score = self._calculate_breach_severity(data_types)

        return BreachEvent(
            breach_name=breach_data.get('Name', 'Unknown'),
            breach_date=breach_date,
            domain=breach_data.get('Domain', ''),
            emails_affected=[email],
            breach_type='credential' if 'Passwords' in data_types else 'email_only',
            data_types=data_types,
            severity_score=severity_score,
            source='hibp',
            verified=breach_data.get('IsVerified', False)
        )

    def _calculate_breach_severity(self, data_types: List[str]) -> float:
        """Calculate severity score based on data types exposed"""
        if not data_types:
            return 0.1

        severity = 0.0
        for data_type in data_types:
            # Normalize data type name
            normalized_type = data_type.lower().replace(' ', '_')

            # Map common HIBP data types to our severity weights
            type_mapping = {
                'passwords': 'passwords',
                'email_addresses': 'emails',
                'names': 'names',
                'usernames': 'names',
                'phone_numbers': 'phone_numbers',
                'geographic_locations': 'addresses',
                'credit_cards': 'credit_cards',
                'social_security_numbers': 'social_security'
            }

            mapped_type = type_mapping.get(normalized_type, 'emails')
            severity += self.severity_weights.get(mapped_type, 0.3)

        # Normalize to 0-1 scale
        return min(severity / len(data_types), 1.0)

    async def _calculate_email_risk_score(self, timeline: EmailTimeline) -> float:
        """Calculate overall risk score for email"""
        if not timeline.breach_events:
            return 0.0

        factors = []

        # Number of breaches factor
        breach_factor = min(timeline.total_breaches / 10, 1.0)  # Normalize to max 10 breaches
        factors.append(breach_factor)

        # Severity factor (average of all breaches)
        severity_scores = [event.severity_score for event in timeline.breach_events]
        avg_severity = sum(severity_scores) / len(severity_scores)
        factors.append(avg_severity)

        # Recency factor (more recent breaches = higher risk)
        if timeline.last_seen:
            days_since_last = (datetime.now() - timeline.last_seen).days
            recency_factor = max(0, 1 - (days_since_last / 365))  # Decay over 1 year
            factors.append(recency_factor)

        # Password breach factor
        password_breaches = [e for e in timeline.breach_events if 'passwords' in [dt.lower() for dt in e.data_types]]
        password_factor = min(len(password_breaches) / 3, 1.0)  # Normalize to max 3 password breaches
        factors.append(password_factor)

        # Calculate weighted average
        weights = [0.3, 0.4, 0.2, 0.1]  # Severity most important, then count, recency, password
        risk_score = sum(f * w for f, w in zip(factors, weights))

        return min(risk_score, 1.0)

    async def _generate_domain_summary(self, analysis: DomainBreachAnalysis) -> Dict[str, Any]:
        """Generate summary statistics for domain breach analysis"""
        summary = {
            'total_emails_checked': len(analysis.email_timelines),
            'emails_with_breaches': 0,
            'total_breaches': 0,
            'unique_breach_sources': set(),
            'average_risk_score': 0.0,
            'highest_risk_email': None,
            'oldest_breach_date': None,
            'most_recent_breach_date': None,
            'common_data_types': defaultdict(int)
        }

        emails_with_breaches = []
        all_breach_dates = []
        all_risk_scores = []

        for email, timeline in analysis.email_timelines.items():
            if timeline.breach_events:
                summary['emails_with_breaches'] += 1
                emails_with_breaches.append((email, timeline.risk_score))

                summary['total_breaches'] += timeline.total_breaches
                all_risk_scores.append(timeline.risk_score)

                # Collect breach sources and dates
                for event in timeline.breach_events:
                    summary['unique_breach_sources'].add(event.source)
                    if event.breach_date:
                        all_breach_dates.append(event.breach_date)

                    # Count data types
                    for data_type in event.data_types:
                        summary['common_data_types'][data_type] += 1

        # Calculate aggregated metrics
        if all_risk_scores:
            summary['average_risk_score'] = sum(all_risk_scores) / len(all_risk_scores)

        if emails_with_breaches:
            highest_risk = max(emails_with_breaches, key=lambda x: x[1])
            summary['highest_risk_email'] = {
                'email': highest_risk[0],
                'risk_score': highest_risk[1]
            }

        if all_breach_dates:
            summary['oldest_breach_date'] = min(all_breach_dates)
            summary['most_recent_breach_date'] = max(all_breach_dates)

        # Convert sets to lists for JSON serialization
        summary['unique_breach_sources'] = list(summary['unique_breach_sources'])
        summary['common_data_types'] = dict(summary['common_data_types'])

        return summary

    async def _assess_domain_risk(self, analysis: DomainBreachAnalysis) -> Dict[str, Any]:
        """Assess overall domain risk based on breach analysis"""
        risk_assessment = {
            'overall_risk_level': 'low',
            'risk_score': 0.0,
            'risk_factors': [],
            'protection_status': 'unknown',
            'exposure_timeline': {},
            'threat_indicators': []
        }

        summary = analysis.breach_summary

        # Calculate overall risk score
        risk_factors = []

        # Factor 1: Percentage of emails breached
        if summary['total_emails_checked'] > 0:
            breach_percentage = summary['emails_with_breaches'] / summary['total_emails_checked']
            risk_factors.append(breach_percentage)

            if breach_percentage > 0.7:
                risk_assessment['risk_factors'].append(f"High breach rate: {breach_percentage:.1%} of emails compromised")

        # Factor 2: Average risk score
        avg_risk = summary.get('average_risk_score', 0)
        risk_factors.append(avg_risk)

        if avg_risk > 0.7:
            risk_assessment['risk_factors'].append(f"High average risk score: {avg_risk:.2f}")

        # Factor 3: Recent breach activity
        if summary.get('most_recent_breach_date'):
            days_since_recent = (datetime.now() - summary['most_recent_breach_date']).days
            recency_factor = max(0, 1 - (days_since_recent / 365))
            risk_factors.append(recency_factor)

            if days_since_recent < 180:  # Recent breach within 6 months
                risk_assessment['risk_factors'].append(f"Recent breach activity: {days_since_recent} days ago")

        # Factor 4: Sensitive data exposure
        common_data_types = summary.get('common_data_types', {})
        sensitive_types = ['Passwords', 'Credit cards', 'Social security numbers', 'Phone numbers']
        sensitive_exposure = any(data_type in common_data_types for data_type in sensitive_types)

        if sensitive_exposure:
            risk_factors.append(0.8)
            risk_assessment['risk_factors'].append("Sensitive data types exposed in breaches")

        # Calculate overall risk score
        if risk_factors:
            risk_assessment['risk_score'] = sum(risk_factors) / len(risk_factors)
        else:
            risk_assessment['risk_score'] = 0.0

        # Determine risk level
        risk_score = risk_assessment['risk_score']
        if risk_score >= 0.8:
            risk_assessment['overall_risk_level'] = 'critical'
        elif risk_score >= 0.6:
            risk_assessment['overall_risk_level'] = 'high'
        elif risk_score >= 0.4:
            risk_assessment['overall_risk_level'] = 'medium'
        elif risk_score >= 0.2:
            risk_assessment['overall_risk_level'] = 'low'
        else:
            risk_assessment['overall_risk_level'] = 'minimal'

        return risk_assessment

    async def _generate_recommendations(self, analysis: DomainBreachAnalysis) -> List[str]:
        """Generate security recommendations based on breach analysis"""
        recommendations = []

        summary = analysis.breach_summary
        risk_assessment = analysis.risk_assessment

        # High-risk recommendations
        if risk_assessment['overall_risk_level'] in ['critical', 'high']:
            recommendations.append("🚨 URGENT: Implement mandatory password reset for all affected accounts")
            recommendations.append("🔐 Enable multi-factor authentication (MFA) across all systems")
            recommendations.append("📧 Consider migrating to new email addresses for high-risk accounts")

        # Medium-risk recommendations
        elif risk_assessment['overall_risk_level'] == 'medium':
            recommendations.append("🔄 Encourage password updates for affected accounts")
            recommendations.append("🛡️ Implement additional security monitoring")

        # General recommendations based on breach data
        common_data_types = summary.get('common_data_types', {})

        if 'Passwords' in common_data_types:
            recommendations.append("🔑 Audit password policies and enforce strong password requirements")

        if 'Email addresses' in common_data_types:
            recommendations.append("📬 Monitor for phishing attempts targeting exposed emails")

        if 'Phone numbers' in common_data_types:
            recommendations.append("📱 Be aware of potential SMS phishing (smishing) attacks")

        # Timeline-based recommendations
        if summary.get('most_recent_breach_date'):
            days_since = (datetime.now() - summary['most_recent_breach_date']).days
            if days_since < 90:
                recommendations.append("⏰ Increase security monitoring due to recent breach activity")

        # If no specific risks found
        if not recommendations:
            recommendations.append("✅ Current exposure appears minimal - maintain standard security practices")
            recommendations.append("🔍 Continue periodic monitoring for new breach activity")

        return recommendations