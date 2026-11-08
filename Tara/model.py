
from dataclasses import dataclass, field
from typing import Optional


CYBERSECURITY_PROPERTIES = [
    "Confidentiality",
    "Integrity",
    "Availability"
]

IMPACT_CATEGORIES = [
    "Safety",
    "Financial",
    "Operational",
    "Privacy"
]

IMPACT_RATINGS = [
    "Severe",
    "Major",
    "Moderate",
    "Negligible"
]

THREAT_TYPES = [
    "Spoofing",
    "Tampering",
    "Repudiation",
    "Information Disclosure",
    "Denial of Service",
    "Elevation of Privilege"
]

RISK_TREATMENTS = [
    "Avoid",
    "Reduce",
    "Share",
    "Retain"
]


@dataclass
class Item:
    id: str
    name: str
    description: str


@dataclass
class Asset:
    id: str
    name: str
    description: str
    cybersecurity_properties: list[str]


@dataclass
class DamageScenario:
    id: str
    asset_id: str
    description: str
    impact_category: str
    impact_rating: str


@dataclass
class ThreatScenario:
    id: str
    asset_id: str
    damage_scenario_id: str
    description: str
    threat_type: str


@dataclass
class AttackPathStep:
    id: str
    description: str
    elapsed_time: str
    specialist_expertise: str
    knowledge_of_item: str
    window_of_opportunity: str
    equipment: str


@dataclass
class AttackPath:
    id: str
    threat_scenario_id: str
    steps: list[AttackPathStep] = field(default_factory=list)


@dataclass
class RiskTreatment:
    decision: str
    rationale: Optional[str] = None


@dataclass
class TARAAnalysis:
    item: Item
    assets: list[Asset] = field(default_factory=list)
    damage_scenarios: list[DamageScenario] = field(default_factory=list)
    threat_scenarios: list[ThreatScenario] = field(default_factory=list)
    attack_paths: list[AttackPath] = field(default_factory=list)
    cybersecurity_goals: list[str] = field(default_factory=list)
    cybersecurity_requirements: list[str] = field(default_factory=list)
    mitigations: list[str] = field(default_factory=list)
