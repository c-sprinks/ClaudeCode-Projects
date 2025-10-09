#!/usr/bin/env python3
"""
M.A.D. Detection System - Threat Analysis & Security Monitoring

Like the M.A.D. agents in Inspector Gadget who were the antagonists trying to
cause chaos, this M.A.D. system ironically serves as our threat detection and
security monitoring system - protecting against the very chaos the original
M.A.D. agents would create.

M.A.D. Detection Capabilities:
- Automated threat detection and analysis
- Security vulnerability assessment
- Anomaly detection in OSINT data
- Malicious pattern recognition
- Risk assessment and scoring
- Real-time monitoring and alerts
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json
import re
import hashlib
import ipaddress
from pathlib import Path

logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    """Threat severity levels"""
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatCategory(Enum):
    """Categories of threats detected"""
    MALWARE = "malware"
    PHISHING = "phishing"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_BREACH = "data_breach"
    RECONNAISSANCE = "reconnaissance"
    SOCIAL_ENGINEERING = "social_engineering"
    INFRASTRUCTURE = "infrastructure"
    CREDENTIAL_EXPOSURE = "credential_exposure"
    UNKNOWN = "unknown"


class RiskFactor(Enum):
    """Risk assessment factors"""
    EXPOSURE_LEVEL = "exposure_level"
    DATA_SENSITIVITY = "data_sensitivity"
    THREAT_ACTOR_CAPABILITY = "threat_actor_capability"
    ATTACK_SURFACE = "attack_surface"
    DEFENSIVE_POSTURE = "defensive_posture"


@dataclass
class ThreatIndicator:
    """Individual threat indicator"""
    indicator_id: str
    indicator_type: str          # ip, domain, email, hash, url, pattern
    indicator_value: str
    threat_level: ThreatLevel
    threat_category: ThreatCategory
    confidence: float            # 0.0 - 1.0
    description: str
    source: str                  # Where this indicator was discovered
    first_seen: datetime
    last_seen: datetime
    metadata: Dict[str, Any]


@dataclass
class SecurityAlert:
    """Security threat alert"""
    alert_id: str
    title: str
    description: str
    threat_level: ThreatLevel
    threat_category: ThreatCategory
    indicators: List[ThreatIndicator]
    affected_targets: List[str]
    risk_score: float            # 0.0 - 10.0
    created_at: datetime
    status: str                  # open, investigating, resolved, false_positive
    recommendations: List[str]
    technical_details: Dict[str, Any]


@dataclass
class RiskAssessment:
    """Comprehensive risk assessment"""
    assessment_id: str
    target: str
    overall_risk_score: float    # 0.0 - 10.0
    risk_factors: Dict[RiskFactor, float]
    threat_indicators: List[ThreatIndicator]
    vulnerabilities: List[str]
    recommendations: List[str]
    assessment_date: datetime
    next_assessment_due: datetime


class MADDetection:
    """
    M.A.D. Detection System - Advanced Threat Analysis

    Provides automated threat detection, security monitoring, and risk assessment
    capabilities for OSINT operations. Ironically named after the M.A.D. agents
    from Inspector Gadget, this system protects against the chaos they would create.
    """

    def __init__(self):
        self.personality_traits = {
            "vigilant": True,
            "analytical": True,
            "proactive": True,
            "systematic": True,
            "security_focused": True
        }

        # Set up persistent storage
        self.data_dir = Path.home() / ".inspector-g" / "mad_detection"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.alerts_file = self.data_dir / "security_alerts.json"
        self.indicators_file = self.data_dir / "threat_indicators.json"
        self.assessments_file = self.data_dir / "risk_assessments.json"

        # Load existing data
        self.security_alerts = self._load_alerts()
        self.threat_indicators = self._load_indicators()
        self.risk_assessments = self._load_assessments()

        # Initialize threat detection patterns
        self.threat_patterns = self._initialize_threat_patterns()
        self.suspicious_patterns = self._initialize_suspicious_patterns()

        logger.info("🦹‍♂️ M.A.D. Detection System initialized - Threat monitoring active!")

    def greet_agent(self, agent_name: str = "Inspector") -> str:
        """M.A.D. Detection System greeting"""
        greetings = [
            f"🚨 M.A.D. Detection System online, {agent_name}. Monitoring for threats...",
            f"🔍 Agent {agent_name}, I've detected unusual activity. Initiating analysis protocols.",
            f"⚠️ {agent_name}, the M.A.D. Detection System has identified potential security risks.",
            f"🛡️ Security monitoring active, {agent_name}. All systems nominal - for now.",
            f"🦹‍♂️ {agent_name}, this is M.A.D. Detection. I'm seeing patterns that require investigation."
        ]
        import random
        return random.choice(greetings)

    def analyze_target(self, target: str, osint_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive threat analysis of a target using OSINT data
        """
        logger.info(f"🔍 Analyzing target '{target}' for security threats...")

        analysis_results = {
            "target": target,
            "analysis_timestamp": datetime.now().isoformat(),
            "threat_indicators": [],
            "security_alerts": [],
            "risk_assessment": None,
            "recommendations": [],
            "overall_threat_level": ThreatLevel.INFORMATIONAL
        }

        # Detect threat indicators
        indicators = self._detect_threat_indicators(target, osint_data)
        analysis_results["threat_indicators"] = [self._indicator_to_dict(ind) for ind in indicators]

        # Generate security alerts if needed
        alerts = self._generate_security_alerts(target, indicators, osint_data)
        analysis_results["security_alerts"] = [self._alert_to_dict(alert) for alert in alerts]

        # Perform risk assessment
        risk_assessment = self._perform_risk_assessment(target, indicators, osint_data)
        analysis_results["risk_assessment"] = self._assessment_to_dict(risk_assessment)

        # Generate recommendations
        recommendations = self._generate_security_recommendations(target, indicators, risk_assessment)
        analysis_results["recommendations"] = recommendations

        # Determine overall threat level
        overall_level = self._calculate_overall_threat_level(indicators, alerts)
        analysis_results["overall_threat_level"] = overall_level.value

        # Store new indicators and alerts
        self.threat_indicators.extend(indicators)
        self.security_alerts.extend(alerts)
        self.risk_assessments.append(risk_assessment)

        # Persist to storage
        self._save_indicators()
        self._save_alerts()
        self._save_assessments()

        logger.info(f"✅ Threat analysis complete for '{target}' - Level: {overall_level.value}")
        return analysis_results

    def _detect_threat_indicators(self, target: str, osint_data: Dict[str, Any]) -> List[ThreatIndicator]:
        """Detect potential threat indicators in OSINT data"""
        indicators = []
        now = datetime.now()

        # Check for suspicious domains
        if "domains" in osint_data:
            for domain in osint_data["domains"]:
                threat_info = self._analyze_domain_threat(domain)
                if threat_info:
                    indicator = ThreatIndicator(
                        indicator_id=f"DOM-{hashlib.md5(domain.encode()).hexdigest()[:8].upper()}",
                        indicator_type="domain",
                        indicator_value=domain,
                        threat_level=threat_info["level"],
                        threat_category=threat_info["category"],
                        confidence=threat_info["confidence"],
                        description=threat_info["description"],
                        source=f"OSINT analysis of {target}",
                        first_seen=now,
                        last_seen=now,
                        metadata=threat_info.get("metadata", {})
                    )
                    indicators.append(indicator)

        # Check for suspicious email patterns
        if "emails" in osint_data:
            for email in osint_data["emails"]:
                threat_info = self._analyze_email_threat(email)
                if threat_info:
                    indicator = ThreatIndicator(
                        indicator_id=f"EML-{hashlib.md5(email.encode()).hexdigest()[:8].upper()}",
                        indicator_type="email",
                        indicator_value=email,
                        threat_level=threat_info["level"],
                        threat_category=threat_info["category"],
                        confidence=threat_info["confidence"],
                        description=threat_info["description"],
                        source=f"OSINT analysis of {target}",
                        first_seen=now,
                        last_seen=now,
                        metadata=threat_info.get("metadata", {})
                    )
                    indicators.append(indicator)

        # Check for suspicious username patterns
        if "usernames" in osint_data:
            for username in osint_data["usernames"]:
                threat_info = self._analyze_username_threat(username)
                if threat_info:
                    indicator = ThreatIndicator(
                        indicator_id=f"USR-{hashlib.md5(username.encode()).hexdigest()[:8].upper()}",
                        indicator_type="username",
                        indicator_value=username,
                        threat_level=threat_info["level"],
                        threat_category=threat_info["category"],
                        confidence=threat_info["confidence"],
                        description=threat_info["description"],
                        source=f"OSINT analysis of {target}",
                        first_seen=now,
                        last_seen=now,
                        metadata=threat_info.get("metadata", {})
                    )
                    indicators.append(indicator)

        return indicators

    def _analyze_domain_threat(self, domain: str) -> Optional[Dict[str, Any]]:
        """Analyze domain for threat indicators"""
        threats = []

        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.bit', '.onion']
        for tld in suspicious_tlds:
            if domain.endswith(tld):
                threats.append({
                    "level": ThreatLevel.MEDIUM,
                    "category": ThreatCategory.SUSPICIOUS_ACTIVITY,
                    "confidence": 0.6,
                    "description": f"Domain uses suspicious TLD: {tld}",
                    "metadata": {"suspicious_tld": tld}
                })

        # Check for domain generation algorithm patterns
        if self._is_dga_domain(domain):
            threats.append({
                "level": ThreatLevel.HIGH,
                "category": ThreatCategory.MALWARE,
                "confidence": 0.8,
                "description": "Domain matches DGA (Domain Generation Algorithm) pattern",
                "metadata": {"dga_indicators": self._get_dga_indicators(domain)}
            })

        # Check for typosquatting patterns
        if self._is_typosquatting(domain):
            threats.append({
                "level": ThreatLevel.MEDIUM,
                "category": ThreatCategory.PHISHING,
                "confidence": 0.7,
                "description": "Domain appears to be typosquatting legitimate brands",
                "metadata": {"typosquatting_target": self._get_typosquatting_target(domain)}
            })

        # Return highest priority threat
        if threats:
            return max(threats, key=lambda x: (x["level"].value, x["confidence"]))
        return None

    def _analyze_email_threat(self, email: str) -> Optional[Dict[str, Any]]:
        """Analyze email for threat indicators"""
        threats = []

        # Check for suspicious email patterns
        suspicious_patterns = [
            r'noreply\d+@',  # Numbered noreply addresses
            r'admin\d+@',    # Numbered admin addresses
            r'[0-9]{6,}@',   # Long numeric prefixes
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, email, re.IGNORECASE):
                threats.append({
                    "level": ThreatLevel.LOW,
                    "category": ThreatCategory.SUSPICIOUS_ACTIVITY,
                    "confidence": 0.4,
                    "description": f"Email matches suspicious pattern: {pattern}",
                    "metadata": {"pattern_matched": pattern}
                })

        # Check for known phishing email domains
        domain = email.split('@')[-1] if '@' in email else ''
        if domain in self.threat_patterns.get('phishing_domains', []):
            threats.append({
                "level": ThreatLevel.HIGH,
                "category": ThreatCategory.PHISHING,
                "confidence": 0.9,
                "description": f"Email domain is known phishing domain: {domain}",
                "metadata": {"known_phishing_domain": domain}
            })

        if threats:
            return max(threats, key=lambda x: (x["level"].value, x["confidence"]))
        return None

    def _analyze_username_threat(self, username: str) -> Optional[Dict[str, Any]]:
        """Analyze username for threat indicators"""
        threats = []

        # Check for suspicious username patterns
        suspicious_patterns = [
            r'admin\d{3,}',     # admin followed by many digits
            r'hacker\w*',       # variations of "hacker"
            r'exploit\w*',      # variations of "exploit"
            r'\w*bot\w*',       # bot-related usernames
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, username, re.IGNORECASE):
                threats.append({
                    "level": ThreatLevel.MEDIUM,
                    "category": ThreatCategory.SUSPICIOUS_ACTIVITY,
                    "confidence": 0.5,
                    "description": f"Username matches suspicious pattern: {pattern}",
                    "metadata": {"pattern_matched": pattern}
                })

        if threats:
            return max(threats, key=lambda x: (x["level"].value, x["confidence"]))
        return None

    def _is_dga_domain(self, domain: str) -> bool:
        """Check if domain matches DGA patterns"""
        # Simple DGA detection heuristics
        base_domain = domain.split('.')[0]

        # Check for random-looking strings
        consonant_clusters = len(re.findall(r'[bcdfghjklmnpqrstvwxz]{3,}', base_domain.lower()))
        vowel_ratio = len(re.findall(r'[aeiou]', base_domain.lower())) / len(base_domain)

        return consonant_clusters >= 2 or vowel_ratio < 0.2

    def _get_dga_indicators(self, domain: str) -> Dict[str, Any]:
        """Get DGA indicators for a domain"""
        base_domain = domain.split('.')[0]
        return {
            "consonant_clusters": len(re.findall(r'[bcdfghjklmnpqrstvwxz]{3,}', base_domain.lower())),
            "vowel_ratio": len(re.findall(r'[aeiou]', base_domain.lower())) / len(base_domain),
            "entropy": self._calculate_entropy(base_domain)
        }

    def _calculate_entropy(self, string: str) -> float:
        """Calculate Shannon entropy of a string"""
        from collections import Counter
        import math

        counter = Counter(string.lower())
        length = len(string)
        entropy = 0

        for count in counter.values():
            p = count / length
            entropy -= p * math.log2(p)

        return entropy

    def _is_typosquatting(self, domain: str) -> bool:
        """Check if domain is typosquatting"""
        # Common legitimate domains to check against
        legitimate_domains = [
            'google', 'microsoft', 'amazon', 'facebook', 'twitter',
            'paypal', 'apple', 'netflix', 'ebay', 'linkedin'
        ]

        base_domain = domain.split('.')[0].lower()

        for legit in legitimate_domains:
            if self._is_similar_domain(base_domain, legit):
                return True
        return False

    def _is_similar_domain(self, domain1: str, domain2: str) -> bool:
        """Check if two domains are suspiciously similar"""
        from difflib import SequenceMatcher

        # Calculate similarity ratio
        similarity = SequenceMatcher(None, domain1, domain2).ratio()

        # Consider it similar if > 70% match but not exact
        return 0.7 < similarity < 1.0

    def _get_typosquatting_target(self, domain: str) -> str:
        """Get the likely typosquatting target"""
        legitimate_domains = [
            'google', 'microsoft', 'amazon', 'facebook', 'twitter',
            'paypal', 'apple', 'netflix', 'ebay', 'linkedin'
        ]

        base_domain = domain.split('.')[0].lower()
        best_match = ""
        best_similarity = 0

        for legit in legitimate_domains:
            from difflib import SequenceMatcher
            similarity = SequenceMatcher(None, base_domain, legit).ratio()
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = legit

        return best_match

    def _generate_security_alerts(self, target: str, indicators: List[ThreatIndicator], osint_data: Dict[str, Any]) -> List[SecurityAlert]:
        """Generate security alerts based on threat indicators"""
        alerts = []
        now = datetime.now()

        # Group indicators by threat level and category
        high_threat_indicators = [ind for ind in indicators if ind.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]]

        if high_threat_indicators:
            alert = SecurityAlert(
                alert_id=f"ALERT-{hashlib.md5(f'{target}-{now}'.encode()).hexdigest()[:8].upper()}",
                title=f"High-Risk Security Indicators Detected: {target}",
                description=f"Multiple high-threat indicators discovered during OSINT analysis of {target}",
                threat_level=max(ind.threat_level for ind in high_threat_indicators),
                threat_category=self._determine_primary_category(high_threat_indicators),
                indicators=high_threat_indicators,
                affected_targets=[target],
                risk_score=self._calculate_alert_risk_score(high_threat_indicators),
                created_at=now,
                status="open",
                recommendations=self._generate_alert_recommendations(high_threat_indicators),
                technical_details={
                    "analysis_method": "automated_osint_analysis",
                    "indicator_count": len(high_threat_indicators),
                    "confidence_scores": [ind.confidence for ind in high_threat_indicators]
                }
            )
            alerts.append(alert)

        return alerts

    def _determine_primary_category(self, indicators: List[ThreatIndicator]) -> ThreatCategory:
        """Determine the primary threat category from multiple indicators"""
        category_counts = {}
        for indicator in indicators:
            category_counts[indicator.threat_category] = category_counts.get(indicator.threat_category, 0) + 1

        return max(category_counts.keys(), key=lambda x: category_counts[x])

    def _calculate_alert_risk_score(self, indicators: List[ThreatIndicator]) -> float:
        """Calculate risk score for an alert"""
        if not indicators:
            return 0.0

        # Weight by threat level and confidence
        score = 0.0
        level_weights = {
            ThreatLevel.INFORMATIONAL: 1.0,
            ThreatLevel.LOW: 2.0,
            ThreatLevel.MEDIUM: 4.0,
            ThreatLevel.HIGH: 7.0,
            ThreatLevel.CRITICAL: 10.0
        }

        for indicator in indicators:
            weight = level_weights.get(indicator.threat_level, 1.0)
            score += weight * indicator.confidence

        return min(10.0, score / len(indicators))

    def _generate_alert_recommendations(self, indicators: List[ThreatIndicator]) -> List[str]:
        """Generate recommendations for security alerts"""
        recommendations = [
            "Conduct immediate verification of all threat indicators",
            "Monitor target for additional suspicious activity",
            "Consider implementing additional security controls",
            "Document all findings for threat intelligence purposes"
        ]

        # Add specific recommendations based on threat categories
        categories = set(ind.threat_category for ind in indicators)

        if ThreatCategory.PHISHING in categories:
            recommendations.append("Implement email security controls and user awareness training")

        if ThreatCategory.MALWARE in categories:
            recommendations.append("Deploy advanced endpoint detection and response capabilities")

        if ThreatCategory.SUSPICIOUS_ACTIVITY in categories:
            recommendations.append("Enhance monitoring and logging for the affected systems")

        return recommendations

    def _perform_risk_assessment(self, target: str, indicators: List[ThreatIndicator], osint_data: Dict[str, Any]) -> RiskAssessment:
        """Perform comprehensive risk assessment"""
        now = datetime.now()

        # Calculate risk factors
        risk_factors = {
            RiskFactor.EXPOSURE_LEVEL: self._calculate_exposure_level(osint_data),
            RiskFactor.DATA_SENSITIVITY: self._estimate_data_sensitivity(osint_data),
            RiskFactor.THREAT_ACTOR_CAPABILITY: self._assess_threat_capability(indicators),
            RiskFactor.ATTACK_SURFACE: self._calculate_attack_surface(osint_data),
            RiskFactor.DEFENSIVE_POSTURE: self._estimate_defensive_posture(osint_data)
        }

        # Calculate overall risk score
        overall_score = sum(risk_factors.values()) / len(risk_factors)

        # Generate vulnerabilities
        vulnerabilities = self._identify_vulnerabilities(osint_data, indicators)

        # Generate recommendations
        recommendations = self._generate_risk_recommendations(risk_factors, vulnerabilities)

        assessment = RiskAssessment(
            assessment_id=f"RISK-{hashlib.md5(f'{target}-{now}'.encode()).hexdigest()[:8].upper()}",
            target=target,
            overall_risk_score=overall_score,
            risk_factors=risk_factors,
            threat_indicators=indicators,
            vulnerabilities=vulnerabilities,
            recommendations=recommendations,
            assessment_date=now,
            next_assessment_due=now + timedelta(days=30)
        )

        return assessment

    def _calculate_exposure_level(self, osint_data: Dict[str, Any]) -> float:
        """Calculate exposure level based on OSINT data"""
        exposure_score = 0.0
        max_score = 10.0

        # More data categories = higher exposure
        data_categories = len(osint_data.keys())
        exposure_score += min(5.0, data_categories * 0.5)

        # Total data points
        total_items = sum(len(v) if isinstance(v, list) else 1 for v in osint_data.values())
        exposure_score += min(5.0, total_items * 0.1)

        return min(max_score, exposure_score)

    def _estimate_data_sensitivity(self, osint_data: Dict[str, Any]) -> float:
        """Estimate data sensitivity level"""
        sensitivity_score = 0.0

        # Sensitive data types
        sensitive_types = ['emails', 'phone', 'addresses', 'personal_info']

        for data_type in sensitive_types:
            if data_type in osint_data:
                sensitivity_score += 2.5

        return min(10.0, sensitivity_score)

    def _assess_threat_capability(self, indicators: List[ThreatIndicator]) -> float:
        """Assess threat actor capability based on indicators"""
        if not indicators:
            return 0.0

        capability_score = 0.0

        for indicator in indicators:
            level_scores = {
                ThreatLevel.INFORMATIONAL: 0.5,
                ThreatLevel.LOW: 1.0,
                ThreatLevel.MEDIUM: 2.5,
                ThreatLevel.HIGH: 5.0,
                ThreatLevel.CRITICAL: 8.0
            }
            capability_score += level_scores.get(indicator.threat_level, 0.0) * indicator.confidence

        return min(10.0, capability_score / len(indicators))

    def _calculate_attack_surface(self, osint_data: Dict[str, Any]) -> float:
        """Calculate attack surface based on exposed data"""
        attack_surface = 0.0

        # Digital footprint categories that increase attack surface
        surface_categories = {
            'usernames': 1.0,
            'emails': 2.0,
            'domains': 1.5,
            'social_media': 1.0,
            'phone': 2.5
        }

        for category, weight in surface_categories.items():
            if category in osint_data:
                items = osint_data[category]
                item_count = len(items) if isinstance(items, list) else 1
                attack_surface += weight * min(3.0, item_count * 0.5)

        return min(10.0, attack_surface)

    def _estimate_defensive_posture(self, osint_data: Dict[str, Any]) -> float:
        """Estimate defensive security posture"""
        # This is inverse - lower score means better defenses
        # Based on exposure of sensitive information
        defensive_score = 5.0  # Start with medium assumption

        # Reduce score (better defenses) if less sensitive data exposed
        if 'emails' not in osint_data or len(osint_data.get('emails', [])) < 3:
            defensive_score -= 1.0

        if 'phone' not in osint_data:
            defensive_score -= 1.0

        # Increase score (worse defenses) if lots of data exposed
        total_exposure = sum(len(v) if isinstance(v, list) else 1 for v in osint_data.values())
        if total_exposure > 20:
            defensive_score += 2.0

        return max(0.0, min(10.0, defensive_score))

    def _identify_vulnerabilities(self, osint_data: Dict[str, Any], indicators: List[ThreatIndicator]) -> List[str]:
        """Identify security vulnerabilities"""
        vulnerabilities = []

        # Common OSINT-based vulnerabilities
        if 'emails' in osint_data and len(osint_data['emails']) > 5:
            vulnerabilities.append("High email address exposure increases phishing attack risk")

        if 'usernames' in osint_data and len(osint_data['usernames']) > 10:
            vulnerabilities.append("Excessive username exposure enables account enumeration attacks")

        if any(ind.threat_category == ThreatCategory.PHISHING for ind in indicators):
            vulnerabilities.append("Presence of phishing indicators suggests ongoing targeting")

        if 'phone' in osint_data:
            vulnerabilities.append("Phone number exposure enables social engineering attacks")

        # Always include general recommendations
        vulnerabilities.append("Publicly available information can be leveraged for social engineering")

        return vulnerabilities

    def _generate_risk_recommendations(self, risk_factors: Dict[RiskFactor, float], vulnerabilities: List[str]) -> List[str]:
        """Generate risk mitigation recommendations"""
        recommendations = []

        # High exposure recommendations
        if risk_factors.get(RiskFactor.EXPOSURE_LEVEL, 0) > 7.0:
            recommendations.append("Implement information exposure monitoring and control measures")

        # High attack surface recommendations
        if risk_factors.get(RiskFactor.ATTACK_SURFACE, 0) > 7.0:
            recommendations.append("Reduce attack surface through data minimization strategies")

        # Poor defensive posture recommendations
        if risk_factors.get(RiskFactor.DEFENSIVE_POSTURE, 0) > 7.0:
            recommendations.append("Enhance security controls and monitoring capabilities")

        # General recommendations
        recommendations.extend([
            "Conduct regular security awareness training",
            "Implement multi-factor authentication on all accounts",
            "Monitor for unauthorized use of discovered information",
            "Establish incident response procedures for identified threats"
        ])

        return recommendations

    def _calculate_overall_threat_level(self, indicators: List[ThreatIndicator], alerts: List[SecurityAlert]) -> ThreatLevel:
        """Calculate overall threat level"""
        if not indicators and not alerts:
            return ThreatLevel.INFORMATIONAL

        # Get highest threat level from indicators
        max_indicator_level = ThreatLevel.INFORMATIONAL
        if indicators:
            level_order = [ThreatLevel.INFORMATIONAL, ThreatLevel.LOW, ThreatLevel.MEDIUM, ThreatLevel.HIGH, ThreatLevel.CRITICAL]
            max_indicator_level = max(ind.threat_level for ind in indicators)

        # Get highest threat level from alerts
        max_alert_level = ThreatLevel.INFORMATIONAL
        if alerts:
            max_alert_level = max(alert.threat_level for alert in alerts)

        # Return the higher of the two
        level_values = {
            ThreatLevel.INFORMATIONAL: 0,
            ThreatLevel.LOW: 1,
            ThreatLevel.MEDIUM: 2,
            ThreatLevel.HIGH: 3,
            ThreatLevel.CRITICAL: 4
        }

        max_value = max(level_values[max_indicator_level], level_values[max_alert_level])
        return [level for level, value in level_values.items() if value == max_value][0]

    def _generate_security_recommendations(self, target: str, indicators: List[ThreatIndicator], risk_assessment: RiskAssessment) -> List[str]:
        """Generate comprehensive security recommendations"""
        recommendations = []

        # Risk-based recommendations
        if risk_assessment.overall_risk_score > 7.0:
            recommendations.append("🚨 CRITICAL: Immediate security review required - high risk detected")
        elif risk_assessment.overall_risk_score > 5.0:
            recommendations.append("⚠️ WARNING: Enhanced security measures recommended")

        # Indicator-based recommendations
        if indicators:
            categories = set(ind.threat_category for ind in indicators)

            if ThreatCategory.PHISHING in categories:
                recommendations.append("📧 Implement advanced email security and phishing protection")

            if ThreatCategory.MALWARE in categories:
                recommendations.append("🛡️ Deploy enhanced endpoint protection and monitoring")

            if ThreatCategory.SUSPICIOUS_ACTIVITY in categories:
                recommendations.append("👁️ Increase monitoring and logging for suspicious activities")

        # General recommendations
        recommendations.extend([
            "📚 Conduct security awareness training for identified risks",
            "🔒 Review and enhance access controls and authentication",
            "📊 Establish continuous monitoring for new threats",
            "📋 Document all findings for threat intelligence"
        ])

        return recommendations

    # Persistence methods
    def _load_alerts(self) -> List[SecurityAlert]:
        """Load security alerts from storage"""
        try:
            if self.alerts_file.exists():
                with open(self.alerts_file, 'r') as f:
                    data = json.load(f)
                    alerts = []
                    for alert_data in data:
                        # Convert indicators
                        indicators = []
                        for ind_data in alert_data.get('indicators', []):
                            indicators.append(self._dict_to_indicator(ind_data))

                        alert = SecurityAlert(
                            alert_id=alert_data['alert_id'],
                            title=alert_data['title'],
                            description=alert_data['description'],
                            threat_level=ThreatLevel(alert_data['threat_level']),
                            threat_category=ThreatCategory(alert_data['threat_category']),
                            indicators=indicators,
                            affected_targets=alert_data['affected_targets'],
                            risk_score=alert_data['risk_score'],
                            created_at=datetime.fromisoformat(alert_data['created_at']),
                            status=alert_data['status'],
                            recommendations=alert_data['recommendations'],
                            technical_details=alert_data['technical_details']
                        )
                        alerts.append(alert)

                    logger.info(f"🚨 Loaded {len(alerts)} security alerts from storage")
                    return alerts
        except Exception as e:
            logger.error(f"❌ Error loading alerts: {e}")
        return []

    def _save_alerts(self):
        """Save security alerts to storage"""
        try:
            data = [self._alert_to_dict(alert) for alert in self.security_alerts]
            with open(self.alerts_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"💾 Saved {len(self.security_alerts)} alerts to storage")
        except Exception as e:
            logger.error(f"❌ Error saving alerts: {e}")

    def _load_indicators(self) -> List[ThreatIndicator]:
        """Load threat indicators from storage"""
        try:
            if self.indicators_file.exists():
                with open(self.indicators_file, 'r') as f:
                    data = json.load(f)
                    indicators = [self._dict_to_indicator(ind_data) for ind_data in data]
                    logger.info(f"🔍 Loaded {len(indicators)} threat indicators from storage")
                    return indicators
        except Exception as e:
            logger.error(f"❌ Error loading indicators: {e}")
        return []

    def _save_indicators(self):
        """Save threat indicators to storage"""
        try:
            data = [self._indicator_to_dict(indicator) for indicator in self.threat_indicators]
            with open(self.indicators_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"💾 Saved {len(self.threat_indicators)} indicators to storage")
        except Exception as e:
            logger.error(f"❌ Error saving indicators: {e}")

    def _load_assessments(self) -> List[RiskAssessment]:
        """Load risk assessments from storage"""
        try:
            if self.assessments_file.exists():
                with open(self.assessments_file, 'r') as f:
                    data = json.load(f)
                    assessments = []
                    for assess_data in data:
                        # Convert risk factors
                        risk_factors = {}
                        for factor_name, value in assess_data['risk_factors'].items():
                            risk_factors[RiskFactor(factor_name)] = value

                        # Convert threat indicators
                        indicators = [self._dict_to_indicator(ind_data) for ind_data in assess_data['threat_indicators']]

                        assessment = RiskAssessment(
                            assessment_id=assess_data['assessment_id'],
                            target=assess_data['target'],
                            overall_risk_score=assess_data['overall_risk_score'],
                            risk_factors=risk_factors,
                            threat_indicators=indicators,
                            vulnerabilities=assess_data['vulnerabilities'],
                            recommendations=assess_data['recommendations'],
                            assessment_date=datetime.fromisoformat(assess_data['assessment_date']),
                            next_assessment_due=datetime.fromisoformat(assess_data['next_assessment_due'])
                        )
                        assessments.append(assessment)

                    logger.info(f"📊 Loaded {len(assessments)} risk assessments from storage")
                    return assessments
        except Exception as e:
            logger.error(f"❌ Error loading assessments: {e}")
        return []

    def _save_assessments(self):
        """Save risk assessments to storage"""
        try:
            data = [self._assessment_to_dict(assessment) for assessment in self.risk_assessments]
            with open(self.assessments_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"💾 Saved {len(self.risk_assessments)} assessments to storage")
        except Exception as e:
            logger.error(f"❌ Error saving assessments: {e}")

    # Serialization helper methods
    def _indicator_to_dict(self, indicator: ThreatIndicator) -> Dict[str, Any]:
        """Convert ThreatIndicator to dictionary"""
        return {
            "indicator_id": indicator.indicator_id,
            "indicator_type": indicator.indicator_type,
            "indicator_value": indicator.indicator_value,
            "threat_level": indicator.threat_level.value,
            "threat_category": indicator.threat_category.value,
            "confidence": indicator.confidence,
            "description": indicator.description,
            "source": indicator.source,
            "first_seen": indicator.first_seen.isoformat(),
            "last_seen": indicator.last_seen.isoformat(),
            "metadata": indicator.metadata
        }

    def _dict_to_indicator(self, data: Dict[str, Any]) -> ThreatIndicator:
        """Convert dictionary to ThreatIndicator"""
        return ThreatIndicator(
            indicator_id=data['indicator_id'],
            indicator_type=data['indicator_type'],
            indicator_value=data['indicator_value'],
            threat_level=ThreatLevel(data['threat_level']),
            threat_category=ThreatCategory(data['threat_category']),
            confidence=data['confidence'],
            description=data['description'],
            source=data['source'],
            first_seen=datetime.fromisoformat(data['first_seen']),
            last_seen=datetime.fromisoformat(data['last_seen']),
            metadata=data['metadata']
        )

    def _alert_to_dict(self, alert: SecurityAlert) -> Dict[str, Any]:
        """Convert SecurityAlert to dictionary"""
        return {
            "alert_id": alert.alert_id,
            "title": alert.title,
            "description": alert.description,
            "threat_level": alert.threat_level.value,
            "threat_category": alert.threat_category.value,
            "indicators": [self._indicator_to_dict(ind) for ind in alert.indicators],
            "affected_targets": alert.affected_targets,
            "risk_score": alert.risk_score,
            "created_at": alert.created_at.isoformat(),
            "status": alert.status,
            "recommendations": alert.recommendations,
            "technical_details": alert.technical_details
        }

    def _assessment_to_dict(self, assessment: RiskAssessment) -> Dict[str, Any]:
        """Convert RiskAssessment to dictionary"""
        return {
            "assessment_id": assessment.assessment_id,
            "target": assessment.target,
            "overall_risk_score": assessment.overall_risk_score,
            "risk_factors": {factor.value: score for factor, score in assessment.risk_factors.items()},
            "threat_indicators": [self._indicator_to_dict(ind) for ind in assessment.threat_indicators],
            "vulnerabilities": assessment.vulnerabilities,
            "recommendations": assessment.recommendations,
            "assessment_date": assessment.assessment_date.isoformat(),
            "next_assessment_due": assessment.next_assessment_due.isoformat()
        }

    def _initialize_threat_patterns(self) -> Dict[str, List[str]]:
        """Initialize known threat patterns"""
        return {
            "phishing_domains": [
                "secure-paypal-update.com",
                "amazon-security-alert.com",
                "microsoft-account-verification.com",
                "google-security-check.com"
            ],
            "malware_domains": [
                "malicious-download.tk",
                "virus-update.ml",
                "fake-antivirus.ga"
            ],
            "suspicious_tlds": [
                ".tk", ".ml", ".ga", ".cf", ".bit", ".onion"
            ]
        }

    def _initialize_suspicious_patterns(self) -> Dict[str, List[str]]:
        """Initialize suspicious patterns for detection"""
        return {
            "email_patterns": [
                r"noreply\d+@",
                r"admin\d+@",
                r"[0-9]{6,}@"
            ],
            "username_patterns": [
                r"admin\d{3,}",
                r"hacker\w*",
                r"exploit\w*",
                r"\w*bot\w*"
            ],
            "domain_patterns": [
                r"[0-9a-f]{16,}\.com",  # Long hex strings
                r"[bcdfghjklmnpqrstvwxz]{5,}\.com"  # Consonant clusters
            ]
        }

    def format_threat_report(self, analysis_results: Dict[str, Any]) -> str:
        """Format threat analysis results for display"""
        report = "🦹‍♂️ M.A.D. THREAT ANALYSIS REPORT\n"
        report += "=" * 50 + "\n\n"

        target = analysis_results.get("target", "Unknown")
        threat_level = analysis_results.get("overall_threat_level", "informational")

        # Threat level emoji
        level_emojis = {
            "informational": "ℹ️",
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
        }

        emoji = level_emojis.get(threat_level, "❓")

        report += f"{emoji} TARGET: {target}\n"
        report += f"{emoji} THREAT LEVEL: {threat_level.upper()}\n"
        report += f"📅 ANALYSIS TIME: {analysis_results.get('analysis_timestamp', 'Unknown')}\n\n"

        # Threat indicators
        indicators = analysis_results.get("threat_indicators", [])
        if indicators:
            report += f"🚨 THREAT INDICATORS ({len(indicators)}):\n"
            for i, indicator in enumerate(indicators[:5], 1):  # Show first 5
                report += f"  {i}. {indicator.get('indicator_type', 'unknown').upper()}: {indicator.get('indicator_value', 'N/A')}\n"
                report += f"     Level: {indicator.get('threat_level', 'unknown')} | Confidence: {indicator.get('confidence', 0):.1%}\n"
                report += f"     {indicator.get('description', 'No description')}\n\n"

            if len(indicators) > 5:
                report += f"     ... and {len(indicators) - 5} more indicators\n\n"
        else:
            report += "✅ No significant threat indicators detected\n\n"

        # Security alerts
        alerts = analysis_results.get("security_alerts", [])
        if alerts:
            report += f"🚨 SECURITY ALERTS ({len(alerts)}):\n"
            for alert in alerts:
                report += f"  • {alert.get('title', 'Unknown Alert')}\n"
                report += f"    Risk Score: {alert.get('risk_score', 0):.1f}/10.0\n"
                report += f"    Status: {alert.get('status', 'unknown')}\n\n"

        # Risk assessment
        risk_assessment = analysis_results.get("risk_assessment")
        if risk_assessment:
            score = risk_assessment.get("overall_risk_score", 0)
            report += f"📊 RISK ASSESSMENT:\n"
            report += f"  Overall Risk Score: {score:.1f}/10.0\n"

            vulnerabilities = risk_assessment.get("vulnerabilities", [])
            if vulnerabilities:
                report += f"  Vulnerabilities: {len(vulnerabilities)} identified\n"

        # Recommendations
        recommendations = analysis_results.get("recommendations", [])
        if recommendations:
            report += f"\n💡 RECOMMENDATIONS:\n"
            for i, rec in enumerate(recommendations[:3], 1):  # Show first 3
                report += f"  {i}. {rec}\n"

        report += f"\n🦹‍♂️ M.A.D. Detection System - Threat analysis complete"
        return report

    def get_threat_summary(self) -> Dict[str, Any]:
        """Get summary of all threat data"""
        return {
            "total_indicators": len(self.threat_indicators),
            "active_alerts": len([alert for alert in self.security_alerts if alert.status == "open"]),
            "total_assessments": len(self.risk_assessments),
            "high_risk_indicators": len([ind for ind in self.threat_indicators if ind.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]]),
            "recent_alerts": len([alert for alert in self.security_alerts if (datetime.now() - alert.created_at).days <= 7])
        }


# Global M.A.D. Detection instance
mad_detection = MADDetection()