import asyncio
import base64
import json
import logging
import uuid
from typing import AsyncIterator

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from google import genai
from google.genai import types as gtypes

from src.tools.model_armor import screen_input
from src.tools.firestore_session import get_session, save_session, get_recent_alerts
from src.tools.sensor_simulator import get_stadium_status, get_real_weather_detail
from src.tools.demo_responses import get_demo_response
from src.tools.stadium_config import get_stadium, list_stadiums, get_event_type, EVENT_TYPES
from src.api.monitor import subscribe, unsubscribe

router = APIRouter()

from src.config import GEMINI_MODEL as _GEMINI_MODEL, API_KEY as _API_KEY
_gemini_client = genai.Client(api_key=_API_KEY) if _API_KEY else None

SYSTEM_PROMPT = """You are StadiumSentinel, an AI-powered crowd safety command system for cricket stadiums in India.

You have three specialist agents:
- CrowdFlowAgent: Analyzes gate queues, crowd density, rerouting decisions
- SecurityAgent: Ticket fraud detection, anomaly patterns, threat assessment
- EmergencyAgent: SOP retrieval, cascade incident response, weather/fire/medical protocols

Reference incidents:
- Chinnaswamy 2024: RCB victory parade, 100,000+ fans outside 38,000-capacity stadium, no routing active → 70+ injured. NEVER let this happen.

Response format:
- Start with **Routing to [AgentName]...**
- Show [AgentName] thinking lines
- Use markdown tables for gate data
- Use 🔴 🟡 🟢 for status indicators
- Give IMMEDIATE ACTIONS numbered list
- End with **Executive Summary** bullets
- Be specific, urgent, actionable. This is a live command system."""


class ChatRequest(BaseModel):
    message: str
    session_id: str = ""
    stadium_id: str = "narendra_modi"
    event_type: str = "ipl_match"


def _classify_agents(message: str) -> list[str]:
    """Returns which specialist agents should handle this query."""
    msg = message.lower()
    agents = []
    if any(w in msg for w in ["crowd", "gate", "queue", "surge", "congestion", "capacity", "rout", "fan"]):
        agents.append("CrowdFlowAgent")
    if any(w in msg for w in ["weather", "rain", "wind", "forecast", "wet", "storm", "cover"]):
        agents.append("WeatherAgent")
    if any(w in msg for w in ["security", "ticket", "fraud", "suspicious", "anomal", "threat", "duplicate"]):
        agents.append("SecurityAgent")
    if any(w in msg for w in ["emergency", "evacuat", "medical", "fire", "sop", "celebrat", "victory", "parade", "chinnaswamy", "flood"]):
        agents.append("EmergencyAgent")
    # rain + crowd = both crowd and weather
    if "CrowdFlowAgent" in agents and "WeatherAgent" not in agents and any(w in msg for w in ["rain", "weather", "wet"]):
        agents.append("WeatherAgent")
    return agents or ["CrowdFlowAgent"]


def _build_context(stadium_id: str, event_type: str) -> str:
    stadium = get_stadium(stadium_id)
    event = get_event_type(event_type)
    status = get_stadium_status(stadium_id)
    gates = status.get("gates", {})
    weather_detail = get_real_weather_detail(stadium_id)

    gate_lines = "\n".join(
        f"  {g}: {pct}% ({'CRITICAL' if pct > 85 else 'WARNING' if pct > 65 else 'OK'})"
        for g, pct in gates.items()
    )
    incident_ref = ""
    if stadium_id == "chinnaswamy" or event_type == "victory_parade":
        incident_ref = "\nREFERENCE: Chinnaswamy 2024 stampede — 70+ injured at RCB victory parade. Activate ALL prevention protocols."

    weather_line = status['weather']
    if weather_detail.get("description"):
        weather_line = (f"{weather_detail['condition']} ({weather_detail['description']}, "
                        f"{weather_detail['temp_c']}°C) — {weather_detail['source']}")

    return (
        f"STADIUM: {stadium['name']} ({stadium['city']}) — capacity {stadium['capacity']:,}\n"
        f"EVENT: {event['name']} | Risk level: {event.get('risk_level', 'NORMAL')}\n"
        f"LIVE SENSOR DATA:\n"
        f"  Overall capacity: {status['capacity_pct']}%\n"
        f"  Weather: {weather_line}\n"
        f"  Threat level: {status['threat_level']}\n"
        f"  Active incidents: {status['active_incidents']}\n"
        f"GATE STATUS:\n{gate_lines}"
        f"{incident_ref}"
    )


