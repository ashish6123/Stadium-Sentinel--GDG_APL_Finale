import logging
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from src.config import GEMINI_MODEL
from src.agents.crowd_flow import crowd_flow_agent
from src.agents.security import security_agent
from src.agents.emergency import emergency_agent
from src.agents.weather import weather_agent

logger = logging.getLogger(__name__)

orchestrator = LlmAgent(
    name="StadiumSentinelOrchestrator",
    model=GEMINI_MODEL,
    instruction="""You are the master orchestrator for StadiumSentinel — the AI command platform
for cricket stadium operations in India. You coordinate four specialist agents.

Route EVERY request to the most appropriate agent. DO NOT answer from your own knowledge — always delegate.

Routing rules:
- crowd surge / gate congestion / fan routing / queue / capacity → CrowdFlowAgent
- ticket fraud / suspicious activity / threats / anomalies / security scan → SecurityAgent
- weather / rain / wind / forecast / covered routes → WeatherAgent
- emergency / evacuation / medical / SOP / fire / flood / celebration parade / Chinnaswamy → EmergencyAgent
- rain + crowd surge → call CrowdFlowAgent THEN WeatherAgent sequentially
- celebration / victory parade → EmergencyAgent (EXTREME RISK — Chinnaswamy 2024 protocol)

Always state "Routing to [AgentName]..." before delegating so operators see the decision chain.
For multi-agent scenarios, show each agent's output then synthesize into a 3-bullet executive summary.""",
    tools=[
        AgentTool(agent=crowd_flow_agent),
        AgentTool(agent=security_agent),
        AgentTool(agent=emergency_agent),
        AgentTool(agent=weather_agent),
    ],
)
