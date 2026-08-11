"""
Deterministic emission calculations. Pure functions only — no FastAPI imports,
no network calls, no randomness — so this module is trivially unit-testable
and Claude never touches the actual math (see claude_client.py docstring).
"""
from __future__ import annotations
from dataclasses import dataclass, field

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from data.emission_factors import get_factor


@dataclass
class FactorUse:
    key: str
    value: float
    unit: str
    source: str
    quantity: float
    subtotal_kg_co2e: float


@dataclass
class FootprintResult:
    total_kg_co2e: float
    by_category: dict[str, float]
    factors_used: list[FactorUse] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "total_kg_co2e": round(self.total_kg_co2e, 2),
            "by_category": {k: round(v, 2) for k, v in self.by_category.items()},
            "factors_used": [
                {
                    "key": f.key,
                    "value": f.value,
                    "unit": f.unit,
                    "source": f.source,
                    "quantity": f.quantity,
                    "subtotal_kg_co2e": round(f.subtotal_kg_co2e, 2),
                }
                for f in self.factors_used
            ],
        }


def _use(key: str, quantity: float) -> FactorUse:
    factor = get_factor(key)
    subtotal = factor["value"] * quantity
    return FactorUse(
        key=key, value=factor["value"], unit=factor["unit"],
        source=factor["source"], quantity=quantity, subtotal_kg_co2e=subtotal,
    )


def calculate_daily_footprint(onboarding: dict) -> FootprintResult:
    """
    onboarding shape (all fields optional, missing = 0 contribution):
    {
      "transport": {"mode": "gasoline_car" | "campus_shuttle" | "two_wheeler"
                            | "cycle_or_walk" | "shared_auto", "km_per_day": float},
      "energy":    {"kwh_per_day": float, "grid": "national" | "ne_hydro_weighted"},
      "food":      {"plant_meals_per_day": int, "meat_meals_per_day": int},
      "waste":     {"landfill_kg_per_day": float, "composted_kg_per_day": float,
                     "recycled_kg_per_day": float},
    }
    """
    factors_used: list[FactorUse] = []
    by_category = {"transport": 0.0, "energy": 0.0, "food": 0.0, "waste": 0.0}

    transport = onboarding.get("transport") or {}
    mode = transport.get("mode")
    km = float(transport.get("km_per_day", 0) or 0)
    if mode and km > 0:
        mode_key_map = {
            "gasoline_car": "transport.gasoline_car_km",
            "campus_shuttle": "transport.campus_shuttle_km",
            "two_wheeler": "transport.two_wheeler_km",
            "cycle_or_walk": "transport.cycle_or_walk_km",
            "shared_auto": "transport.shared_auto_km",
        }
        key = mode_key_map.get(mode)
        if key is None:
            raise ValueError(f"Unknown transport mode: {mode!r}")
        use = _use(key, km)
        factors_used.append(use)
        by_category["transport"] += use.subtotal_kg_co2e

    energy = onboarding.get("energy") or {}
    kwh = float(energy.get("kwh_per_day", 0) or 0)
    if kwh > 0:
        grid = energy.get("grid", "national")
        key = (
            "energy.grid_electricity_kwh_hydro_weighted"
            if grid == "ne_hydro_weighted"
            else "energy.grid_electricity_kwh"
        )
        use = _use(key, kwh)
        factors_used.append(use)
        by_category["energy"] += use.subtotal_kg_co2e

    food = onboarding.get("food") or {}
    plant_meals = float(food.get("plant_meals_per_day", 0) or 0)
    meat_meals = float(food.get("meat_meals_per_day", 0) or 0)
    if plant_meals > 0:
        use = _use("food.plant_meal", plant_meals)
        factors_used.append(use)
        by_category["food"] += use.subtotal_kg_co2e
    if meat_meals > 0:
        use = _use("food.meat_meal", meat_meals)
        factors_used.append(use)
        by_category["food"] += use.subtotal_kg_co2e

    waste = onboarding.get("waste") or {}
    for field_name, key in [
        ("landfill_kg_per_day", "waste.landfill_kg"),
        ("composted_kg_per_day", "waste.composted_kg"),
        ("recycled_kg_per_day", "waste.recycled_kg"),
    ]:
        qty = float(waste.get(field_name, 0) or 0)
        if qty > 0:
            use = _use(key, qty)
            factors_used.append(use)
            by_category["waste"] += use.subtotal_kg_co2e

    total = sum(by_category.values())
    return FootprintResult(total_kg_co2e=total, by_category=by_category, factors_used=factors_used)


# Map of known food-item names (as the vision model might label them) to
# emission-factor keys. Deliberately small and India-campus-dining specific —
# extend this list before extending anything else if meal logging accuracy
# needs improving.
FOOD_ITEM_TO_FACTOR_KEY = {
    "rice": "food.rice_serving",
    "dal": "food.dal_serving",
    "lentils": "food.dal_serving",
    "mixed vegetables": "food.vegetable_sabzi_serving",
    "vegetable sabzi": "food.vegetable_sabzi_serving",
    "sabzi": "food.vegetable_sabzi_serving",
    "chicken curry": "food.chicken_curry_serving",
    "chicken": "food.chicken_curry_serving",
    "egg": "food.egg_item",
    "boiled egg": "food.egg_item",
    "paneer": "food.paneer_serving",
    "roti": "food.roti_item",
    "chapati": "food.roti_item",
}


def calculate_meal_emissions(food_items: list[dict]) -> FootprintResult:
    """
    food_items: [{"name": str, "quantity": float (default 1)}]
    Unmatched item names fall back to a conservative fallback factor rather
    than silently contributing zero — an unidentified item should never look
    free.
    """
    factors_used: list[FactorUse] = []
    total = 0.0

    for item in food_items:
        name = (item.get("name") or "").strip().lower()
        quantity = float(item.get("quantity", 1) or 1)
        key = FOOD_ITEM_TO_FACTOR_KEY.get(name, "food.unidentified_item_fallback")
        use = _use(key, quantity)
        factors_used.append(use)
        total += use.subtotal_kg_co2e

    return FootprintResult(
        total_kg_co2e=total,
        by_category={"food": total},
        factors_used=factors_used,
    )
