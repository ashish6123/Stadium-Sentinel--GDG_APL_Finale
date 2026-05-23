import time
from google.cloud import firestore
from src.config import FIRESTORE_DATABASE

_db: firestore.AsyncClient | None = None


def _get_db() -> firestore.AsyncClient:
    global _db
    if _db is None:
        _db = firestore.AsyncClient(database=FIRESTORE_DATABASE)
    return _db


async def get_session(session_id: str) -> dict:
    try:
        db = _get_db()
        doc = await db.collection("sessions").document(session_id).get()
        return doc.to_dict() or {"history": [], "summary": "", "created_at": time.time()}
    except Exception:
        return {"history": [], "summary": "", "created_at": time.time()}


async def save_session(session_id: str, history: list, summary: str = "") -> None:
    try:
        db = _get_db()
        await db.collection("sessions").document(session_id).set({
            "history": history[-10:],  # keep last 10 turns only
            "summary": summary,
            "updated_at": time.time(),
        }, merge=True)
    except Exception:
        pass


async def push_alert(alert: dict) -> str:
    """Stores a proactive alert to Firestore. Returns alert ID."""
    try:
        db = _get_db()
        alert["ts"] = time.time()
        ref = db.collection("alerts").document()
        await ref.set(alert)
        return ref.id
    except Exception:
        return "local"


async def get_recent_alerts(limit: int = 20) -> list[dict]:
    try:
        db = _get_db()
        docs = (
            db.collection("alerts")
            .order_by("ts", direction=firestore.Query.DESCENDING)
            .limit(limit)
        )
        results = []
        async for doc in docs.stream():
            d = doc.to_dict()
            d["id"] = doc.id
            results.append(d)
        return results
    except Exception:
        return []
