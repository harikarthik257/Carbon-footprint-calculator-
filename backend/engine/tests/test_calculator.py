import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from engine.calculator import calculate_daily_footprint, calculate_meal_emissions
from data.emission_factors import get_factor


def test_empty_onboarding_gives_zero_footprint():
    result = calculate_daily_footprint({})
    assert result.total_kg_co2e == 0
    assert result.by_category == {"transport": 0.0, "energy": 0.0, "food": 0.0, "waste": 0.0}


def test_gasoline_car_commute_matches_factor_exactly():
    result = calculate_daily_footprint({
        "transport": {"mode": "gasoline_car", "km_per_day": 10},
    })
    expected = get_factor("transport.gasoline_car_km")["value"] * 10
    assert result.by_category["transport"] == pytest.approx(expected)
    assert result.total_kg_co2e == pytest.approx(expected)


def test_cycle_or_walk_is_zero_emissions():
    result = calculate_daily_footprint({
        "transport": {"mode": "cycle_or_walk", "km_per_day": 5},
    })
    assert result.by_category["transport"] == 0


def test_unknown_transport_mode_raises_loudly_not_silently():
    with pytest.raises(ValueError):
        calculate_daily_footprint({"transport": {"mode": "teleporter", "km_per_day": 5}})


def test_all_four_categories_sum_correctly():
    result = calculate_daily_footprint({
        "transport": {"mode": "campus_shuttle", "km_per_day": 4},
        "energy": {"kwh_per_day": 2, "grid": "national"},
        "food": {"plant_meals_per_day": 2, "meat_meals_per_day": 1},
        "waste": {"landfill_kg_per_day": 0.5},
    })
    manual_total = (
        get_factor("transport.campus_shuttle_km")["value"] * 4
        + get_factor("energy.grid_electricity_kwh")["value"] * 2
        + get_factor("food.plant_meal")["value"] * 2
        + get_factor("food.meat_meal")["value"] * 1
        + get_factor("waste.landfill_kg")["value"] * 0.5
    )
    assert result.total_kg_co2e == pytest.approx(manual_total)
    assert len(result.factors_used) == 5  # one FactorUse per non-zero input


def test_factors_used_are_traceable_to_a_source():
    result = calculate_daily_footprint({
        "transport": {"mode": "gasoline_car", "km_per_day": 3},
    })
    assert result.factors_used[0].source  # never empty — must be citeable


def test_meal_emissions_matches_known_items():
    result = calculate_meal_emissions([
        {"name": "Rice", "quantity": 1},
        {"name": "dal", "quantity": 1},
    ])
    expected = get_factor("food.rice_serving")["value"] + get_factor("food.dal_serving")["value"]
    assert result.total_kg_co2e == pytest.approx(expected)


def test_unidentified_food_item_uses_fallback_not_zero():
    result = calculate_meal_emissions([{"name": "mystery gravy", "quantity": 1}])
    fallback = get_factor("food.unidentified_item_fallback")["value"]
    assert result.total_kg_co2e == pytest.approx(fallback)
    assert result.total_kg_co2e > 0


def test_to_dict_rounds_and_is_json_serializable():
    result = calculate_daily_footprint({
        "transport": {"mode": "gasoline_car", "km_per_day": 3.333333},
    })
    d = result.to_dict()
    import json
    json.dumps(d)  # must not raise
    assert isinstance(d["total_kg_co2e"], float)
