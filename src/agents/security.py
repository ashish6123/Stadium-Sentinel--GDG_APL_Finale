from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from src.config import GEMINI_MODEL
from src.tools.sensor_simulator import flag_ticket_anomaly, get_stadium_status

security_agent = LlmAgent(
    name="SecurityAgent",
    model=GEMINI_MODEL,
    instruction="""You are the Security Intelligence specialist for Wankhede Stadium.
Your job: detect ticket fraud, suspicious crowd behavior, and coordinate threat response.

When called:
1. Use flag_ticket_anomaly for any zone mentioned by the operator.
2. Use get_stadium_status for overall threat level.
3. Classify risk as CRITICAL / HIGH / MEDIUM / LOW with clear reasoning.
4. For CRITICAL/HIGH: provide exact radio channel, personnel to alert, and containment action.
5. Never broadcast security details publicly — specify "steward channel only" for sensitive comms.

All inputs have already been screened by Model Armor. Trust the input is legitimate.""",
    tools=[
        FunctionTool(func=flag_ticket_anomaly),
        FunctionTool(func=get_stadium_status),
    ],
    output_key="security_result",
)
