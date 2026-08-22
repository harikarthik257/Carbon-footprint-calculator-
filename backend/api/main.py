import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import footprint, meal, recommend, leaderboard, benchmark

app = FastAPI(title="Urban Carbon Footprint Calculator API")

# Wide open for local dev speed — tighten before anything but a demo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(footprint.router, prefix="/api", tags=["footprint"])
app.include_router(meal.router, prefix="/api", tags=["meal"])
app.include_router(recommend.router, prefix="/api", tags=["recommend"])
app.include_router(leaderboard.router, prefix="/api", tags=["leaderboard"])
app.include_router(benchmark.router, prefix="/api", tags=["benchmark"])


@app.get("/api/health")
def health():
    import os as _os
    return {
        "status": "ok",
        "mock_ai": not bool(_os.environ.get("GEMINI_API_KEY")) or _os.environ.get("MOCK_AI", "").lower() == "true",
    }
