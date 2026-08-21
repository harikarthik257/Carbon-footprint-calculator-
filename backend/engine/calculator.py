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


# Map of known food-item names/variants to emission-factor keys. Covers
# ~100 everyday Indian dishes (see data/emission_factors.py) so both the
# manual-entry list and the photo-extraction path have real sourced numbers
# behind most of what a student would actually log, not just a handful of
# canonical names.
FOOD_ITEM_TO_FACTOR_KEY = {
    # Rice / grain
    "rice": "food.rice_serving", "plain rice": "food.rice_serving", "steamed rice": "food.rice_serving",
    "jeera rice": "food.jeera_rice_serving", "cumin rice": "food.jeera_rice_serving",
    "lemon rice": "food.lemon_rice_serving",
    "curd rice": "food.curd_rice_serving",
    "pulao": "food.pulao_serving", "pilaf": "food.pulao_serving", "veg pulao": "food.pulao_serving",
    "veg biryani": "food.veg_biryani_serving", "vegetable biryani": "food.veg_biryani_serving",
    "chicken biryani": "food.chicken_biryani_serving",
    "mutton biryani": "food.mutton_biryani_serving",
    "khichdi": "food.khichdi_serving",
    "poha": "food.poha_serving",
    "upma": "food.upma_serving",
    # Breads
    "roti": "food.roti_item", "chapati": "food.roti_item", "phulka": "food.roti_item",
    "naan": "food.naan_item",
    "paratha": "food.paratha_plain_item", "plain paratha": "food.paratha_plain_item",
    "aloo paratha": "food.aloo_paratha_item", "potato paratha": "food.aloo_paratha_item",
    "poori": "food.poori_item", "puri": "food.poori_item",
    "bhatura": "food.bhatura_item", "bhature": "food.bhatura_item",
    # Dals / legumes
    "dal": "food.dal_serving", "lentils": "food.dal_serving", "daal": "food.dal_serving",
    "dal tadka": "food.dal_tadka_serving", "tadka dal": "food.dal_tadka_serving",
    "dal makhani": "food.dal_makhani_serving",
    "chana masala": "food.chana_masala_serving", "chickpea curry": "food.chana_masala_serving",
    "rajma": "food.rajma_serving", "kidney bean curry": "food.rajma_serving",
    "sambar": "food.sambar_serving", "sambhar": "food.sambar_serving",
    "moong dal": "food.moong_dal_serving",
    "chole": "food.chole_serving", "chhole": "food.chole_serving",
    # Vegetable curries
    "mixed vegetables": "food.vegetable_sabzi_serving", "vegetable sabzi": "food.vegetable_sabzi_serving",
    "sabzi": "food.vegetable_sabzi_serving", "mixed veg": "food.vegetable_sabzi_serving",
    "aloo gobi": "food.aloo_gobi_serving", "potato cauliflower curry": "food.aloo_gobi_serving",
    "aloo matar": "food.aloo_matar_serving", "potato peas curry": "food.aloo_matar_serving",
    "baingan bharta": "food.baingan_bharta_serving", "eggplant bharta": "food.baingan_bharta_serving",
    "bhindi masala": "food.bhindi_masala_serving", "okra curry": "food.bhindi_masala_serving",
    "mixed vegetable curry": "food.mixed_veg_curry_serving",
    "cabbage sabzi": "food.cabbage_sabzi_serving", "cabbage curry": "food.cabbage_sabzi_serving",
    "capsicum sabzi": "food.capsicum_sabzi_serving", "bell pepper curry": "food.capsicum_sabzi_serving",
    "gobi manchurian": "food.gobi_manchurian_serving", "cauliflower manchurian": "food.gobi_manchurian_serving",
    "veg kofta": "food.veg_kofta_serving", "vegetable kofta": "food.veg_kofta_serving",
    "jeera aloo": "food.jeera_aloo_serving", "cumin potato": "food.jeera_aloo_serving",
    "karela sabzi": "food.karela_sabzi_serving", "bitter gourd curry": "food.karela_sabzi_serving",
    # Paneer
    "paneer": "food.paneer_serving",
    "paneer butter masala": "food.paneer_butter_masala_serving",
    "palak paneer": "food.palak_paneer_serving", "spinach paneer": "food.palak_paneer_serving",
    "shahi paneer": "food.shahi_paneer_serving",
    "paneer tikka": "food.paneer_tikka_serving",
    # Non-veg
    "chicken curry": "food.chicken_curry_serving", "chicken": "food.chicken_curry_serving",
    "chicken 65": "food.chicken_65_serving",
    "tandoori chicken": "food.tandoori_chicken_serving",
    "butter chicken": "food.butter_chicken_serving",
    "chicken tikka": "food.chicken_tikka_serving",
    "egg": "food.egg_item", "boiled egg": "food.egg_item",
    "egg curry": "food.egg_curry_serving",
    "egg bhurji": "food.egg_bhurji_serving", "scrambled egg": "food.egg_bhurji_serving",
    "mutton curry": "food.mutton_curry_serving", "lamb curry": "food.mutton_curry_serving",
    "mutton keema": "food.mutton_keema_serving", "keema": "food.mutton_keema_serving",
    "fish curry": "food.fish_curry_serving",
    "fish fry": "food.fish_fry_serving",
    "prawn curry": "food.prawn_curry_serving", "shrimp curry": "food.prawn_curry_serving",
    "chicken soup": "food.chicken_soup_serving",
    # South Indian
    "idli": "food.idli_item",
    "dosa": "food.dosa_item", "plain dosa": "food.dosa_item",
    "masala dosa": "food.masala_dosa_item",
    "uttapam": "food.uttapam_item", "uthappam": "food.uttapam_item",
    "vada": "food.vada_item",
    "rasam": "food.rasam_serving",
    "medu vada": "food.medu_vada_item",
    "appam": "food.appam_item",
    # Snacks / street food
    "samosa": "food.samosa_item",
    "pakora": "food.pakora_serving", "bhajji": "food.pakora_serving", "bhaji": "food.pakora_serving",
    "vada pav": "food.vada_pav_item",
    "dhokla": "food.dhokla_serving",
    "bhel puri": "food.bhel_puri_serving", "bhelpuri": "food.bhel_puri_serving",
    "pani puri": "food.pani_puri_serving", "golgappa": "food.pani_puri_serving", "gupchup": "food.pani_puri_serving",
    "kachori": "food.kachori_item",
    "aloo tikki": "food.aloo_tikki_item", "potato tikki": "food.aloo_tikki_item",
    "sev puri": "food.sev_puri_serving",
    "cutlet": "food.cutlet_item", "vegetable cutlet": "food.cutlet_item",
    # Dairy / sides
    "curd": "food.curd_serving", "yogurt": "food.curd_serving", "dahi": "food.curd_serving",
    "raita": "food.raita_serving",
    "lassi": "food.lassi_serving",
    "buttermilk": "food.buttermilk_serving", "chaas": "food.buttermilk_serving",
    "papad": "food.papad_item", "papadum": "food.papad_item",
    "pickle": "food.pickle_serving", "achaar": "food.pickle_serving",
    "ghee": "food.ghee_serving",
    "butter": "food.butter_serving",
    # Sweets
    "gulab jamun": "food.gulab_jamun_item",
    "jalebi": "food.jalebi_serving",
    "rasgulla": "food.rasgulla_item",
    "kheer": "food.kheer_serving", "rice pudding": "food.kheer_serving",
    "halwa": "food.halwa_serving",
    "laddoo": "food.laddoo_item", "ladoo": "food.laddoo_item",
    "barfi": "food.barfi_item", "burfi": "food.barfi_item",
    "kaju katli": "food.kaju_katli_item",
    "rabri": "food.rabri_serving",
    "shrikhand": "food.shrikhand_serving",
    # Soups / beverages
    "veg soup": "food.veg_soup_serving", "vegetable soup": "food.veg_soup_serving",
    "tomato soup": "food.tomato_soup_serving",
    "tea": "food.tea_serving", "chai": "food.tea_serving",
    "coffee": "food.coffee_serving",
    # Combos / thali
    "veg thali": "food.veg_thali_serving", "vegetarian thali": "food.veg_thali_serving",
    "non veg thali": "food.non_veg_thali_serving", "non-veg thali": "food.non_veg_thali_serving",
    "mini meal": "food.mini_meal_serving",
}

