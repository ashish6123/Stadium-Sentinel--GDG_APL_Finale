# StadiumSentinel — AI Crowd Command Platform

> **"On 18 May 2024, 70 people were injured outside Chinnaswamy Stadium because nobody had a system that could say — in real time — where the crowd was building and what to do about it. StadiumSentinel is that system."**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Cloud%20Run-4285F4?style=for-the-badge&logo=google-cloud)](https://stadium-sentinel-93223261212.us-central1.run.app)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-2.0-34A853?style=for-the-badge)](https://google.github.io/adk-docs/)
[![Gemini](https://img.shields.io/badge/Gemini-3.5%20Flash-EA4335?style=for-the-badge)](https://ai.google.dev/)
[![Cloud Run](https://img.shields.io/badge/Cloud%20Run-Deployed-FBBC04?style=for-the-badge&logo=google-cloud)](https://cloud.google.com/run)

---

## The Problem

India's cricket stadiums host 66,000–132,000 fans per match. When something goes wrong — a gate surge, sudden rain, a suspicious ticket cluster, or a post-match celebration — the operations team gets calls from 10 different radio channels, checks spreadsheets, and tries to make a decision manually. It takes 15 minutes. By then, people are already crushed against barriers.

**The Chinnaswamy 2024 incident is proof this gap is real and deadly.**

---

## The Solution

StadiumSentinel is an **AI-powered crowd safety command platform** that gives stadium operations directors a single interface to monitor, analyze, and act — in real time — across every gate, every section, every incident type.

One command. Four specialist AI agents. Immediate, specific, actionable response.

---

## Architecture

```
Operator Query
      │
      ▼
┌─────────────────┐     ┌──────────────────┐
│  Model Armor    │────▶│  Query Classifier │
│  (Input Safety) │     │  (Agent Router)   │
└─────────────────┘     └────────┬─────────┘
                                 │
              ┌──────────────────┼──────────────────┬──────────────────┐
              ▼                  ▼                   ▼                  ▼
   ┌─────────────────┐  ┌──────────────┐  ┌───────────────┐  ┌──────────────────┐
   │ CrowdFlowAgent  │  │ WeatherAgent │  │ SecurityAgent │  │ EmergencyAgent   │
   │                 │  │              │  │               │  │                  │
   │ Gate congestion │  │ Live weather │  │ Ticket fraud  │  │ SOP retrieval    │
   │ Rerouting logic │  │ Rain routing │  │ Anomaly scan  │  │ Evacuation plans │
   │ Density analysis│  │ Covered gates│  │ Threat scoring│  │ Chinnaswamy SOP  │
   └────────┬────────┘  └──────┬───────┘  └───────┬───────┘  └────────┬─────────┘
            └──────────────────┴───────────────────┴───────────────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   Gemini 3.5 Flash   │
                              │  (Response Synthesis) │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   SSE Stream to UI   │
                              │  + Voice Alert (TTS) │
                              └─────────────────────┘
```

### Proactive Monitor Loop
A background asyncio task polls sensor data every 30 seconds **without any user input** and fires cascade alerts automatically — the key differentiator from every generic chatbot.

---

## Google AI & GCP Stack

| Service | Usage |
|---------|-------|
| **Gemini 3.5 Flash** | Core AI reasoning — analyzes queries with live sensor context |
| **Google ADK 2.0** | Multi-agent orchestration — 4 specialist agents via `AgentTool` |
| **Google Model Armor** | Input safety screening — blocks prompt injection before it hits Gemini |
| **Vertex AI Search** | RAG — retrieves stadium emergency SOPs from seeded knowledge base |
| **Google Cloud Firestore** | Session persistence — chat history and alert log storage |
| **Cloud Run** | Serverless deployment — stateless, auto-scaling |
| **Cloud Build** | CI/CD — container build pipeline via `cloudbuild.yaml` |
| **OpenWeatherMap** | Real-time weather at stadium GPS coordinates |

---

## Key Features

### Multi-Agent Routing
Every query is classified and routed to the appropriate specialist agent(s). Rain + surge queries activate **both** CrowdFlowAgent and WeatherAgent simultaneously, with each agent's output shown in the thought log.

### Real-Time Sensor Data with Spatial Propagation
Gates have an adjacency map — a surge at G7 automatically propagates pressure to G6 and G8. Rain triggers increased load on covered gates only. This models real crowd flow dynamics, not random noise.

### Real Weather Integration
Live weather pulled from OpenWeatherMap every 5 minutes for the selected stadium's GPS coordinates. Ahmedabad, Mumbai, Bengaluru, and Kolkata all wired in.

### Chinnaswamy 2024 Prevention Protocol
Victory parade / celebration events trigger an EXTREME RISK protocol referencing the real 2024 incident — with zone-routing, 5-minute PA intervals, and emergency corridor lockdown instructions.

### Proactive Alerts Without User Input
The system fires cascade alerts autonomously. Wait 20 seconds after loading — Gate G7 + rain triggers a live alert with no user prompt.

### Voice Broadcast
Web Speech API reads critical alerts aloud. Zero API cost. Toggle in top-right corner.

### Image Analysis
Upload a crowd photo → Gemini Vision estimates density (persons/m²), detects bottleneck formation, recommends immediate actions.

---

## Stadiums Supported

| Stadium | City | Capacity |
|---------|------|----------|
| Narendra Modi Stadium | Ahmedabad | 1,32,000 |
| Wankhede Stadium | Mumbai | 33,108 |
| M. Chinnaswamy Stadium | Bengaluru | 38,000 |
| Eden Gardens | Kolkata | 66,000 |

---

## Happy Path Demo Script

### Scenario 1 — Cascade Incident (Rain + Surge)
```
"Gate 7 is overcrowded and rain is coming in 20 minutes, what's the protocol?"
```
CrowdFlowAgent + WeatherAgent both activate. Gate rerouting + covered-route advisory issued.

### Scenario 2 — Victory Parade (Chinnaswamy Prevention)
```
"We have a victory parade outside with 50,000 fans gathered"
```
EmergencyAgent activates EXTREME RISK protocol. References Chinnaswamy 2024. Zone routing + PA intervals issued.

### Scenario 3 — Security Anomaly
```
"Run a ticket anomaly scan on the North Stand"
```
SecurityAgent detects duplicate/revoked tickets. Silent plainclothes response protocol issued.

### Scenario 4 — Proactive Alert (No Input Required)
Wait 20–30 seconds without typing. System autonomously detects Gate G7 surge + rain and fires a live cascade alert.

---

## Project Structure

```
stadium-sentinel/
├── src/
│   ├── main.py                  # FastAPI app + lifespan
│   ├── config.py                # Single source of truth for all env config
│   ├── agents/
│   │   ├── orchestrator.py      # Master ADK orchestrator
│   │   ├── crowd_flow.py        # Gate congestion specialist
│   │   ├── security.py          # Ticket fraud specialist
│   │   ├── emergency.py         # SOP + evacuation specialist
│   │   └── weather.py           # Weather impact specialist
│   ├── api/
│   │   ├── routes.py            # FastAPI endpoints + SSE streaming
│   │   └── monitor.py           # Proactive background alert loop
│   └── tools/
│       ├── sensor_simulator.py  # Spatial gate model with adjacency propagation
│       ├── stadium_config.py    # Real data for 4 Indian stadiums
│       ├── vertex_search.py     # Vertex AI Search RAG + local fallback
│       ├── firestore_session.py # Async Firestore session management
│       ├── model_armor.py       # Input safety screening
│       └── demo_responses.py    # Scripted fallback (bulletproof demo)
├── frontend/
│   └── index.html               # Single-file ops-center UI
├── data/
│   └── stadium_sops.json        # 6 SOPs seeded into Vertex AI Search
├── Dockerfile                   # Cloud Run optimized
├── cloudbuild.yaml              # CI/CD pipeline
├── setup_vertex.py              # One-time Vertex AI Search seeding script
└── requirements.txt
```

---

## Local Setup

```bash
git clone https://github.com/ashish6123/stadium-sentinel
cd stadium-sentinel
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create `.env`:
```env
GOOGLE_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_key
GCP_PROJECT_ID=your_gcp_project
GCP_LOCATION=us-central1
GEMINI_MODEL=gemini-3.5-flash
```

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

Open `http://localhost:8080`

---

## GCP Deployment

```bash
gcloud run deploy stadium-sentinel \
  --source . \
  --project YOUR_PROJECT_ID \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --set-env-vars "GOOGLE_API_KEY=...,GEMINI_MODEL=gemini-3.5-flash,GCP_PROJECT_ID=..."
```

---

## Scalability & Security

- **Stateless Cloud Run** — horizontal auto-scaling, no shared state between instances
- **Firestore** — persistent session and alert storage survives instance restarts
- **Model Armor** — every input screened before reaching Gemini
- **DOMPurify** — all AI responses sanitized before rendering (XSS prevention)
- **No secrets in code** — all keys via environment variables, `.env` gitignored
- **File upload validation** — 10MB size limit, MIME type checked on image analysis
- **Graceful fallback** — demo_responses.py ensures happy path works even if all APIs are down

---

## Why StadiumSentinel Wins

| Differentiator | Others | StadiumSentinel |
|---|---|---|
| Proactive alerts | User must ask | Fires autonomously every 30s |
| Multi-agent routing | Single LLM call | 4 specialist agents, classified per query |
| Sensor realism | Random data | Adjacency propagation, rain affects covered gates only |
| Real-world anchor | Generic demo | Chinnaswamy 2024 — real incident, real prevention |
| Weather | Hardcoded | Live OpenWeatherMap at stadium GPS coordinates |
| Demo resilience | Breaks if API down | Scripted fallback for every scenario |

---

*Built for Google Cloud Agentic Premier League National Finale 2026*  
*Stack: Google ADK 2.0 · Gemini 3.5 Flash · Vertex AI Search · Model Armor · Firestore · Cloud Run*
