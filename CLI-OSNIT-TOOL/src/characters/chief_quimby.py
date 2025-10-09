#!/usr/bin/env python3
"""
Chief Quimby - Mission Briefings & Case Management

Like Chief Quimby in Inspector Gadget who provided missions and briefings,
this Chief Quimby manages OSINT cases, provides investigation briefings,
tracks mission progress, and coordinates multiple investigations.

Chief Quimby's Capabilities:
- Mission briefing generation and delivery
- Case management and tracking
- Investigation assignment and coordination
- Progress monitoring and reporting
- Strategic oversight and guidance
- Multi-case correlation and insights
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class MissionPriority(Enum):
    """Mission priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    CLASSIFIED = "classified"


class MissionStatus(Enum):
    """Mission status tracking"""
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"


class CaseType(Enum):
    """Types of OSINT investigations"""
    INDIVIDUAL = "individual"       # Single person investigation
    CORPORATE = "corporate"         # Company/organization investigation
    INFRASTRUCTURE = "infrastructure"  # Technical infrastructure analysis
    THREAT_INTEL = "threat_intel"   # Security threat investigation
    BACKGROUND = "background"       # Background check operations
    SURVEILLANCE = "surveillance"   # Monitoring and tracking
    FORENSIC = "forensic"          # Digital forensics investigation


