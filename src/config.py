import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "gdg-apl-finale")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
VERTEX_SEARCH_APP_ID = os.getenv("VERTEX_SEARCH_APP_ID", "stadium-sop-search")
FIRESTORE_DATABASE = os.getenv("FIRESTORE_DATABASE", "(default)")

VERTEX_SEARCH_SERVING_CONFIG = (
    f"projects/{PROJECT_ID}/locations/global/collections/default_collection"
    f"/engines/{VERTEX_SEARCH_APP_ID}/servingConfigs/default_config"
)

APP_NAME = "stadium-sentinel"

# ADK routing: use Gemini API key if set, else Vertex AI
API_KEY = os.getenv("GOOGLE_API_KEY", "")
_api_key = API_KEY  # backward compat
if _api_key:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
    os.environ["GOOGLE_API_KEY"] = _api_key
else:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