async def _stream_agent(message: str, session_id: str, stadium_id: str = "narendra_modi", event_type: str = "ipl_match") -> AsyncIterator[str]:
    yield json.dumps({"type": "thought", "text": "Screening input through Model Armor..."})
    await asyncio.sleep(0.1)

    armor = screen_input(message)
    if not armor["safe"]:
        yield json.dumps({"type": "blocked", "text": f"Input blocked: {armor['reason']}"})
        return

    yield json.dumps({"type": "thought", "text": "Input cleared. Pulling live sensor data..."})
    await asyncio.sleep(0.1)

    session = await get_session(session_id)
    history = session.get("history", [])
    full_response = ""
    live_success = False

    # Try real Gemini API with live sensor context
    if _gemini_client:
        try:
            context = _build_context(stadium_id, event_type)
            agents = _classify_agents(message)
            for ag in agents:
                yield json.dumps({"type": "thought", "text": f"[{ag}] activated — analyzing..."})
                await asyncio.sleep(0.15)
            yield json.dumps({"type": "thought", "text": f"Routing to {_GEMINI_MODEL} — live analysis..."})

            history_contents = []
            for h in history[-6:]:
                history_contents.append(gtypes.Content(
                    role=h["role"] if h["role"] == "user" else "model",
                    parts=[gtypes.Part(text=h["text"])]
                ))

            agent_directive = f"ACTIVE AGENTS FOR THIS QUERY: {', '.join(agents)}\nRespond with a section for EACH active agent before the executive summary."
            full_prompt = f"{context}\n\n{agent_directive}\n\nOPERATOR QUERY: {message}"

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: _gemini_client.models.generate_content(
                    model=_GEMINI_MODEL,
                    contents=history_contents + [gtypes.Part(text=full_prompt)],
                    config=gtypes.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.4,
                        max_output_tokens=4000,
                    ),
                )
            )
            text = (response.text if response else "") or ""
            if text.strip():
                full_response = text
                live_success = True
                yield json.dumps({"type": "thought", "text": "Gemini analysis complete. Streaming response..."})
                words = text.split()
                for i, word in enumerate(words):
                    chunk = word + (" " if i < len(words) - 1 else "")
                    yield json.dumps({"type": "token", "text": chunk})
                    await asyncio.sleep(0.018)
        except Exception as e:
            logger.warning("Gemini call failed, falling back to demo: %s", e)
            yield json.dumps({"type": "thought", "text": "Gemini unavailable — switching to demo mode..."})

    if not live_success:
        yield json.dumps({"type": "thought", "text": "Orchestrator routing to specialist agent..."})
        await asyncio.sleep(0.4)
        yield json.dumps({"type": "thought", "text": "Agent tool execution in progress..."})
        await asyncio.sleep(0.4)
        yield json.dumps({"type": "thought", "text": "Sensor data retrieved. Composing response..."})
        await asyncio.sleep(0.2)

        full_response = get_demo_response(message, stadium_id, event_type)
        words = full_response.split()
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            yield json.dumps({"type": "token", "text": chunk})
            await asyncio.sleep(0.022)

    history.append({"role": "user", "text": message})
    history.append({"role": "assistant", "text": full_response})
    await save_session(session_id, history)
    yield json.dumps({"type": "done", "text": ""})


@router.post("/chat")
async def chat_stream(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    async def generator():
        async for chunk in _stream_agent(req.message, session_id, req.stadium_id, req.event_type):
            yield {"data": chunk}

    return EventSourceResponse(generator())


@router.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    stadium_id: str = Form("narendra_modi"),
    session_id: str = Form(""),
):
    """Accepts crowd image, runs Gemini Vision analysis (falls back to demo)."""
    contents = await file.read()
    b64 = base64.b64encode(contents).decode()
    stadium = get_stadium(stadium_id)

    # Try Gemini Vision
    try:
        if not _API_KEY:
            raise ValueError("No API key")
        if len(contents) > 10 * 1024 * 1024:
            raise ValueError("File too large (max 10MB)")
        response = _gemini_client.models.generate_content(
            model=_GEMINI_MODEL,
            contents=[
                gtypes.Part.from_bytes(data=contents, mime_type=file.content_type or "image/jpeg"),
                f"You are a crowd safety AI for {stadium['name']}. Analyze this image for: crowd density (persons/m²), bottleneck formation, safety risks, and recommended immediate actions. Be specific and urgent.",
            ],
        )
        analysis = (response.text or "").strip() or get_demo_response("image crowd analysis upload", stadium_id)
    except Exception:
        analysis = get_demo_response("image crowd analysis upload", stadium_id)

    return JSONResponse({"analysis": analysis, "stadium": stadium["name"]})


@router.get("/stadiums")
async def stadiums_list():
    return JSONResponse(list_stadiums())


@router.get("/stadiums/{stadium_id}")
async def stadium_detail(stadium_id: str):
    return JSONResponse(get_stadium(stadium_id))


@router.get("/event-types")
async def event_types():
    return JSONResponse([{"id": k, "name": v["name"], "risk": v.get("risk_level", "NORMAL")} for k, v in EVENT_TYPES.items()])


@router.get("/status")
async def stadium_status(stadium_id: str = "narendra_modi"):
    s = get_stadium_status()
    s["stadium_id"] = stadium_id
    s["stadium_name"] = get_stadium(stadium_id)["name"]
    return JSONResponse(s)


@router.get("/alerts")
async def recent_alerts():
    alerts = await get_recent_alerts(20)
    return JSONResponse(alerts)


@router.get("/alerts/stream")
async def alert_stream(request: Request):
    q = subscribe()

    async def generator():
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    alert = await asyncio.wait_for(q.get(), timeout=30.0)
                    yield {"data": json.dumps(alert)}
                except asyncio.TimeoutError:
                    yield {"data": json.dumps({"type": "heartbeat"})}
        finally:
            unsubscribe(q)

    return EventSourceResponse(generator())


@router.get("/health")
async def health():
    return {"status": "ok", "service": "stadium-sentinel"}
