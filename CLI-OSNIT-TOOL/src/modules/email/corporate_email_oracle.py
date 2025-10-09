#!/usr/bin/env python3
"""
Corporate Email Oracle (CEO) for Inspector-G
Revolutionary email intelligence using corporate psychology and predictive analytics

Like Brain the dog's understanding of human behavior, the CEO analyzes corporate
culture and organizational psychology to predict email structures with scientific precision.
"""

import asyncio
import aiohttp
import re
import dns.resolver
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from urllib.parse import urljoin, urlparse
import json
import logging
import statistics

from ...ai.neural_engine import NeuralFoundationEngine
from .breach_timeline_engine import BreachTimelineEngine

logger = logging.getLogger(__name__)


@dataclass
class CorporateDNA:
    """Complete corporate email culture analysis"""
    domain: str
    analysis_date: datetime

    # Naming conventions analysis
    naming_conventions: Dict[str, float] = field(default_factory=dict)
    separator_preferences: Dict[str, float] = field(default_factory=dict)
    name_order_patterns: Dict[str, float] = field(default_factory=dict)

    # Organizational structure
    hierarchical_structure: Dict[str, Any] = field(default_factory=dict)
    department_patterns: Dict[str, List[str]] = field(default_factory=dict)
    seniority_indicators: List[str] = field(default_factory=list)

    # Cultural indicators
    formality_level: float = 0.5
    international_presence: bool = False
    tech_sophistication: float = 0.5
    security_awareness: float = 0.5

    # Technical preferences
    email_providers: List[str] = field(default_factory=list)
    subdomain_usage: Dict[str, int] = field(default_factory=dict)
    mx_record_patterns: List[str] = field(default_factory=list)

    # Confidence metrics
    confidence_score: float = 0.0
    sample_size: int = 0


@dataclass
class EmailPrediction:
    """Single email address prediction with confidence"""
    email_address: str
    confidence_score: float
    prediction_method: str
    supporting_evidence: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    validation_status: str = "unverified"  # unverified, valid, invalid, risky


@dataclass
class EmployeeProfile:
    """Employee profile for email prediction"""
    full_name: str
    first_name: str
    last_name: str
    title: Optional[str] = None
    department: Optional[str] = None
    seniority_level: Optional[str] = None
    linkedin_url: Optional[str] = None
    additional_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmailInvestigationResult:
    """Complete email investigation result"""
    target_domain: str
    start_time: datetime
    end_time: Optional[datetime] = None

    corporate_dna: Optional[CorporateDNA] = None
    discovered_emails: List[str] = field(default_factory=list)
    predicted_emails: List[EmailPrediction] = field(default_factory=list)
    employees_found: List[EmployeeProfile] = field(default_factory=list)

    breach_timeline: Dict[str, Any] = field(default_factory=dict)
    security_assessment: Dict[str, Any] = field(default_factory=dict)

    ai_insights: Dict[str, Any] = field(default_factory=dict)
    confidence_metrics: Dict[str, float] = field(default_factory=dict)
    investigation_notes: List[str] = field(default_factory=list)


