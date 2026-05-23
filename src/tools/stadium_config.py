"""
Stadium configurations — real data for major Indian cricket venues.
Each stadium has gates, sections, capacity, and event-specific protocols.
"""

STADIUMS = {
    "narendra_modi": {
        "id": "narendra_modi",
        "name": "Narendra Modi Stadium",
        "city": "Ahmedabad, Gujarat",
        "capacity": 132000,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Narendra_Modi_Stadium.jpg/1280px-Narendra_Modi_Stadium.jpg",
        "gates": {
            "G1": {"name": "Gate 1 — East VIP", "capacity": 8000, "type": "vip"},
            "G2": {"name": "Gate 2 — East General", "capacity": 15000, "type": "general"},
            "G3": {"name": "Gate 3 — North East", "capacity": 12000, "type": "general"},
            "G4": {"name": "Gate 4 — North", "capacity": 14000, "type": "general"},
            "G5": {"name": "Gate 5 — North West", "capacity": 12000, "type": "general"},
            "G6": {"name": "Gate 6 — West VIP", "capacity": 8000, "type": "vip"},
            "G7": {"name": "Gate 7 — West General", "capacity": 15000, "type": "general"},
            "G8": {"name": "Gate 8 — South West", "capacity": 12000, "type": "general"},
            "G9": {"name": "Gate 9 — South", "capacity": 14000, "type": "general"},
            "G10": {"name": "Gate 10 — South East", "capacity": 12000, "type": "general"},
        },
        "sections": [
            "Adani Pavilion (East)", "Reliance Stand (West)",
            "Tata Corporate Box (North)", "BCCI VIP Box",
            "Lower Tier East", "Lower Tier West",
            "Upper Tier East", "Upper Tier West",
            "Student Zone (North)", "Family Stand (South)",
        ],
        "emergency_contacts": {
            "security_chief": "Radio Ch 1",
            "medical": "Radio Ch 2",
            "police_control": "Ahmedabad Police: 100",
            "fire": "Gujarat Fire: 101",
            "stadium_ops": "Radio Ch 3",
        },
        "upcoming_event": {
            "date": "31 May 2026",
            "match": "IPL 2026 Final",
            "teams": "TBD vs TBD",
            "expected_crowd": 130000,
            "high_risk": True,
            "notes": "Maximum capacity event. Pre-position all 10 gates. Additional police deployment mandatory.",
        },
    },
    "wankhede": {
        "id": "wankhede",
        "name": "Wankhede Stadium",
        "city": "Mumbai, Maharashtra",
        "capacity": 33108,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Wankhede_stadium.jpg/1280px-Wankhede_stadium.jpg",
        "gates": {
            "G1": {"name": "Gate 1 — North VIP", "capacity": 3000, "type": "vip"},
            "G2": {"name": "Gate 2 — North General", "capacity": 4000, "type": "general"},
            "G3": {"name": "Gate 3 — East", "capacity": 4000, "type": "general"},
            "G4": {"name": "Gate 4 — South East", "capacity": 3500, "type": "general"},
            "G5": {"name": "Gate 5 — South", "capacity": 4000, "type": "general"},
            "G6": {"name": "Gate 6 — South West", "capacity": 3500, "type": "general"},
            "G7": {"name": "Gate 7 — West", "capacity": 4000, "type": "general"},
            "G8": {"name": "Gate 8 — North West", "capacity": 3500, "type": "general"},
        },
        "sections": [
            "Garware Pavilion", "Sunil Gavaskar Stand",
            "Vijay Merchant Stand", "Sachin Tendulkar Stand",
            "North Stand", "South Stand",
        ],
        "emergency_contacts": {
            "security_chief": "Radio Ch 1",
            "medical": "Radio Ch 2",
            "police_control": "Mumbai Police: 100",
            "fire": "Mumbai Fire: 101",
        },
        "upcoming_event": None,
    },
    "chinnaswamy": {
        "id": "chinnaswamy",
        "name": "M. Chinnaswamy Stadium",
        "city": "Bengaluru, Karnataka",
        "capacity": 38000,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/M._Chinnaswamy_Stadium.jpg/1280px-M._Chinnaswamy_Stadium.jpg",
        "gates": {
            "G1": {"name": "Gate 1 — East VIP", "capacity": 3000, "type": "vip"},
            "G2": {"name": "Gate 2 — East", "capacity": 5000, "type": "general"},
            "G3": {"name": "Gate 3 — North", "capacity": 5000, "type": "general"},
            "G4": {"name": "Gate 4 — West", "capacity": 5000, "type": "general"},
            "G5": {"name": "Gate 5 — South", "capacity": 5000, "type": "general"},
            "G6": {"name": "Gate 6 — South East", "capacity": 4000, "type": "general"},
        },
        "sections": [
            "KSCA Pavilion", "Corporate Box",
            "East Stand", "West Stand",
            "North Stand", "South Stand",
        ],
        "emergency_contacts": {
            "security_chief": "Radio Ch 1",
            "medical": "Radio Ch 2",
            "police_control": "Bengaluru Police: 100",
            "fire": "Karnataka Fire: 101",
        },
        "incident_history": [
            {
                "date": "2024",
                "type": "Victory Parade Stampede",
                "description": "RCB IPL victory parade — uncontrolled crowd surge outside stadium. 70+ injured. Root cause: inadequate pre-event capacity planning and no dynamic crowd routing.",
                "lessons": [
                    "Mandatory pre-registration for victory parades",
                    "Dynamic zone-based crowd routing",
                    "Real-time density monitoring at all perimeter points",
                    "Proactive PA dispersal announcements every 5 minutes",
                    "Dedicated emergency vehicle corridor must remain clear",
                ],
            }
        ],
        "upcoming_event": None,
    },
    "eden_gardens": {
        "id": "eden_gardens",
        "name": "Eden Gardens",
        "city": "Kolkata, West Bengal",
        "capacity": 66000,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Eden_Gardens_Cricket_Stadium.jpg/1280px-Eden_Gardens_Cricket_Stadium.jpg",
        "gates": {
            "G1": {"name": "Gate 1 — Club House", "capacity": 5000, "type": "vip"},
            "G2": {"name": "Gate 2 — North", "capacity": 8000, "type": "general"},
            "G3": {"name": "Gate 3 — East", "capacity": 8000, "type": "general"},
            "G4": {"name": "Gate 4 — South East", "capacity": 7000, "type": "general"},
            "G5": {"name": "Gate 5 — South", "capacity": 8000, "type": "general"},
            "G6": {"name": "Gate 6 — West", "capacity": 8000, "type": "general"},
        },
        "sections": [
            "Club House", "BCCI Box",
            "North Stand", "South Stand",
            "East Stand B", "East Stand C",
        ],
        "emergency_contacts": {
            "security_chief": "Radio Ch 1",
            "medical": "Radio Ch 2",
            "police_control": "Kolkata Police: 100",
        },
        "upcoming_event": None,
    },
}

