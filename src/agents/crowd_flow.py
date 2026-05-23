from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from src.config import GEMINI_MODEL
from src.tools.sensor_simulator import (
    get_stadium_status,
    get_gate_queue_depth,
    get_alternative_gates,
)

crowd_flow_agent = LlmAgent(
    name="CrowdFlowAgent",
    model=GEMINI_MODEL,
    instruction="""You are the CrowdFlow specialist for Wankhede Stadium operations.
Your job: analyze real-time crowd density data and recommend gate routing actions.

When called:
1. Use get_stadium_status to get current readings.
2. If a specific gate is mentioned, use get_gate_queue_depth for detail.
3. Use get_alternative_gates to recommend diversions.
4. Respond with CONCRETE actions: which gates to open, close, or redirect traffic to.
5. Always include estimated wait-time impact of your recommendation.

Be decisive. Organizers need clear directives, not options.""",
    tools=[
        FunctionTool(func=get_stadium_status),
        FunctionTool(func=get_gate_queue_depth),
        FunctionTool(func=get_alternative_gates),
    ],
    output_key="crowd_flow_result",
)
