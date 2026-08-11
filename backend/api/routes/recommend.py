from fastapi import APIRouter
from pydantic import BaseModel

from engine.claude_client import generate_recommendation

router = APIRouter()


class RecommendRequest(BaseModel):
    total_kg_co2e: float
    by_category: dict[str, float]


class Strategy(BaseModel):
    action: str
    estimated_savings_kg_co2e_per_day: float


class RecommendResponse(BaseModel):
    strategies: list[Strategy]
    is_mock: bool


@router.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    breakdown = {"total_kg_co2e": req.total_kg_co2e, "by_category": req.by_category}
    return generate_recommendation(breakdown)