class CorporateEmailOracle:
    """
    Revolutionary Corporate Email Oracle for Inspector-G

    Combines corporate psychology, organizational behavior analysis, and AI prediction
    to generate highly accurate email addresses with confidence scoring.

    Like Brain the dog's understanding of human patterns, CEO sees through
    corporate email structures that others miss.
    """

    def __init__(self, neural_engine: Optional[NeuralFoundationEngine] = None):
        self.neural_engine = neural_engine or NeuralFoundationEngine()
        self.breach_engine = BreachTimelineEngine()

        # Configuration
        self.max_concurrent_requests = 5
        self.request_delay = 2.0
        self.confidence_threshold = 0.7

        # Corporate email patterns database
        self.common_patterns = [
            "{first}.{last}",
            "{first}{last}",
            "{f}{last}",
            "{first}.{l}",
            "{first}_{last}",
            "{first}-{last}",
            "{last}.{first}",
            "{last}{first}",
            "{last}.{f}",
            "{f}.{last}",
            "{first}",
            "{last}"
        ]

        # Department-specific patterns
        self.department_patterns = {
            'it': ['it.', 'tech.', 'dev.', 'sysadmin.'],
            'sales': ['sales.', 'business.', 'bd.'],
            'marketing': ['marketing.', 'promo.', 'social.'],
            'hr': ['hr.', 'people.', 'talent.'],
            'finance': ['finance.', 'accounting.', 'billing.'],
            'support': ['support.', 'help.', 'service.'],
            'legal': ['legal.', 'compliance.', 'contracts.']
        }

        # Seniority indicators
        self.seniority_indicators = {
            'executive': ['ceo', 'cto', 'cfo', 'coo', 'president', 'founder'],
            'senior': ['senior', 'principal', 'lead', 'head', 'director', 'vp'],
            'mid': ['manager', 'coordinator', 'specialist'],
            'junior': ['junior', 'associate', 'assistant', 'intern']
        }

    async def investigate_domain_emails(
        self,
        target_domain: str,
        employee_list: Optional[List[EmployeeProfile]] = None,
        enable_breach_analysis: bool = True,
        enable_prediction: bool = True,
        enable_validation: bool = False
    ) -> EmailInvestigationResult:
        """
        Conduct comprehensive email investigation for domain

        Args:
            target_domain: Target domain to investigate
            employee_list: Known employees for email prediction
            enable_breach_analysis: Enable breach timeline analysis
            enable_prediction: Enable predictive email generation
            enable_validation: Enable email validation (careful - can be detected)

        Returns:
            Complete email investigation results
        """
        logger.info(f"🏢 Go-Go-Gadget Corporate Email Investigation: {target_domain}")

        investigation = EmailInvestigationResult(
            target_domain=target_domain,
            start_time=datetime.now()
        )

        try:
            # Phase 1: Corporate DNA Analysis
            logger.info("🧬 Phase 1: Corporate DNA Analysis")
            corporate_dna = await self._analyze_corporate_dna(target_domain)
            investigation.corporate_dna = corporate_dna
            investigation.investigation_notes.append(f"Corporate DNA analyzed with {corporate_dna.confidence_score:.1%} confidence")

            # Phase 2: Email Discovery
            logger.info("📧 Phase 2: Email Discovery")
            discovered_emails = await self._discover_existing_emails(target_domain)
            investigation.discovered_emails = discovered_emails
            investigation.investigation_notes.append(f"Discovered {len(discovered_emails)} existing emails")

            # Phase 3: Employee Intelligence
            logger.info("👥 Phase 3: Employee Intelligence Gathering")
            if not employee_list:
                employee_list = await self._discover_employees(target_domain)
            investigation.employees_found = employee_list
            investigation.investigation_notes.append(f"Found {len(employee_list)} employees")

            # Phase 4: Predictive Email Generation
            if enable_prediction and employee_list:
                logger.info("🔮 Phase 4: Predictive Email Generation")
                predicted_emails = await self._predict_employee_emails(
                    target_domain, employee_list, corporate_dna
                )
                investigation.predicted_emails = predicted_emails
                investigation.investigation_notes.append(f"Generated {len(predicted_emails)} email predictions")

            # Phase 5: Breach Timeline Analysis
            if enable_breach_analysis:
                logger.info("🕰️ Phase 5: Breach Timeline Analysis")
                breach_timeline = await self._analyze_breach_timeline(target_domain, investigation)
                investigation.breach_timeline = breach_timeline

            # Phase 6: Security Assessment
            logger.info("🛡️ Phase 6: Security Assessment")
            security_assessment = await self._assess_email_security(target_domain, investigation)
            investigation.security_assessment = security_assessment

            # Phase 7: AI-Enhanced Analysis
            logger.info("🤖 Phase 7: AI-Enhanced Analysis")
            ai_insights = await self._generate_ai_insights(investigation)
            investigation.ai_insights = ai_insights

            # Phase 8: Confidence Metrics
            logger.info("📊 Phase 8: Confidence Scoring")
            confidence_metrics = await self._calculate_confidence_metrics(investigation)
            investigation.confidence_metrics = confidence_metrics

            investigation.end_time = datetime.now()
            duration = (investigation.end_time - investigation.start_time).total_seconds()

            logger.info(f"✅ Corporate Email Investigation complete in {duration:.1f}s")
            logger.info(f"📈 Results: {len(investigation.discovered_emails)} discovered, {len(investigation.predicted_emails)} predicted")

            return investigation

        except Exception as e:
            logger.error(f"❌ Corporate email investigation failed: {e}")
            investigation.end_time = datetime.now()
            investigation.investigation_notes.append(f"Investigation failed: {str(e)}")
            raise

    async def _analyze_corporate_dna(self, domain: str) -> CorporateDNA:
        """Analyze corporate culture and email patterns"""
        logger.info(f"🧬 Analyzing corporate DNA for {domain}")

        corporate_dna = CorporateDNA(
            domain=domain,
            analysis_date=datetime.now()
        )

        try:
            # DNS and MX record analysis
            mx_records = await self._analyze_mx_records(domain)
            corporate_dna.mx_record_patterns = mx_records

            # Email provider detection
            email_providers = await self._detect_email_providers(mx_records)
            corporate_dna.email_providers = email_providers

            # Subdomain analysis
            subdomains = await self._discover_subdomains(domain)
            corporate_dna.subdomain_usage = subdomains

            # Web scraping for email patterns
            discovered_patterns = await self._scrape_email_patterns(domain)
            corporate_dna.naming_conventions = discovered_patterns.get('naming_conventions', {})
            corporate_dna.separator_preferences = discovered_patterns.get('separators', {})

            # Organizational structure inference
            org_structure = await self._infer_organizational_structure(domain)
            corporate_dna.hierarchical_structure = org_structure

            # Cultural analysis
            culture_analysis = await self._analyze_corporate_culture(domain)
            corporate_dna.formality_level = culture_analysis.get('formality', 0.5)
            corporate_dna.tech_sophistication = culture_analysis.get('tech_sophistication', 0.5)
            corporate_dna.international_presence = culture_analysis.get('international', False)

            # Calculate confidence score
            corporate_dna.confidence_score = await self._calculate_dna_confidence(corporate_dna)

            logger.info(f"✅ Corporate DNA analysis complete: {corporate_dna.confidence_score:.1%} confidence")
            return corporate_dna

        except Exception as e:
            logger.warning(f"Corporate DNA analysis error: {e}")
            return corporate_dna

    async def _analyze_mx_records(self, domain: str) -> List[str]:
        """Analyze MX records for email infrastructure"""
        try:
            mx_records = []
            answers = dns.resolver.resolve(domain, 'MX')
            for rdata in answers:
                mx_records.append(str(rdata.exchange).rstrip('.'))
            return mx_records
        except Exception as e:
            logger.warning(f"MX record analysis failed for {domain}: {e}")
            return []

    async def _detect_email_providers(self, mx_records: List[str]) -> List[str]:
        """Detect email service providers from MX records"""
        providers = []

        provider_patterns = {
            'google': ['google.com', 'gmail.com', 'googlemail.com'],
            'microsoft': ['outlook.com', 'hotmail.com', 'live.com', 'office365.com'],
            'proofpoint': ['pphosted.com'],
            'mimecast': ['mimecast.com'],
            'custom': []  # Will be detected if no known patterns
        }

        for mx_record in mx_records:
            mx_lower = mx_record.lower()
            provider_found = False

            for provider, patterns in provider_patterns.items():
                if provider == 'custom':
                    continue
                if any(pattern in mx_lower for pattern in patterns):
                    providers.append(provider)
                    provider_found = True
                    break

            if not provider_found:
                providers.append('custom')

        return list(set(providers))

    async def _discover_subdomains(self, domain: str) -> Dict[str, int]:
        """Discover subdomains that might host email-related services"""
        subdomains = defaultdict(int)

        # Common email-related subdomains
        common_subdomains = [
            'mail', 'email', 'smtp', 'imap', 'pop', 'webmail',
            'mx', 'exchange', 'outlook', 'office365'
        ]

        for subdomain in common_subdomains:
            full_domain = f"{subdomain}.{domain}"
            try:
                # Simple DNS lookup
                dns.resolver.resolve(full_domain, 'A')
                subdomains[subdomain] += 1
            except:
                pass

        return dict(subdomains)

    async def _scrape_email_patterns(self, domain: str) -> Dict[str, Any]:
        """Scrape public sources for email patterns"""
        patterns = {
            'naming_conventions': {},
            'separators': {},
            'samples': []
        }

        try:
            # Search for emails on the company website
            website_emails = await self._scrape_website_emails(domain)
            patterns['samples'].extend(website_emails)

            # Analyze patterns from samples
            if website_emails:
                naming_analysis = self._analyze_naming_patterns(website_emails, domain)
                patterns['naming_conventions'] = naming_analysis['conventions']
                patterns['separators'] = naming_analysis['separators']

        except Exception as e:
            logger.warning(f"Email pattern scraping failed: {e}")

        return patterns

    async def _scrape_website_emails(self, domain: str) -> List[str]:
        """Scrape emails from company website"""
        emails = []

        try:
            urls_to_check = [
                f"https://{domain}",
                f"https://{domain}/about",
                f"https://{domain}/contact",
                f"https://{domain}/team",
                f"https://{domain}/staff"
            ]

            email_pattern = re.compile(
                r'\b[A-Za-z0-9._%+-]+@' + re.escape(domain) + r'\b',
                re.IGNORECASE
            )

            async with aiohttp.ClientSession() as session:
                for url in urls_to_check:
                    try:
                        await asyncio.sleep(self.request_delay)
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (compatible; Inspector-G/1.0; +https://inspectorbrain.ai/bot)'
                        }

                        async with session.get(url, headers=headers, timeout=10) as response:
                            if response.status == 200:
                                content = await response.text()
                                found_emails = email_pattern.findall(content)
                                emails.extend(found_emails)
                    except:
                        continue

            # Remove duplicates and clean
            emails = list(set([email.lower() for email in emails]))

        except Exception as e:
            logger.warning(f"Website email scraping failed: {e}")

        return emails

    def _analyze_naming_patterns(self, emails: List[str], domain: str) -> Dict[str, Any]:
        """Analyze naming patterns from email samples"""
        conventions = defaultdict(int)
        separators = defaultdict(int)

        for email in emails:
            username = email.split('@')[0]

            # Analyze separators
            if '.' in username:
                separators['.'] += 1
            if '_' in username:
                separators['_'] += 1
            if '-' in username:
                separators['-'] += 1
            if username.isalnum():
                separators['none'] += 1

            # Analyze patterns (simplified)
            parts = re.split(r'[._-]', username)
            if len(parts) == 2:
                conventions['firstname.lastname'] += 1
            elif len(parts) == 1:
                if len(username) > 6:
                    conventions['firstlast'] += 1
                else:
                    conventions['firstname'] += 1

        # Convert to ratios
        total_emails = len(emails)
        conventions = {k: v/total_emails for k, v in conventions.items()}
        separators = {k: v/total_emails for k, v in separators.items()}

        return {
            'conventions': conventions,
            'separators': separators
        }

    async def _infer_organizational_structure(self, domain: str) -> Dict[str, Any]:
        """Infer organizational structure from public data"""
        structure = {
            'departments': [],
            'hierarchy_levels': [],
            'size_estimate': 'unknown',
            'industry': 'unknown'
        }

        try:
            # LinkedIn company search (would need API access for full implementation)
            # For now, we'll use simple heuristics

            # Analyze company size from domain authority and web presence
            size_indicators = await self._estimate_company_size(domain)
            structure['size_estimate'] = size_indicators

            # Try to identify industry from domain content
            industry = await self._identify_industry(domain)
            structure['industry'] = industry

        except Exception as e:
            logger.warning(f"Organizational structure inference failed: {e}")

        return structure

    async def _estimate_company_size(self, domain: str) -> str:
        """Estimate company size from various indicators"""
        # Simplified size estimation
        # Real implementation would use domain authority, employee counts, etc.
        return "medium"  # Placeholder

    async def _identify_industry(self, domain: str) -> str:
        """Identify industry from website content"""
        # Simplified industry detection
        # Real implementation would analyze website content, keywords, etc.
        return "technology"  # Placeholder

    async def _analyze_corporate_culture(self, domain: str) -> Dict[str, Any]:
        """Analyze corporate culture indicators"""
        culture = {
            'formality': 0.5,
            'tech_sophistication': 0.5,
            'international': False,
            'startup_vs_enterprise': 'enterprise'
        }

        try:
            # Analyze website language, design, content for culture indicators
            # This would be a complex ML task in practice
            pass

        except Exception as e:
            logger.warning(f"Corporate culture analysis failed: {e}")

        return culture

    async def _calculate_dna_confidence(self, corporate_dna: CorporateDNA) -> float:
        """Calculate confidence score for corporate DNA analysis"""
        factors = []

        # MX records availability
        if corporate_dna.mx_record_patterns:
            factors.append(0.8)

        # Email samples found
        if corporate_dna.naming_conventions:
            factors.append(0.9)

        # Provider identification
        if corporate_dna.email_providers:
            factors.append(0.7)

        # Subdomain discovery
        if corporate_dna.subdomain_usage:
            factors.append(0.6)

        return statistics.mean(factors) if factors else 0.1

    async def _discover_existing_emails(self, domain: str) -> List[str]:
        """Discover existing emails through various sources"""
        emails = []

        try:
            # Website scraping
            website_emails = await self._scrape_website_emails(domain)
            emails.extend(website_emails)

            # Search engines (simplified)
            search_emails = await self._search_engine_email_discovery(domain)
            emails.extend(search_emails)

            # Remove duplicates
            emails = list(set([email.lower() for email in emails]))

        except Exception as e:
            logger.warning(f"Email discovery failed: {e}")

        return emails

    async def _search_engine_email_discovery(self, domain: str) -> List[str]:
        """Use search engines to find emails (simplified implementation)"""
        # This would use search APIs or web scraping in practice
        # For now, return empty list as placeholder
        return []

    async def _discover_employees(self, domain: str) -> List[EmployeeProfile]:
        """Discover employees through various sources"""
        employees = []

        try:
            # LinkedIn discovery (would need API access)
            linkedin_employees = await self._discover_linkedin_employees(domain)
            employees.extend(linkedin_employees)

            # Website team pages
            website_employees = await self._scrape_team_pages(domain)
            employees.extend(website_employees)

        except Exception as e:
            logger.warning(f"Employee discovery failed: {e}")

        return employees

    async def _discover_linkedin_employees(self, domain: str) -> List[EmployeeProfile]:
        """Discover employees from LinkedIn (placeholder)"""
        # Would need LinkedIn API access for real implementation
        return []

    async def _scrape_team_pages(self, domain: str) -> List[EmployeeProfile]:
        """Scrape team/about pages for employee information"""
        employees = []

        try:
            team_urls = [
                f"https://{domain}/team",
                f"https://{domain}/about/team",
                f"https://{domain}/staff",
                f"https://{domain}/leadership"
            ]

            name_patterns = [
                r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b',  # First Last
                r'\b([A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+)\b',  # First M. Last
            ]

            async with aiohttp.ClientSession() as session:
                for url in team_urls:
                    try:
                        await asyncio.sleep(self.request_delay)
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (compatible; Inspector-G/1.0)'
                        }

                        async with session.get(url, headers=headers, timeout=10) as response:
                            if response.status == 200:
                                content = await response.text()

                                for pattern in name_patterns:
                                    matches = re.findall(pattern, content)
                                    for match in matches:
                                        parts = match.split()
                                        if len(parts) >= 2:
                                            employee = EmployeeProfile(
                                                full_name=match,
                                                first_name=parts[0],
                                                last_name=parts[-1]
                                            )
                                            employees.append(employee)
                    except:
                        continue

            # Remove duplicates
            seen_names = set()
            unique_employees = []
            for emp in employees:
                if emp.full_name not in seen_names:
                    seen_names.add(emp.full_name)
                    unique_employees.append(emp)

            employees = unique_employees

        except Exception as e:
            logger.warning(f"Team page scraping failed: {e}")

        return employees

    async def _predict_employee_emails(
        self,
        domain: str,
        employees: List[EmployeeProfile],
        corporate_dna: CorporateDNA
    ) -> List[EmailPrediction]:
        """Predict employee email addresses using corporate DNA"""
        predictions = []

        for employee in employees:
            employee_predictions = await self._predict_single_employee_email(
                employee, domain, corporate_dna
            )
            predictions.extend(employee_predictions)

        # Sort by confidence
        predictions.sort(key=lambda x: x.confidence_score, reverse=True)

        return predictions

    async def _predict_single_employee_email(
        self,
        employee: EmployeeProfile,
        domain: str,
        corporate_dna: CorporateDNA
    ) -> List[EmailPrediction]:
        """Predict email addresses for a single employee"""
        predictions = []

        first = employee.first_name.lower()
        last = employee.last_name.lower()
        f = first[0] if first else ''
        l = last[0] if last else ''

        # Generate patterns based on corporate DNA
        patterns_to_try = self._get_prioritized_patterns(corporate_dna)

        for pattern in patterns_to_try:
            try:
                email = pattern.format(
                    first=first, last=last, f=f, l=l
                ) + f"@{domain}"

                # Calculate confidence based on corporate DNA
                confidence = self._calculate_email_confidence(
                    pattern, corporate_dna, employee
                )

                # Generate supporting evidence
                evidence = self._generate_email_evidence(
                    pattern, corporate_dna, employee
                )

                prediction = EmailPrediction(
                    email_address=email,
                    confidence_score=confidence,
                    prediction_method=f"corporate_dna_{pattern}",
                    supporting_evidence=evidence
                )

                predictions.append(prediction)

            except Exception as e:
                logger.warning(f"Email prediction failed for pattern {pattern}: {e}")

        return predictions

    def _get_prioritized_patterns(self, corporate_dna: CorporateDNA) -> List[str]:
        """Get email patterns prioritized by corporate DNA analysis"""
        patterns = self.common_patterns.copy()

        # Prioritize based on detected patterns
        if corporate_dna.naming_conventions:
            # Sort patterns by their likelihood based on corporate DNA
            pattern_scores = {}
            for pattern in patterns:
                score = 0.5  # Base score

                # Boost score based on detected conventions
                if 'firstname.lastname' in corporate_dna.naming_conventions and '{first}.{last}' == pattern:
                    score += corporate_dna.naming_conventions['firstname.lastname']
                elif 'firstlast' in corporate_dna.naming_conventions and '{first}{last}' == pattern:
                    score += corporate_dna.naming_conventions['firstlast']

                # Boost based on separator preferences
                if '.' in pattern and corporate_dna.separator_preferences.get('.', 0) > 0.5:
                    score += 0.2
                elif '_' in pattern and corporate_dna.separator_preferences.get('_', 0) > 0.5:
                    score += 0.2

                pattern_scores[pattern] = score

            # Sort by score
            patterns = sorted(patterns, key=lambda p: pattern_scores.get(p, 0.5), reverse=True)

        return patterns

    def _calculate_email_confidence(
        self,
        pattern: str,
        corporate_dna: CorporateDNA,
        employee: EmployeeProfile
    ) -> float:
        """Calculate confidence score for email prediction"""
        base_confidence = 0.5

        # Boost based on corporate DNA match
        if corporate_dna.naming_conventions:
            if '{first}.{last}' == pattern and 'firstname.lastname' in corporate_dna.naming_conventions:
                base_confidence += corporate_dna.naming_conventions['firstname.lastname'] * 0.3

        # Boost based on separator preferences
        if '.' in pattern and corporate_dna.separator_preferences.get('.', 0) > 0.5:
            base_confidence += 0.1
        elif '_' in pattern and corporate_dna.separator_preferences.get('_', 0) > 0.5:
            base_confidence += 0.1

        # Boost based on corporate DNA confidence
        base_confidence += corporate_dna.confidence_score * 0.2

        # Boost based on employee seniority (executives more likely to have predictable emails)
        if employee.title and any(indicator in employee.title.lower()
                                for indicator in self.seniority_indicators['executive']):
            base_confidence += 0.1

        return min(base_confidence, 0.95)  # Cap at 95%

    def _generate_email_evidence(
        self,
        pattern: str,
        corporate_dna: CorporateDNA,
        employee: EmployeeProfile
    ) -> List[str]:
        """Generate supporting evidence for email prediction"""
        evidence = []

        if corporate_dna.naming_conventions:
            evidence.append(f"Corporate DNA shows preference for {pattern} pattern")

        if corporate_dna.confidence_score > 0.7:
            evidence.append(f"High corporate DNA confidence ({corporate_dna.confidence_score:.1%})")

        if employee.title:
            evidence.append(f"Employee title: {employee.title}")

        return evidence

    async def _analyze_breach_timeline(
        self,
        domain: str,
        investigation: EmailInvestigationResult
    ) -> Dict[str, Any]:
        """Analyze breach timeline for domain emails"""
        try:
            timeline = await self.breach_engine.analyze_domain_breaches(
                domain, investigation.discovered_emails
            )
            return timeline
        except Exception as e:
            logger.warning(f"Breach timeline analysis failed: {e}")
            return {}

    async def _assess_email_security(
        self,
        domain: str,
        investigation: EmailInvestigationResult
    ) -> Dict[str, Any]:
        """Assess email security posture"""
        assessment = {
            'email_security_score': 0.5,
            'risks': [],
            'recommendations': [],
            'dmarc_status': 'unknown',
            'spf_status': 'unknown'
        }

        try:
            # Check DMARC record
            try:
                dmarc_record = dns.resolver.resolve(f"_dmarc.{domain}", 'TXT')
                assessment['dmarc_status'] = 'configured'
                assessment['email_security_score'] += 0.2
            except:
                assessment['dmarc_status'] = 'not_configured'
                assessment['risks'].append('No DMARC record found')

            # Check SPF record
            try:
                spf_record = dns.resolver.resolve(domain, 'TXT')
                for record in spf_record:
                    if 'v=spf1' in str(record):
                        assessment['spf_status'] = 'configured'
                        assessment['email_security_score'] += 0.2
                        break
                else:
                    assessment['spf_status'] = 'not_configured'
                    assessment['risks'].append('No SPF record found')
            except:
                assessment['spf_status'] = 'not_configured'
                assessment['risks'].append('No SPF record found')

            # Generate recommendations
            if assessment['dmarc_status'] == 'not_configured':
                assessment['recommendations'].append('Implement DMARC policy')
            if assessment['spf_status'] == 'not_configured':
                assessment['recommendations'].append('Configure SPF record')

        except Exception as e:
            logger.warning(f"Email security assessment failed: {e}")

        return assessment

    async def _generate_ai_insights(self, investigation: EmailInvestigationResult) -> Dict[str, Any]:
        """Generate AI-powered insights about the email investigation"""
        try:
            analysis_data = {
                'domain': investigation.target_domain,
                'discovered_emails': len(investigation.discovered_emails),
                'predicted_emails': len(investigation.predicted_emails),
                'employees_found': len(investigation.employees_found),
                'corporate_dna_confidence': investigation.corporate_dna.confidence_score if investigation.corporate_dna else 0
            }

            # Use neural engine for analysis (would be implemented)
            ai_insights = {
                'summary': f"Email investigation reveals {'strong' if len(investigation.discovered_emails) > 5 else 'limited'} email presence",
                'key_findings': [
                    f"Discovered {len(investigation.discovered_emails)} existing emails",
                    f"Generated {len(investigation.predicted_emails)} high-confidence predictions"
                ],
                'recommendations': [
                    "Validate predicted emails carefully to avoid detection",
                    "Monitor for new employees to update email predictions"
                ],
                'risk_assessment': 'Medium',
                'confidence_analysis': {
                    'overall_confidence': statistics.mean([
                        pred.confidence_score for pred in investigation.predicted_emails
                    ]) if investigation.predicted_emails else 0
                }
            }

            return ai_insights

        except Exception as e:
            logger.warning(f"AI insights generation failed: {e}")
            return {
                'summary': 'AI analysis unavailable',
                'key_findings': [],
                'recommendations': [],
                'risk_assessment': 'Unknown'
            }

    async def _calculate_confidence_metrics(self, investigation: EmailInvestigationResult) -> Dict[str, float]:
        """Calculate comprehensive confidence metrics"""
        metrics = {}

        # Corporate DNA confidence
        if investigation.corporate_dna:
            metrics['corporate_dna_confidence'] = investigation.corporate_dna.confidence_score

        # Email prediction confidence
        if investigation.predicted_emails:
            confidences = [pred.confidence_score for pred in investigation.predicted_emails]
            metrics['average_prediction_confidence'] = statistics.mean(confidences)
            metrics['highest_prediction_confidence'] = max(confidences)
            metrics['prediction_count'] = len(investigation.predicted_emails)

        # Discovery success rate
        total_attempts = len(investigation.discovered_emails) + len(investigation.predicted_emails)
        if total_attempts > 0:
            metrics['discovery_success_rate'] = len(investigation.discovered_emails) / total_attempts

        # Employee intelligence coverage
        if investigation.employees_found:
            metrics['employee_coverage'] = len(investigation.employees_found) / max(len(investigation.employees_found), 10)

        return metrics