@dataclass
class Mission:
    """OSINT Mission data structure"""
    mission_id: str
    title: str
    description: str
    case_type: CaseType
    priority: MissionPriority
    status: MissionStatus
    target: str                    # Primary investigation target
    objectives: List[str]          # Mission objectives
    assigned_to: str              # Inspector assigned
    created_at: datetime
    deadline: Optional[datetime]
    progress: int                  # 0-100%
    findings: Dict[str, Any]       # Investigation results
    notes: List[str]              # Mission notes
    resources: List[str]          # Required tools/modules

    def to_dict(self) -> Dict[str, Any]:
        """Convert Mission to dictionary for JSON serialization"""
        data = asdict(self)
        data['case_type'] = self.case_type.value
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        data['deadline'] = self.deadline.isoformat() if self.deadline else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Mission':
        """Create Mission from dictionary"""
        data['case_type'] = CaseType(data['case_type'])
        data['priority'] = MissionPriority(data['priority'])
        data['status'] = MissionStatus(data['status'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['deadline'] = datetime.fromisoformat(data['deadline']) if data['deadline'] else None
        return cls(**data)


@dataclass
class CaseBriefing:
    """Mission briefing information"""
    briefing_id: str
    mission_id: str
    briefing_type: str            # initial, progress, final
    content: str
    key_points: List[str]
    recommendations: List[str]
    urgency_level: str
    classified: bool
    timestamp: datetime


class ChiefQuimby:
    """
    Chief Quimby - Mission Control & Case Management

    Chief Quimby provides mission briefings, manages OSINT cases,
    tracks investigation progress, and ensures operational success.
    """

    def __init__(self):
        self.personality_traits = {
            "authoritative": True,
            "organized": True,
            "strategic": True,
            "thorough": True,
            "supportive": True
        }

        # Set up persistent storage
        self.data_dir = Path.home() / ".inspector-g" / "missions"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.missions_file = self.data_dir / "active_missions.json"
        self.history_file = self.data_dir / "mission_history.json"

        # Load existing data
        self.active_missions = self._load_missions()
        self.mission_history = self._load_history()
        self.case_templates = self._initialize_case_templates()
        logger.info("👨‍💼 Chief Quimby initialized - Mission control operational!")

    def greet_agent(self, agent_name: str = "Inspector") -> str:
        """Chief Quimby's official greeting"""
        greetings = [
            f"Attention {agent_name}! Chief Quimby here with your mission briefing.",
            f"Good work on your last case, {agent_name}. I have a new assignment for you.",
            f"{agent_name}, report to my office immediately! We have a situation that requires your expertise.",
            f"Inspector {agent_name}, your country needs you for this critical OSINT operation.",
            f"Listen carefully, {agent_name}. This mission is of utmost importance to national security."
        ]
        import random
        return random.choice(greetings)

    def create_mission(
        self,
        title: str,
        target: str,
        case_type: CaseType,
        priority: MissionPriority = MissionPriority.NORMAL,
        objectives: Optional[List[str]] = None,
        deadline_hours: Optional[int] = None
    ) -> Mission:
        """Create a new OSINT mission"""

        mission_id = f"MISSION-{uuid.uuid4().hex[:8].upper()}"

        if not objectives:
            objectives = self._generate_default_objectives(case_type, target)

        deadline = None
        if deadline_hours:
            deadline = datetime.now() + timedelta(hours=deadline_hours)

        mission = Mission(
            mission_id=mission_id,
            title=title,
            description=self._generate_mission_description(case_type, target, priority),
            case_type=case_type,
            priority=priority,
            status=MissionStatus.ASSIGNED,
            target=target,
            objectives=objectives,
            assigned_to="Inspector-G",
            created_at=datetime.now(),
            deadline=deadline,
            progress=0,
            findings={},
            notes=[],
            resources=self._suggest_resources(case_type)
        )

        self.active_missions[mission_id] = mission
        self._save_missions()  # Persist to disk
        logger.info(f"📋 Mission {mission_id} created: {title}")
        return mission

    def _generate_default_objectives(self, case_type: CaseType, target: str) -> List[str]:
        """Generate appropriate objectives based on case type"""

        objectives_map = {
            CaseType.INDIVIDUAL: [
                f"Identify all online accounts associated with {target}",
                f"Map social media presence and activity patterns",
                f"Discover contact information and communication channels",
                f"Analyze behavioral patterns and digital footprint",
                f"Assess potential security risks or threats"
            ],
            CaseType.CORPORATE: [
                f"Map organizational structure and key personnel",
                f"Identify corporate email patterns and communication systems",
                f"Analyze digital infrastructure and technology stack",
                f"Assess cybersecurity posture and vulnerabilities",
                f"Monitor corporate communications and public presence"
            ],
            CaseType.INFRASTRUCTURE: [
                f"Map network infrastructure and architecture",
                f"Identify exposed services and potential vulnerabilities",
                f"Analyze DNS records and domain configurations",
                f"Assess security configurations and access points",
                f"Monitor for suspicious activity or anomalies"
            ],
            CaseType.THREAT_INTEL: [
                f"Identify threat actors and their capabilities",
                f"Map attack vectors and methodologies",
                f"Analyze indicators of compromise (IOCs)",
                f"Assess threat landscape and emerging risks",
                f"Develop countermeasures and defensive strategies"
            ]
        }

        return objectives_map.get(case_type, [
            f"Conduct comprehensive OSINT analysis of {target}",
            f"Gather all available intelligence through multiple sources",
            f"Correlate findings across different data points",
            f"Provide detailed intelligence assessment"
        ])

    def _generate_mission_description(self, case_type: CaseType, target: str, priority: MissionPriority) -> str:
        """Generate mission description based on type and priority"""

        priority_context = {
            MissionPriority.LOW: "This is a routine intelligence gathering operation.",
            MissionPriority.NORMAL: "This investigation requires standard OSINT procedures.",
            MissionPriority.HIGH: "This is a high-priority investigation requiring immediate attention.",
            MissionPriority.CRITICAL: "URGENT: This critical operation demands your full attention and expertise.",
            MissionPriority.CLASSIFIED: "CLASSIFIED OPERATION: Maintain strict operational security protocols."
        }

        case_context = {
            CaseType.INDIVIDUAL: f"Individual subject investigation focusing on {target}.",
            CaseType.CORPORATE: f"Corporate intelligence operation targeting {target} organization.",
            CaseType.INFRASTRUCTURE: f"Technical infrastructure analysis of {target} systems.",
            CaseType.THREAT_INTEL: f"Threat intelligence operation investigating {target} threat actor.",
            CaseType.BACKGROUND: f"Background verification investigation of {target}.",
            CaseType.SURVEILLANCE: f"Surveillance and monitoring operation on {target}.",
            CaseType.FORENSIC: f"Digital forensics investigation related to {target}."
        }

        return f"{priority_context.get(priority, '')} {case_context.get(case_type, '')} Use all available OSINT capabilities and report findings immediately."

    def _suggest_resources(self, case_type: CaseType) -> List[str]:
        """Suggest appropriate Inspector-G modules for case type"""

        resource_map = {
            CaseType.INDIVIDUAL: ["username", "email", "phone", "ai"],
            CaseType.CORPORATE: ["email", "domain", "ai"],
            CaseType.INFRASTRUCTURE: ["domain", "phone", "ai"],
            CaseType.THREAT_INTEL: ["username", "domain", "ai"],
            CaseType.BACKGROUND: ["username", "email", "phone", "ai"],
            CaseType.SURVEILLANCE: ["username", "ai"],
            CaseType.FORENSIC: ["email", "domain", "ai"]
        }

        return resource_map.get(case_type, ["ai"])

    def generate_briefing(self, mission: Mission, briefing_type: str = "initial") -> CaseBriefing:
        """Generate mission briefing"""

        briefing_id = f"BRIEF-{uuid.uuid4().hex[:6].upper()}"

        if briefing_type == "initial":
            content = self._generate_initial_briefing(mission)
        elif briefing_type == "progress":
            content = self._generate_progress_briefing(mission)
        elif briefing_type == "final":
            content = self._generate_final_briefing(mission)
        else:
            content = f"Mission briefing for {mission.title}"

        briefing = CaseBriefing(
            briefing_id=briefing_id,
            mission_id=mission.mission_id,
            briefing_type=briefing_type,
            content=content,
            key_points=self._extract_key_points(mission, briefing_type),
            recommendations=self._generate_recommendations(mission, briefing_type),
            urgency_level=mission.priority.value,
            classified=mission.priority == MissionPriority.CLASSIFIED,
            timestamp=datetime.now()
        )

        return briefing

    def _generate_initial_briefing(self, mission: Mission) -> str:
        """Generate initial mission briefing"""

        urgency = "URGENT - " if mission.priority in [MissionPriority.HIGH, MissionPriority.CRITICAL] else ""

        briefing = f"""
{urgency}MISSION BRIEFING - {mission.mission_id}

OPERATION: {mission.title}
TARGET: {mission.target}
CASE TYPE: {mission.case_type.value.title()}
PRIORITY: {mission.priority.value.upper()}
DEADLINE: {mission.deadline.strftime('%Y-%m-%d %H:%M') if mission.deadline else 'No specific deadline'}

MISSION DESCRIPTION:
{mission.description}

OBJECTIVES:
"""

        for i, objective in enumerate(mission.objectives, 1):
            briefing += f"{i}. {objective}\n"

        briefing += f"""
RECOMMENDED RESOURCES:
{', '.join(mission.resources)}

OPERATIONAL NOTES:
- Maintain operational security at all times
- Document all findings thoroughly
- Report any unusual discoveries immediately
- Use appropriate Inspector-G modules for maximum efficiency

Remember: The success of this operation depends on your expertise and attention to detail.

Chief Quimby expects nothing less than excellence.

Good luck, Inspector!
"""
        return briefing

    def _generate_progress_briefing(self, mission: Mission) -> str:
        """Generate progress update briefing"""

        return f"""
PROGRESS REPORT - {mission.mission_id}

MISSION: {mission.title}
CURRENT STATUS: {mission.status.value.title()}
PROGRESS: {mission.progress}%
LAST UPDATE: {datetime.now().strftime('%Y-%m-%d %H:%M')}

CURRENT FINDINGS:
{len(mission.findings)} data categories discovered
Key discoveries logged and analyzed

NEXT STEPS:
Continue investigation according to mission objectives
Maintain momentum and thoroughness
Report significant findings immediately

Keep up the excellent work, Inspector!
"""

    def _generate_final_briefing(self, mission: Mission) -> str:
        """Generate final mission briefing"""

        return f"""
MISSION COMPLETION REPORT - {mission.mission_id}

OPERATION: {mission.title}
FINAL STATUS: {mission.status.value.title()}
COMPLETION: {mission.progress}%
COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M')}

MISSION SUMMARY:
Target: {mission.target}
Objectives Achieved: {len([obj for obj in mission.objectives if mission.progress >= 80])} of {len(mission.objectives)}

INTELLIGENCE GATHERED:
{len(mission.findings)} categories of intelligence collected
Comprehensive OSINT analysis completed

OPERATIONAL ASSESSMENT:
Mission objectives successfully achieved
Intelligence gathering protocols followed
All required documentation completed

COMMENDATION:
Excellent work, Inspector! Your thoroughness and expertise have resulted in a successful operation.
The intelligence gathered will be invaluable for future operations.

Chief Quimby is pleased with your performance.

Mission archived for future reference.
"""

    def _extract_key_points(self, mission: Mission, briefing_type: str) -> List[str]:
        """Extract key points for briefing"""

        if briefing_type == "initial":
            return [
                f"Target: {mission.target}",
                f"Priority: {mission.priority.value.upper()}",
                f"Case Type: {mission.case_type.value.title()}",
                f"Deadline: {mission.deadline.strftime('%Y-%m-%d') if mission.deadline else 'None'}",
                f"Resources: {', '.join(mission.resources)}"
            ]
        elif briefing_type == "progress":
            return [
                f"Progress: {mission.progress}%",
                f"Status: {mission.status.value.title()}",
                f"Findings: {len(mission.findings)} categories"
            ]
        else:  # final
            return [
                f"Mission Complete: {mission.progress}%",
                f"Intelligence: {len(mission.findings)} categories",
                f"Status: {mission.status.value.title()}"
            ]

    def _generate_recommendations(self, mission: Mission, briefing_type: str) -> List[str]:
        """Generate recommendations based on briefing type"""

        if briefing_type == "initial":
            return [
                "Begin with broad reconnaissance using AI analysis",
                "Use multiple OSINT modules for comprehensive coverage",
                "Document all findings in structured format",
                "Maintain operational security throughout investigation",
                "Report significant discoveries immediately"
            ]
        elif briefing_type == "progress":
            return [
                "Continue systematic investigation approach",
                "Cross-reference findings across multiple sources",
                "Pursue high-confidence leads first",
                "Prepare for potential escalation if needed"
            ]
        else:  # final
            return [
                "Archive all mission data securely",
                "Prepare detailed intelligence report",
                "Identify patterns for future operations",
                "Consider follow-up investigations if warranted"
            ]

    def update_mission_progress(self, mission_id: str, progress: int, findings: Optional[Dict] = None, notes: Optional[str] = None) -> bool:
        """Update mission progress and findings"""

        if mission_id not in self.active_missions:
            return False

        mission = self.active_missions[mission_id]
        mission.progress = min(100, max(0, progress))

        if findings:
            mission.findings.update(findings)

        if notes:
            mission.notes.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {notes}")

        # Update status based on progress
        if mission.progress == 100:
            mission.status = MissionStatus.COMPLETED
        elif mission.progress > 0:
            mission.status = MissionStatus.IN_PROGRESS

        self._save_missions()  # Persist changes to disk
        logger.info(f"📈 Mission {mission_id} progress updated to {progress}%")
        return True

    def get_mission_status(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """Get current mission status"""

        if mission_id not in self.active_missions:
            return None

        mission = self.active_missions[mission_id]

        return {
            "mission_id": mission.mission_id,
            "title": mission.title,
            "target": mission.target,
            "progress": mission.progress,
            "status": mission.status.value,
            "priority": mission.priority.value,
            "findings_count": len(mission.findings),
            "notes_count": len(mission.notes),
            "deadline": mission.deadline.isoformat() if mission.deadline else None,
            "time_remaining": self._calculate_time_remaining(mission.deadline) if mission.deadline else None
        }

    def _calculate_time_remaining(self, deadline: datetime) -> str:
        """Calculate time remaining until deadline"""

        now = datetime.now()
        if deadline <= now:
            return "OVERDUE"

        diff = deadline - now
        days = diff.days
        hours = diff.seconds // 3600

        if days > 0:
            return f"{days} day(s), {hours} hour(s)"
        elif hours > 0:
            return f"{hours} hour(s)"
        else:
            return "Less than 1 hour"

    def list_active_missions(self) -> List[Dict[str, Any]]:
        """List all active missions"""

        return [self.get_mission_status(mission_id) for mission_id in self.active_missions.keys()]

    def format_briefing_display(self, briefing: CaseBriefing) -> str:
        """Format briefing for terminal display"""

        classified_header = "🔒 CLASSIFIED 🔒\n" if briefing.classified else ""
        urgency_emoji = {"critical": "🚨", "high": "⚠️", "normal": "📋", "low": "📝"}.get(briefing.urgency_level, "📋")

        formatted = f"""
{classified_header}
{urgency_emoji} MISSION BRIEFING {urgency_emoji}
Briefing ID: {briefing.briefing_id}
Mission: {briefing.mission_id}
Type: {briefing.briefing_type.title()}
Timestamp: {briefing.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

{briefing.content}

KEY POINTS:
"""

        for point in briefing.key_points:
            formatted += f"• {point}\n"

        formatted += "\nRECOMMendations:\n"
        for rec in briefing.recommendations:
            formatted += f"• {rec}\n"

        formatted += f"\n{urgency_emoji} END BRIEFING {urgency_emoji}"

        return formatted

    def _load_missions(self) -> Dict[str, Mission]:
        """Load missions from persistent storage"""
        try:
            if self.missions_file.exists():
                with open(self.missions_file, 'r') as f:
                    data = json.load(f)
                    missions = {}
                    for mission_id, mission_data in data.items():
                        missions[mission_id] = Mission.from_dict(mission_data)
                    logger.info(f"📁 Loaded {len(missions)} active missions from storage")
                    return missions
        except Exception as e:
            logger.error(f"❌ Error loading missions: {e}")
        return {}

    def _save_missions(self):
        """Save missions to persistent storage"""
        try:
            data = {}
            for mission_id, mission in self.active_missions.items():
                data[mission_id] = mission.to_dict()

            with open(self.missions_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"💾 Saved {len(self.active_missions)} missions to storage")
        except Exception as e:
            logger.error(f"❌ Error saving missions: {e}")

    def _load_history(self) -> List[Mission]:
        """Load mission history from persistent storage"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    history = [Mission.from_dict(mission_data) for mission_data in data]
                    logger.info(f"📚 Loaded {len(history)} historical missions")
                    return history
        except Exception as e:
            logger.error(f"❌ Error loading mission history: {e}")
        return []

    def _save_history(self):
        """Save mission history to persistent storage"""
        try:
            data = [mission.to_dict() for mission in self.mission_history]
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"📚 Saved {len(self.mission_history)} historical missions")
        except Exception as e:
            logger.error(f"❌ Error saving mission history: {e}")

    def archive_mission(self, mission_id: str) -> bool:
        """Archive a completed mission to history"""
        if mission_id not in self.active_missions:
            return False

        mission = self.active_missions[mission_id]
        mission.status = MissionStatus.ARCHIVED

        # Move to history
        self.mission_history.append(mission)
        del self.active_missions[mission_id]

        # Save both files
        self._save_missions()
        self._save_history()

        logger.info(f"📦 Mission {mission_id} archived to history")
        return True

    def _initialize_case_templates(self) -> Dict[str, Dict]:
        """Initialize case templates for different investigation types"""

        return {
            "individual_investigation": {
                "objectives": [
                    "Identify all social media accounts",
                    "Map online presence and activity",
                    "Discover contact information",
                    "Analyze behavioral patterns"
                ],
                "resources": ["username", "email", "phone", "ai"],
                "estimated_duration": 4
            },
            "corporate_intelligence": {
                "objectives": [
                    "Map organizational structure",
                    "Identify key personnel",
                    "Analyze corporate communications",
                    "Assess security posture"
                ],
                "resources": ["email", "domain", "ai"],
                "estimated_duration": 8
            },
            "threat_assessment": {
                "objectives": [
                    "Identify threat indicators",
                    "Map attack vectors",
                    "Assess capabilities",
                    "Develop countermeasures"
                ],
                "resources": ["username", "domain", "ai"],
                "estimated_duration": 6
            }
        }


# Global Chief Quimby instance
chief_quimby = ChiefQuimby()