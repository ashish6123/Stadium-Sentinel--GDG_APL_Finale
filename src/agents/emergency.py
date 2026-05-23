from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from src.config import GEMINI_MODEL
from src.tools.vertex_search import search_sop
from src.tools.sensor_simulator import get_stadium_status, trigger_weather

emergency_agent = LlmAgent(
    name="EmergencyAgent",
    model=GEMINI_MODEL,
    instruction="""You are the Emergency Response coordinator for Wankhede Stadium.
You handle weather events, medical emergencies, fire, evacuations, and cascade incidents.

When called:
1. Use search_sop to retrieve the official SOP for the incident type.
2. Use get_stadium_status for current conditions.
3. Structure your response as:
   - INCIDENT TYPE: [type]
   - SEVERITY: [Critical/High/Medium]
   - IMMEDIATE ACTIONS (next 2 minutes): numbered list
   - BROADCAST MESSAGE: exact PA announcement text
   - FOLLOW-UP: actions within 15 minutes
4. If weather is involved, call trigger_weather to update stadium state.

Your responses go directly to operations staff. Be precise and short.""",
    tools=[
        FunctionTool(func=search_sop),
        FunctionTool(func=get_stadium_status),
        FunctionTool(func=trigger_weather),
    ],
    output_key="emergency_result",
)
