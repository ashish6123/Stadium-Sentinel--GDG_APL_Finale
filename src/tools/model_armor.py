import httpx
import google.auth
import google.auth.transport.requests
from src.config import PROJECT_ID, LOCATION

_ENDPOINT = (
    f"https://modelarmor.{LOCATION}.rep.googleapis.com/v1"
    f"/projects/{PROJECT_ID}/locations/{LOCATION}/templates/default:sanitizeUserPrompt"
)

_BLOCKED_PATTERNS = [
    "ignore previous", "forget instructions", "jailbreak",
    "act as", "pretend you", "DAN mode", "disregard",
]


def _get_token() -> str:
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token


def screen_input(user_input: str) -> dict:
    """
    Screens user input through Model Armor.
    Falls back to local heuristic if API unavailable.
    Returns {"safe": bool, "reason": str, "sanitized": str}
    """
    lower = user_input.lower()
    for pattern in _BLOCKED_PATTERNS:
        if pattern in lower:
            return {
                "safe": False,
                "reason": f"Prompt injection pattern detected: '{pattern}'",
                "sanitized": "",
            }

    try:
        token = _get_token()
        resp = httpx.post(
            _ENDPOINT,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"userPromptData": {"text": user_input}},
            timeout=5.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            violations = data.get("sanitizationResult", {}).get("filterMatchState", "NO_MATCH_FOUND")
            if violations != "NO_MATCH_FOUND":
                return {"safe": False, "reason": f"Model Armor blocked: {violations}", "sanitized": ""}
    except Exception:
        pass  # fallback to local check — already passed above

    return {"safe": True, "reason": "clean", "sanitized": user_input}
