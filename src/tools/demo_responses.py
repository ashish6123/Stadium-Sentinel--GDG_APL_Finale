"""
Scripted demo responses — stadium-aware, event-aware, Gemini-quality output.
Automatically falls back here when LLM API is unavailable.
"""

DEMO_RESPONSES = {
    "crowd_nm": """**Routing to CrowdFlowAgent...**

[CrowdFlowAgent] Pulling live sensor data — Narendra Modi Stadium (132,000 capacity)...
[CrowdFlowAgent] Analyzing 10-gate distribution for IPL 2026 Final...

---
**CROWD FLOW ASSESSMENT — NARENDRA MODI STADIUM**
📅 31 May 2026 | IPL 2026 Final | 19:30 IST

🚨 **CRITICAL: Gate G4 at 96% — Immediate rerouting required**

| Gate | Load | Wait | Action |
|------|------|------|--------|
| G4 (North) | 🔴 96% | 42 min | CLOSE TO NEW ENTRY |
| G3 (NE) | 🟡 71% | 18 min | MONITOR |
| G9 (South) | 🟢 28% | 6 min | **DIVERT HERE** |
| G10 (SE) | 🟢 31% | 7 min | **DIVERT HERE** |

**IMMEDIATE ACTIONS:**
1. Close Gate G4 to new entries
2. Activate emergency signage directing fans to G9/G10
3. Deploy 6 stewards to G4 barrier
4. PA: *"Fans near Gate 4 — proceed to Gate 9 or 10. Under 7 minutes wait."*
5. Coordinate with Ahmedabad Traffic Police for SG Highway diversion

**Executive Summary:**
• G4 overflow critical — diversion to G9/G10 activated
• 4 additional gates approaching warning threshold
• Recommend all 10 gates open simultaneously now""",

    "crowd": """**Routing to CrowdFlowAgent...**

[CrowdFlowAgent] Analyzing real-time sensor data across all gates...

---
**CROWD FLOW ASSESSMENT**

🚨 Critical gate overflow detected — Immediate action required

**Congested Gates:** Queue depth exceeding 85% threshold
**Available Alternates:** 3 gates at under 35% load

**IMMEDIATE ACTIONS:**
1. Activate overflow gates — redirect all inbound traffic
2. Deploy crowd stewards to affected gate barriers
3. Broadcast PA: *"Please use alternate gates for faster entry"*
4. Alert medical team to standby at congested gate
5. Notify police control room if queue exceeds 500 persons

**Executive Summary:**
• Critical gate rerouting activated to 3 alternate gates
• Wait time drops from 35+ minutes to under 8 minutes
• Stewards deployed, medical on standby""",

    "security": """**Routing to SecurityAgent...**

[SecurityAgent] Running ticket anomaly scan via pattern analysis...
[Model Armor] Input screened — CLEAN ✓

---
**SECURITY INTELLIGENCE REPORT**

🔍 Scan Complete — **3 anomalies detected** | Risk: **HIGH**

| Ticket ID | Issue | Location |
|-----------|-------|----------|
| TKT-47821 | Duplicate scan (2nd attempt) | North Stand-A |
| TKT-83344 | Zone mismatch (wrong section) | North Stand-B |
| TKT-29107 | Revoked ticket (BCCI flagged) | North Stand-C |

**RESPONSE (radio channel 4 only — silent protocol):**
1. Dispatch plainclothes security to flagged sectors
2. Alert security chief via radio channel 4
3. Secondary bag check at North Stand entry
4. Do NOT make public PA — silent containment

**Executive Summary:**
• 3 anomalies in North Stand — HIGH risk
• Silent containment via plainclothes officers
• Police control room notified via priority line""",

    "celebration": """**Routing to EmergencyAgent...**

[EmergencyAgent] VICTORY PARADE / CELEBRATION EVENT detected — activating elevated protocol...
[EmergencyAgent] Cross-referencing Chinnaswamy Stadium 2024 incident database...
[EmergencyAgent] Retrieving crowd surge SOP from stadium operations knowledge base...

---
**⚠️ CELEBRATION EVENT — EXTREME RISK PROTOCOL**

**CHINNASWAMY 2024 INCIDENT REFERENCE:**
> *"RCB victory parade drew 100,000+ unticketted fans outside a 38,000-capacity stadium. No dynamic routing, no density monitoring, no PA dispersal system active. Result: 70+ injured in crowd surge."*

**THIS MUST NOT HAPPEN HERE. Activating all prevention protocols:**

**IMMEDIATE ACTIONS (T-0 to T+10 min):**
1. 🚨 Activate Zone-Based Crowd Routing NOW — divide perimeter into 8 sectors
2. 📢 PA every 5 minutes: *"For your safety, please move to [Zone X]. Security personnel will guide you."*
3. 🚑 Pre-position 4 medical teams at sector boundaries
4. 🚗 Lock emergency vehicle corridors — Gate 1 and Gate 6 service roads CLEAR
5. 🚔 Request immediate police deployment — minimum 200 personnel

**CAPACITY MANAGEMENT:**
- Implement fan registration via QR code at entry points
- Cap each zone at 70% of safe density
- Real-time monitoring every 60 seconds
- Auto-alert if any zone exceeds 80%

**BROADCAST MESSAGE:**
> *"Welcome to the celebration! For everyone's safety, please move to your designated zone shown on screens. Security staff are guiding crowd movement. Do not push forward — there is space for everyone."*

**DISPERSAL PLAN (post-event):**
- Phase 1: VIP exit (T+0 to T+15)
- Phase 2: Zone A/B exit via north exits (T+15 to T+30)
- Phase 3: Zone C/D via south exits (T+30 to T+45)
- Phase 4: Remaining zones (T+45 to T+60)
- Police escorts at each phase transition

**Executive Summary:**
• Chinnaswamy-class incident PREVENTED — zone routing active
• Medical pre-positioned, emergency corridors locked
• PA dispersal cycle initiated — 5-minute intervals""",

    "emergency": """**Routing to EmergencyAgent...**

[EmergencyAgent] Retrieving SOP from stadium operations knowledge base...
[EmergencyAgent] Cross-referencing incident history and weather data...

---
**CASCADE INCIDENT RESPONSE**

🚨 INCIDENT TYPE: Crowd Surge + Adverse Weather
⚠️ SEVERITY: **CRITICAL**

**IMMEDIATE ACTIONS (next 2 minutes):**
1. Activate overflow gates — full capacity
2. Open covered concourse routes — tunnel lighting ON
3. Deploy 6 stewards to crowd management positions
4. Medical team to standby at primary congestion point

**BROADCAST MESSAGE:**
> *"Attention — Gate 7 is at full capacity. Please proceed to Gates 9 and 10 for faster entry. Rain expected in 18 minutes — covered walkways now open via North Concourse."*

**FOLLOW-UP (within 15 minutes):**
- Confirm gate queue below 65% before reopening
- Deploy extra stewards to covered route access points
- Update ground staff on weather ETA via radio channel 2

**Executive Summary:**
• Cascade incident contained — overflow gates activated, covered routes open
• PA broadcast issued, medical on standby
• Weather SOP activated — all wet-weather protocols engaged""",

    "status": """**Routing to CrowdFlowAgent...**

[CrowdFlowAgent] Pulling live stadium sensor readings...

---
**STADIUM STATUS REPORT — Live**

| Metric | Value | Status |
|--------|-------|--------|
| Overall Capacity | 87% | 🟡 HIGH |
| Highest Risk Gate | G7 — 97% | 🔴 CRITICAL |
| Weather | Rain in 18 mins | 🟡 ADVISORY |
| Active Incidents | 1 surge, 1 weather | 🔴 ACTIVE |
| Threat Level | MEDIUM | 🟡 MONITOR |

**Gate Summary:**
- 🔴 Critical (>85%): G7
- 🟡 Warning (65-85%): G3, G5, G8
- 🟢 Normal (<65%): G1, G2, G4, G6, G9, G10

**Executive Summary:**
• G7 primary risk gate — immediate rerouting recommended
• 3 overflow gates available and ready
• Pre-emptive weather advisory issued""",

    "image_crowd": """**Routing to SecurityAgent + CrowdFlowAgent...**

[CrowdFlowAgent] Analyzing uploaded crowd image via Gemini Vision...
[CrowdFlowAgent] Density estimation in progress...

---
**CROWD IMAGE ANALYSIS REPORT**

📸 Image Analysis Complete — AI Vision Assessment:

**Crowd Density:** HIGH — estimated 4.2 persons/m² (danger threshold: 4.5/m²)
**Crowd Flow Direction:** Predominantly northward — gate funnel detected
**Risk Indicators Detected:**
- Bottleneck formation at image center-right
- Low lateral movement capacity
- No visible crowd management personnel in frame

**IMMEDIATE CONCERN:** Density approaching crowd crush threshold (>4.5/m²)

**RECOMMENDED ACTIONS:**
1. Deploy stewards to create lateral movement channels
2. PA announcement to slow crowd advance immediately
3. Open parallel entry route to reduce funnel pressure

**Executive Summary:**
• Image analysis shows high-density crowd approaching danger threshold
• Funnel formation detected — lateral relief channels needed urgently
• Recommend immediate intervention within 90 seconds""",

    "default": """**Routing to StadiumSentinelOrchestrator...**

[Orchestrator] Analyzing request — routing to specialist agent...
[CrowdFlowAgent] Retrieving current sensor data...

---
**STADIUM SENTINEL — OPERATIONAL RESPONSE**

All specialist agents online. Current stadium status is elevated with one critical gate.

**Active Monitoring:**
- ✅ CrowdFlowAgent: Monitoring all gates
- ✅ SecurityAgent: Ticket anomaly scanning active
- ✅ EmergencyAgent: SOPs loaded and ready
- ✅ Proactive Monitor: 30-second polling cycle active
- ✅ Model Armor: All inputs screened

Recommend checking Gate G7 queue and initiating pre-emptive rerouting to G9/G10.

**Executive Summary:**
• All systems operational — no critical incidents active
• G7 approaching warning threshold — monitoring closely
• Next proactive alert check in 25 seconds""",
}