EVENT_TYPES = {
    "ipl_match": {
        "name": "IPL Match",
        "risk_multiplier": 1.3,
        "protocols": ["crowd_surge", "security_screening", "post_match_dispersal"],
        "notes": "High energy, expect rapid crowd surge at entry. Peak risk: 90 mins before match.",
    },
    "test_match": {
        "name": "Test Match",
        "risk_multiplier": 0.8,
        "protocols": ["crowd_surge", "weather"],
        "notes": "Spread entry over 5 days. Day 1 and Day 5 (result day) highest risk.",
    },
    "world_cup": {
        "name": "World Cup Match",
        "risk_multiplier": 1.8,
        "protocols": ["crowd_surge", "security_screening", "vip_protocol", "emergency"],
        "notes": "International event — highest security tier. Expect 100% capacity.",
    },
    "victory_parade": {
        "name": "Victory Parade / Celebration",
        "risk_multiplier": 2.5,
        "protocols": ["crowd_surge", "emergency", "unplanned_gathering"],
        "risk_level": "EXTREME",
        "notes": "EXTREME RISK. Uncontrolled crowd — no ticketing. Reference: Chinnaswamy 2024 incident. Mandatory: zone-based routing, 5-min PA intervals, emergency vehicle corridors.",
        "chinnaswamy_warning": True,
    },
    "concert": {
        "name": "Concert / Non-Cricket Event",
        "risk_multiplier": 1.5,
        "protocols": ["crowd_surge", "weather", "medical"],
        "notes": "Different crowd profile — younger, less familiar with stadium layout.",
    },
    "ipl_final": {
        "name": "IPL Final",
        "risk_multiplier": 2.0,
        "protocols": ["crowd_surge", "security_screening", "vip_protocol", "emergency", "post_match_dispersal"],
        "risk_level": "VERY HIGH",
        "notes": "Maximum capacity expected. Pre-position all gates 4 hours before. Mandatory police deployment at all entry points.",
    },
}


def get_stadium(stadium_id: str) -> dict:
    return STADIUMS.get(stadium_id, STADIUMS["narendra_modi"])


def get_event_type(event_id: str) -> dict:
    return EVENT_TYPES.get(event_id, EVENT_TYPES["ipl_match"])


def list_stadiums() -> list:
    return [{"id": k, "name": v["name"], "city": v["city"], "capacity": v["capacity"]} for k, v in STADIUMS.items()]
