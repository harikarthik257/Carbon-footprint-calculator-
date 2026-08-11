from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from engine.calculator import calculate_daily_footprint

router = APIRouter()


class TransportInput(BaseModel):
    mode: Optional[str] = None
    km_per_day: float = 0


class EnergyInput(BaseModel):
    kwh_per_day: float = 0
    grid: str = "national"


class FoodInput(BaseModel):
    plant_meals_per_day: int = 0
    meat_meals_per_day: int = 0


class WasteInput(BaseModel):
    landfill_kg_per_day: float = 0
    composted_kg_per_day: float = 0
    recycled_kg_per_day: float = 0


class CalculateRequest(BaseModel):
    transport: Optional[TransportInput] = None
    energy: Optional[EnergyInput] = None
    food: Optional[FoodInput] = None
    waste: Optional[WasteInput] = None


@router.post("/calculate")
def calculate(req: CalculateRequest):
    onboarding = {
        "transport": req.transport.dict() if req.transport else {},
        "energy": req.energy.dict() if req.energy else {},
        "food": req.food.dict() if req.food else {},
        "waste": req.waste.dict() if req.waste else {},
    }
    result = calculate_daily_footprint(onboarding)
    return result.to_dict()
