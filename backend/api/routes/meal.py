import base64
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from engine.claude_client import extract_meal_from_photo
from engine.calculator import calculate_meal_emissions

router = APIRouter()


class LogMealRequest(BaseModel):
    image_base64: str
    media_type: str = "image/jpeg"


@router.post("/log-meal")
def log_meal(req: LogMealRequest):
    try:
        image_bytes = base64.b64decode(req.image_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="image_base64 is not valid base64")

    extraction = extract_meal_from_photo(image_bytes, media_type=req.media_type)
    items = extraction.get("items", [])

    # Nothing is "logged" yet at this point — the frontend shows these items
    # as an editable pre-filled list (see PRD.md §2) and calls /calculate-meal
    # (below) once the user confirms/edits quantities.
    calc = calculate_meal_emissions(items) if items else None

    return {
        "items": items,
        "is_mock": extraction.get("is_mock", False),
        "preview_total_kg_co2e": calc.total_kg_co2e if calc else 0,
        "note": "Preview only — items are editable before logging. "
                "Call /calculate-meal with the confirmed list to finalize.",
    }


class ConfirmedItem(BaseModel):
    name: str
    quantity: float = 1


class CalculateMealRequest(BaseModel):
    items: list[ConfirmedItem]


@router.post("/calculate-meal")
def calculate_meal(req: CalculateMealRequest):
    items = [item.dict() for item in req.items]
    result = calculate_meal_emissions(items)
    return result.to_dict()
