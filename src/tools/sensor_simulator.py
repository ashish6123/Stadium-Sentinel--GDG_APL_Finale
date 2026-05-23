import os
import random
import time
import threading
import urllib.request
import json
from typing import Any

GATES = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"]
ZONES = ["North Stand", "South Stand", "East Pavilion", "West Pavilion", "VIP Box"]

# Adjacency map — gates that share physical corridors/concourses
# Surge at one gate bleeds pressure to its neighbours
GATE_ADJACENCY: dict[str, list[str]] = {
    "G1":  ["G2", "G10"],
    "G2":  ["G1", "G3"],
    "G3":  ["G2", "G4"],
    "G4":  ["G3", "G5"],
    "G5":  ["G4", "G6"],
    "G6":  ["G5", "G7"],
    "G7":  ["G6", "G8"],
    "G8":  ["G7", "G9"],
    "G9":  ["G8", "G10"],
    "G10": ["G9", "G1"],
}

# Gates with covered concourse access (rain changes fan routing)
COVERED_GATES = {"G1", "G2", "G6", "G7"}

# Stadium GPS coords — Narendra Modi Stadium, Ahmedabad
_STADIUM_COORDS = {"narendra_modi": (23.0925, 72.5311), "wankhede": (18.9388, 72.8258),
                   "chinnaswamy": (12.9788, 77.5996), "eden_gardens": (22.5645, 88.3433)}

_state: dict[str, Any] = {
    "capacity_pct": 78,
    "gates": {g: random.randint(20, 70) for g in GATES},
    "weather": "clear",
    "threat_level": "low",
    "incidents": [],
}


_weather_cache: dict = {}
_weather_lock = threading.Lock()


def _fetch_real_weather(stadium_id: str = "narendra_modi") -> str:
    """Fetches real weather from OpenWeatherMap. Returns condition string."""
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        return ""
    coords = _STADIUM_COORDS.get(stadium_id, _STADIUM_COORDS["narendra_modi"])
    cache_key = stadium_id
    now = time.time()
    with _weather_lock:
        cached = _weather_cache.get(cache_key)
        if cached and now - cached["ts"] < 300:  # 5-min cache
            return cached["condition"]
    try:
        url = (f"https://api.openweathermap.org/data/2.5/weather"
               f"?lat={coords[0]}&lon={coords[1]}&appid={api_key}&units=metric")
        with urllib.request.urlopen(url, timeout=4) as resp:
            data = json.loads(resp.read())
        main = data["weather"][0]["main"].lower()
        condition = ("rain" if "rain" in main or "drizzle" in main
                     else "thunderstorm" if "thunder" in main
                     else "clear")
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        with _weather_lock:
            _weather_cache[cache_key] = {"condition": condition, "ts": now,
                                          "desc": desc, "temp": temp}
        return condition
    except Exception:
        return ""


def get_real_weather_detail(stadium_id: str = "narendra_modi") -> dict:
    """Returns full weather detail for context injection."""
    with _weather_lock:
        cached = _weather_cache.get(stadium_id, {})
    return {
        "condition": cached.get("condition", _state["weather"]),
        "description": cached.get("desc", ""),
        "temp_c": cached.get("temp", ""),
        "source": "OpenWeatherMap (live)" if cached else "simulator",
    }


