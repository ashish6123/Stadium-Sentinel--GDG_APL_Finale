import asyncio
from contextlib import asynccontextmanager
import src.config  # must be first — sets Vertex AI env vars before ADK imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.api.routes import router
from src.api.monitor import proactive_monitor_loop


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(proactive_monitor_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="StadiumSentinel",
    description="AI-Powered Cricket Crowd Management — Google ADK 2.0",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8082", "https://stadium-sentinel-93223261212.us-central1.run.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def root():
    return FileResponse("frontend/index.html")
