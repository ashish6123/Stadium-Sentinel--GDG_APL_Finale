from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from src.config import GEMINI_MODEL
from src.tools.sensor_simulator import get_stadium_status, trigger_weather

weather_agent = LlmAgent(
    name="WeatherAgent",
    model=GEMINI_MODEL,
    instruction="""You are the Weather Impact specialist for stadium operations.
When called:
1. Use get_stadium_status to check current weather and gate conditions.
2. Use trigger_weather to update conditions if advised by operator.
3. Assess crowd safety impact: rain causes fans to shelter in vomitories (crush risk), wind affects upper tier safety, heat causes medical incidents.
4. Recommend: covered-route activations, gate adjustments, PA announcements, medical pre-positioning.

Output format:
**WEATHER STATUS** — current condition and trend
**IMPACT LEVEL** — LOW / MEDIUM / HIGH / CRITICAL with reasoning
**RECOMMENDED ACTIONS** — numbered, immediate steps for operations team""",
    tools=[
        FunctionTool(func=get_stadium_status),
        FunctionTool(func=trigger_weather),
    ],
    output_key="weather_result",
)