def get_demo_response(message: str, stadium_id: str = "narendra_modi", event_type: str = "ipl_match") -> str:
    msg = (message or "").lower()

    # Celebration / victory parade — highest priority check
    if any(w in msg for w in ["celebrat", "victory", "parade", "chinnaswamy", "win", "champion", "trophy"]):
        return DEMO_RESPONSES["celebration"]

    # Image analysis
    if any(w in msg for w in ["image", "photo", "picture", "camera", "upload", "visual"]):
        return DEMO_RESPONSES["image_crowd"]

    # Cascade: crowd + weather
    if any(w in msg for w in ["surge", "gate", "crowd", "queue", "congestion", "rout"]):
        if any(w in msg for w in ["rain", "weather", "emergency", "sop", "protocol", "evacuat"]):
            return DEMO_RESPONSES["emergency"]
        if stadium_id == "narendra_modi":
            return DEMO_RESPONSES["crowd_nm"]
        return DEMO_RESPONSES["crowd"]

    if any(w in msg for w in ["security", "ticket", "suspicious", "anomal", "threat", "fraud", "duplicate"]):
        return DEMO_RESPONSES["security"]

    if any(w in msg for w in ["rain", "weather", "emergency", "fire", "medical", "sop", "evacuat", "flood"]):
        return DEMO_RESPONSES["emergency"]

    if any(w in msg for w in ["status", "current", "overall", "report", "how is", "capacity"]):
        return DEMO_RESPONSES["status"]

    return DEMO_RESPONSES["default"]