# Longest-name-first so a specific match ("chicken biryani") is tried before
# a shorter one it happens to contain ("chicken curry" via "chicken").
_SORTED_FOOD_NAMES = sorted(FOOD_ITEM_TO_FACTOR_KEY, key=len, reverse=True)


_MIN_FUZZY_MATCH_LEN = 4  # below this, substring matching false-positives too
                          # easily (e.g. "tea" inside "sTEAmed vegetables")


def _match_factor_key(name: str) -> str:
    """Exact match first; if that misses, fall back to a substring match in
    either direction so a free-form name the vision model wasn't told to
    canonicalize (e.g. "spicy chicken curry with extra rice") still finds a
    real factor instead of the flat unidentified-item guess. Short known
    names (under _MIN_FUZZY_MATCH_LEN) are skipped for fuzzy matching —
    they're too likely to appear inside an unrelated word by coincidence."""
    if name in FOOD_ITEM_TO_FACTOR_KEY:
        return FOOD_ITEM_TO_FACTOR_KEY[name]
    for known_name in _SORTED_FOOD_NAMES:
        if len(known_name) < _MIN_FUZZY_MATCH_LEN:
            continue
        if known_name in name or name in known_name:
            return FOOD_ITEM_TO_FACTOR_KEY[known_name]
    return "food.unidentified_item_fallback"


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
        key = _match_factor_key(name)
        use = _use(key, quantity)
        factors_used.append(use)
        total += use.subtotal_kg_co2e

    return FootprintResult(
        total_kg_co2e=total,
        by_category={"food": total},
        factors_used=factors_used,
    )