def get_stadium_status(stadium_id: str = "narendra_modi") -> dict[str, Any]:
    """Returns current simulated stadium sensor readings with spatial propagation."""
    # Sync real weather
    real_weather = _fetch_real_weather(stadium_id)
    if real_weather:
        _state["weather"] = real_weather

    _state["capacity_pct"] = min(99, _state["capacity_pct"] + random.randint(-1, 2))

    # Natural drift — small random walk per gate
    for g in GATES:
        drift = random.randint(-4, 6)
        _state["gates"][g] = max(0, min(100, _state["gates"][g] + drift))

    # Rain effect: fans avoid open gates, pressure builds at covered gates
    if _state["weather"] in ("rain", "heavy_rain"):
        for g in COVERED_GATES:
            _state["gates"][g] = min(100, _state["gates"][g] + random.randint(2, 6))

    # Adjacency propagation: congested gates push pressure to neighbours
    snapshot = dict(_state["gates"])
    for g, pct in snapshot.items():
        if pct > 80:
            for neighbour in GATE_ADJACENCY[g]:
                bleed = int((pct - 80) * 0.15)
                _state["gates"][neighbour] = min(100, _state["gates"][neighbour] + bleed)

    # Derive threat level from gate state
    critical_count = sum(1 for v in _state["gates"].values() if v > 85)
    if critical_count >= 3:
        _state["threat_level"] = "high"
    elif critical_count >= 1:
        _state["threat_level"] = "medium"
    else:
        _state["threat_level"] = "low"

    return {
        "timestamp": int(time.time()),
        "capacity_pct": _state["capacity_pct"],
        "gates": dict(_state["gates"]),
        "weather": _state["weather"],
        "threat_level": _state["threat_level"],
        "active_incidents": len(_state["incidents"]),
    }


def trigger_surge(gate: str) -> dict:
    """Simulates a sudden crowd surge at a specific gate with adjacency propagation."""
    _state["gates"][gate] = 97
    # Immediate pressure on adjacent gates
    for neighbour in GATE_ADJACENCY.get(gate, []):
        _state["gates"][neighbour] = min(100, _state["gates"][neighbour] + random.randint(10, 20))
    _state["incidents"].append({"type": "surge", "gate": gate, "ts": int(time.time())})
    return {"status": "surge triggered", "gate": gate, "adjacent_pressure": GATE_ADJACENCY.get(gate, [])}


def trigger_weather(condition: str) -> dict:
    """Updates weather state. Rain increases load on covered gates automatically."""
    _state["weather"] = condition
    return {"status": "updated", "weather": condition}


def get_gate_queue_depth(gate: str) -> dict[str, Any]:
    """Returns queue depth, wait time, and adjacency context for a specific gate."""
    depth = _state["gates"].get(gate, 50)
    wait_mins = max(1, int(depth * 0.4))
    status = "critical" if depth > 85 else "warning" if depth > 65 else "normal"
    neighbour_loads = {n: _state["gates"].get(n, 0) for n in GATE_ADJACENCY.get(gate, [])}
    return {
        "gate": gate,
        "queue_pct": depth,
        "wait_mins": wait_mins,
        "status": status,
        "adjacent_gates": neighbour_loads,
        "covered": gate in COVERED_GATES,
    }


def get_alternative_gates(congested_gate: str) -> dict[str, Any]:
    """Returns top 3 least-congested non-adjacent alternative gates."""
    adjacent = set(GATE_ADJACENCY.get(congested_gate, []))
    others = {g: v for g, v in _state["gates"].items()
              if g != congested_gate and g not in adjacent}
    sorted_gates = sorted(others.items(), key=lambda x: x[1])[:3]
    return {
        "congested": congested_gate,
        "alternatives": [{"gate": g, "queue_pct": v, "covered": g in COVERED_GATES}
                         for g, v in sorted_gates],
    }


def flag_ticket_anomaly(zone: str) -> dict[str, Any]:
    """Scans for suspicious ticket clusters in a zone."""
    anomaly_count = random.randint(0, 4)
    anomalies = [
        {
            "ticket_id": f"TKT-{random.randint(10000, 99999)}",
            "issue": random.choice(["duplicate_scan", "zone_mismatch", "revoked"]),
            "sector": f"{zone}-Sector-{random.choice(['A', 'B', 'C'])}",
        }
        for _ in range(anomaly_count)
    ]
    return {
        "zone": zone,
        "anomaly_count": anomaly_count,
        "anomalies": anomalies,
        "risk": "high" if anomaly_count >= 3 else "medium" if anomaly_count >= 1 else "none",
    }
