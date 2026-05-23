from google.cloud import discoveryengine_v1 as discoveryengine
from src.config import PROJECT_ID, VERTEX_SEARCH_SERVING_CONFIG

_client: discoveryengine.SearchServiceClient | None = None


def _get_client() -> discoveryengine.SearchServiceClient:
    global _client
    if _client is None:
        _client = discoveryengine.SearchServiceClient()
    return _client


_FALLBACK_SOPS = {
    "crowd surge": (
        "CROWD SURGE SOP: 1) Activate overflow gates immediately. "
        "2) Deploy crowd management stewards to affected zone. "
        "3) Broadcast PA announcement directing fans to alternate gates. "
        "4) Alert medical team to standby. 5) Notify local police control room."
    ),
    "rain": (
        "WET WEATHER SOP: 1) Open covered concourse routes. "
        "2) Issue advisory for slippery surfaces. "
        "3) Deploy extra stewards at ramp access points. "
        "4) Pause open-air food vendor operations. "
        "5) Ensure drainage channels are clear."
    ),
    "security threat": (
        "SECURITY THREAT SOP: 1) Isolate the flagged sector. "
        "2) Alert stadium security chief and local police. "
        "3) Do not broadcast publicly — use steward radio channel 4. "
        "4) Initiate bag re-check at nearest gate. "
        "5) Document incident in security log system."
    ),
    "fire": (
        "FIRE EMERGENCY SOP: 1) Trigger zone evacuation immediately. "
        "2) Activate PA evacuation message. "
        "3) Direct fans to nearest exit — avoid lifts. "
        "4) Fire marshal to coordinate with BFES team. "
        "5) Suspend match and inform match officials."
    ),
    "medical": (
        "MEDICAL EMERGENCY SOP: 1) Dispatch medical team to location. "
        "2) Clear 10-meter radius around patient. "
        "3) Request AED unit from nearest first aid post. "
        "4) Do not move patient unless immediate hazard. "
        "5) Coordinate ambulance access via Gate 1 service road."
    ),
}


def search_sop(query: str) -> str:
    """Retrieves relevant stadium SOP from Vertex AI Search. Falls back to local SOPs."""
    try:
        client = _get_client()
        request = discoveryengine.SearchRequest(
            serving_config=VERTEX_SEARCH_SERVING_CONFIG,
            query=query,
            page_size=3,
        )
        response = client.search(request)
        results = []
        for r in response.results:
            doc = r.document.derived_struct_data
            snippet = doc.get("snippets", [{}])[0].get("snippet", "")
            if snippet:
                results.append(snippet)
        if results:
            return "\n\n".join(results)
    except Exception:
        pass

    # Local fallback — always works
    query_lower = query.lower()
    for keyword, sop in _FALLBACK_SOPS.items():
        if keyword in query_lower:
            return sop
    return _FALLBACK_SOPS["crowd surge"]
