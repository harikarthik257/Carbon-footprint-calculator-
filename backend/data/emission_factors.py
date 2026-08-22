"""
Single source of truth for every emission factor used in the app.
Per SKILL.md: never hardcode a factor anywhere else in the codebase.

Sources: IPCC AR6 default factors, US EPA GHG Emission Factors Hub (2025),
GHG Protocol Scope 1-3 guidance. Where a source gives a range, we take the
midpoint and note it — defensible if anyone asks "where does that number
come from."
"""

EMISSION_FACTORS = {
    # --- Transport: kg CO2e per km ---
    "transport.gasoline_car_km": {
        "value": 0.17, "unit": "kg_co2e_per_km", "source": "EPA GHG Emission Factors Hub 2025",
    },
    "transport.campus_shuttle_km": {
        "value": 0.10, "unit": "kg_co2e_per_km", "source": "EPA (bus, per-passenger average)",
    },
    "transport.two_wheeler_km": {
        "value": 0.09, "unit": "kg_co2e_per_km", "source": "IPCC AR6 default, motorcycle",
    },
    "transport.cycle_or_walk_km": {
        "value": 0.0, "unit": "kg_co2e_per_km", "source": "N/A — zero tailpipe emissions",
    },
    "transport.shared_auto_km": {
        "value": 0.06, "unit": "kg_co2e_per_km", "source": "IPCC AR6 default, shared paratransit, per-passenger",
    },

    # --- Energy: kg CO2e per kWh ---
    # India's Northeast grid is hydro-heavy relative to the national average;
    # we use the national CEA average as the defensible default and flag it
    # as the one factor worth localizing further in a v2.
    "energy.grid_electricity_kwh": {
        "value": 0.71, "unit": "kg_co2e_per_kWh", "source": "CEA India CO2 Baseline Database (national average)",
    },
    "energy.grid_electricity_kwh_hydro_weighted": {
        "value": 0.30, "unit": "kg_co2e_per_kWh", "source": "CEA regional estimate, NE grid (hydro-heavy) — use if available",
    },

    # --- Food: kg CO2e per meal / per serving ---
    "food.plant_meal": {
        "value": 0.9, "unit": "kg_co2e_per_meal", "source": "GHG Protocol / Poore & Nemecek (2018), vegetarian thali average",
    },
    "food.meat_meal": {
        "value": 3.5, "unit": "kg_co2e_per_meal", "source": "GHG Protocol / Poore & Nemecek (2018), mixed non-veg meal average",
    },
    "food.dal_serving": {
        "value": 0.4, "unit": "kg_co2e_per_serving", "source": "Poore & Nemecek (2018), legumes",
    },
    "food.rice_serving": {
        "value": 0.35, "unit": "kg_co2e_per_serving", "source": "Poore & Nemecek (2018), rice per 150g cooked",
    },
    "food.vegetable_sabzi_serving": {
        "value": 0.15, "unit": "kg_co2e_per_serving", "source": "Poore & Nemecek (2018), mixed vegetables",
    },
    "food.chicken_curry_serving": {
        "value": 2.5, "unit": "kg_co2e_per_serving", "source": "Poore & Nemecek (2018), poultry per 100g",
    },
    "food.egg_item": {
        "value": 0.3, "unit": "kg_co2e_per_item", "source": "Poore & Nemecek (2018), per egg",
    },
    "food.paneer_serving": {
        "value": 1.1, "unit": "kg_co2e_per_serving", "source": "Poore & Nemecek (2018), dairy-derived protein",
    },
    "food.roti_item": {
        "value": 0.08, "unit": "kg_co2e_per_item", "source": "Poore & Nemecek (2018), wheat flatbread"
    },
    "food.unidentified_item_fallback": {
        "value": 0.3, "unit": "kg_co2e_per_item", "source": "Conservative mid-range estimate — used only when the vision model can't confidently identify an item",
    },

    # --- Food: expanded everyday Indian dish list ---
    # These are NOT individually-studied dishes — each is estimated from its
    # dominant ingredient(s) against Poore & Nemecek (2018)'s per-food-category
    # GHG intensities (grain, legume, dairy, poultry, red meat, fried-in-oil),
    # the same methodology already used for the 9 dishes above, just applied
    # dish-by-dish instead of category-by-category. Composite dishes (biryani,
    # thali) sum their component parts. Labeled "estimated" rather than
    # "sourced" in spirit — real math, not an individually cited study, and
    # that distinction matters more than the dish count.
    # --- Rice / grain dishes ---
    "food.jeera_rice_serving": {"value": 0.38, "unit": "kg_co2e_per_serving", "source": "Estimated: rice + oil tempering, Poore & Nemecek (2018) grain baseline"},
    "food.lemon_rice_serving": {"value": 0.35, "unit": "kg_co2e_per_serving", "source": "Estimated: rice + oil tempering, Poore & Nemecek (2018) grain baseline"},
    "food.curd_rice_serving": {"value": 0.45, "unit": "kg_co2e_per_serving", "source": "Estimated: rice + dairy, Poore & Nemecek (2018) grain + dairy baseline"},
    "food.pulao_serving": {"value": 0.55, "unit": "kg_co2e_per_serving", "source": "Estimated: rice + mixed vegetables + oil, Poore & Nemecek (2018)"},
    "food.veg_biryani_serving": {"value": 0.7, "unit": "kg_co2e_per_serving", "source": "Estimated: rice + vegetables + ghee/oil, Poore & Nemecek (2018)"},
    "food.chicken_biryani_serving": {"value": 2.8, "unit": "kg_co2e_per_serving", "source": "Estimated: rice + poultry, Poore & Nemecek (2018) poultry-dominant"},
    "food.mutton_biryani_serving": {"value": 5.5, "unit": "kg_co2e_per_serving", "source": "Estimated: rice + red meat, Poore & Nemecek (2018) lamb/mutton-dominant"},
    "food.khichdi_serving": {"value": 0.5, "unit": "kg_co2e_per_serving", "source": "Estimated: rice + lentils, Poore & Nemecek (2018) grain + legume baseline"},
    "food.poha_serving": {"value": 0.35, "unit": "kg_co2e_per_serving", "source": "Estimated: flattened rice + light vegetables, Poore & Nemecek (2018)"},
    "food.upma_serving": {"value": 0.32, "unit": "kg_co2e_per_serving", "source": "Estimated: semolina + light vegetables, Poore & Nemecek (2018) grain baseline"},
    # --- Breads ---
    "food.naan_item": {"value": 0.15, "unit": "kg_co2e_per_item", "source": "Estimated: refined wheat + dairy, Poore & Nemecek (2018) wheat baseline"},
    "food.paratha_plain_item": {"value": 0.25, "unit": "kg_co2e_per_item", "source": "Estimated: wheat + ghee, Poore & Nemecek (2018) wheat + added fat"},
    "food.aloo_paratha_item": {"value": 0.3, "unit": "kg_co2e_per_item", "source": "Estimated: wheat + potato + ghee, Poore & Nemecek (2018)"},
    "food.poori_item": {"value": 0.3, "unit": "kg_co2e_per_item", "source": "Estimated: wheat, deep-fried in oil, Poore & Nemecek (2018)"},
    "food.bhatura_item": {"value": 0.35, "unit": "kg_co2e_per_item", "source": "Estimated: refined wheat, deep-fried in oil, Poore & Nemecek (2018)"},
    # --- Dals / legumes ---
    "food.dal_tadka_serving": {"value": 0.42, "unit": "kg_co2e_per_serving", "source": "Estimated: lentils + oil tempering, Poore & Nemecek (2018) legume baseline"},
    "food.dal_makhani_serving": {"value": 0.75, "unit": "kg_co2e_per_serving", "source": "Estimated: lentils + cream/butter, Poore & Nemecek (2018) legume + dairy"},
    "food.chana_masala_serving": {"value": 0.5, "unit": "kg_co2e_per_serving", "source": "Estimated: chickpeas + oil, Poore & Nemecek (2018) legume baseline"},
    "food.rajma_serving": {"value": 0.55, "unit": "kg_co2e_per_serving", "source": "Estimated: kidney beans in gravy, Poore & Nemecek (2018) legume baseline"},
    "food.sambar_serving": {"value": 0.35, "unit": "kg_co2e_per_serving", "source": "Estimated: lentils + vegetables, Poore & Nemecek (2018) legume + vegetable"},
    "food.moong_dal_serving": {"value": 0.38, "unit": "kg_co2e_per_serving", "source": "Estimated: lentils, light preparation, Poore & Nemecek (2018) legume baseline"},
    "food.chole_serving": {"value": 0.5, "unit": "kg_co2e_per_serving", "source": "Estimated: chickpeas in gravy, Poore & Nemecek (2018) legume baseline"},
    # --- Vegetable curries ---
    "food.aloo_gobi_serving": {"value": 0.3, "unit": "kg_co2e_per_serving", "source": "Estimated: potato + cauliflower + oil, Poore & Nemecek (2018) vegetable baseline"},
    "food.aloo_matar_serving": {"value": 0.28, "unit": "kg_co2e_per_serving", "source": "Estimated: potato + peas + oil, Poore & Nemecek (2018) vegetable baseline"},
    "food.baingan_bharta_serving": {"value": 0.25, "unit": "kg_co2e_per_serving", "source": "Estimated: roasted eggplant + oil, Poore & Nemecek (2018) vegetable baseline"},
    "food.bhindi_masala_serving": {"value": 0.22, "unit": "kg_co2e_per_serving", "source": "Estimated: okra + oil, Poore & Nemecek (2018) vegetable baseline"},
    "food.mixed_veg_curry_serving": {"value": 0.3, "unit": "kg_co2e_per_serving", "source": "Estimated: mixed vegetables in gravy, Poore & Nemecek (2018) vegetable baseline"},
    "food.cabbage_sabzi_serving": {"value": 0.18, "unit": "kg_co2e_per_serving", "source": "Estimated: cabbage + light oil, Poore & Nemecek (2018) vegetable baseline"},
    "food.capsicum_sabzi_serving": {"value": 0.2, "unit": "kg_co2e_per_serving", "source": "Estimated: bell pepper + oil, Poore & Nemecek (2018) vegetable baseline"},
    "food.gobi_manchurian_serving": {"value": 0.4, "unit": "kg_co2e_per_serving", "source": "Estimated: deep-fried cauliflower + sauce, Poore & Nemecek (2018) vegetable + frying oil"},
    "food.veg_kofta_serving": {"value": 0.45, "unit": "kg_co2e_per_serving", "source": "Estimated: fried vegetable dumplings + dairy gravy, Poore & Nemecek (2018)"},
    "food.jeera_aloo_serving": {"value": 0.25, "unit": "kg_co2e_per_serving", "source": "Estimated: potato + light oil, Poore & Nemecek (2018) vegetable baseline"},
    "food.karela_sabzi_serving": {"value": 0.18, "unit": "kg_co2e_per_serving", "source": "Estimated: bitter gourd + light oil, Poore & Nemecek (2018) vegetable baseline"},
    # --- Paneer ---
    "food.paneer_butter_masala_serving": {"value": 1.4, "unit": "kg_co2e_per_serving", "source": "Estimated: paneer + cream/butter gravy, Poore & Nemecek (2018) dairy protein"},
    "food.palak_paneer_serving": {"value": 1.25, "unit": "kg_co2e_per_serving", "source": "Estimated: paneer + spinach, Poore & Nemecek (2018) dairy protein + vegetable"},
    "food.shahi_paneer_serving": {"value": 1.5, "unit": "kg_co2e_per_serving", "source": "Estimated: paneer + rich cream gravy, Poore & Nemecek (2018) dairy protein"},
    "food.paneer_tikka_serving": {"value": 1.2, "unit": "kg_co2e_per_serving", "source": "Estimated: grilled paneer, light marinade, Poore & Nemecek (2018) dairy protein"},
    # --- Non-veg ---
    "food.chicken_65_serving": {"value": 2.7, "unit": "kg_co2e_per_serving", "source": "Estimated: fried poultry, Poore & Nemecek (2018) poultry baseline"},
    "food.tandoori_chicken_serving": {"value": 2.6, "unit": "kg_co2e_per_serving", "source": "Estimated: roasted poultry, Poore & Nemecek (2018) poultry baseline"},
    "food.butter_chicken_serving": {"value": 2.9, "unit": "kg_co2e_per_serving", "source": "Estimated: poultry + cream/butter gravy, Poore & Nemecek (2018) poultry + dairy"},
    "food.chicken_tikka_serving": {"value": 2.6, "unit": "kg_co2e_per_serving", "source": "Estimated: grilled poultry, Poore & Nemecek (2018) poultry baseline"},
    "food.egg_curry_serving": {"value": 0.5, "unit": "kg_co2e_per_serving", "source": "Estimated: eggs in gravy, Poore & Nemecek (2018) egg baseline"},
    "food.egg_bhurji_serving": {"value": 0.4, "unit": "kg_co2e_per_serving", "source": "Estimated: scrambled eggs + oil, Poore & Nemecek (2018) egg baseline"},
    "food.mutton_curry_serving": {"value": 6.0, "unit": "kg_co2e_per_serving", "source": "Estimated: red meat (mutton/lamb), Poore & Nemecek (2018) high-intensity red meat"},
    "food.mutton_keema_serving": {"value": 5.8, "unit": "kg_co2e_per_serving", "source": "Estimated: minced red meat, Poore & Nemecek (2018) high-intensity red meat"},
    "food.fish_curry_serving": {"value": 1.5, "unit": "kg_co2e_per_serving", "source": "Estimated: fish, Poore & Nemecek (2018) fish/seafood baseline"},
    "food.fish_fry_serving": {"value": 1.6, "unit": "kg_co2e_per_serving", "source": "Estimated: fried fish, Poore & Nemecek (2018) fish/seafood baseline"},
    "food.prawn_curry_serving": {"value": 3.0, "unit": "kg_co2e_per_serving", "source": "Estimated: prawns/shrimp, Poore & Nemecek (2018) crustacean aquaculture baseline"},
    "food.chicken_soup_serving": {"value": 1.2, "unit": "kg_co2e_per_serving", "source": "Estimated: light broth with poultry, Poore & Nemecek (2018) poultry baseline"},
    # --- South Indian ---
    "food.idli_item": {"value": 0.12, "unit": "kg_co2e_per_item", "source": "Estimated: steamed rice/lentil batter, Poore & Nemecek (2018) grain + legume baseline"},
    "food.dosa_item": {"value": 0.25, "unit": "kg_co2e_per_item", "source": "Estimated: fermented rice/lentil crepe + oil, Poore & Nemecek (2018)"},
    "food.masala_dosa_item": {"value": 0.4, "unit": "kg_co2e_per_item", "source": "Estimated: dosa + potato filling, Poore & Nemecek (2018)"},
    "food.uttapam_item": {"value": 0.3, "unit": "kg_co2e_per_item", "source": "Estimated: thick rice/lentil pancake + vegetables, Poore & Nemecek (2018)"},
    "food.vada_item": {"value": 0.3, "unit": "kg_co2e_per_item", "source": "Estimated: deep-fried lentil doughnut, Poore & Nemecek (2018) legume + frying oil"},
    "food.rasam_serving": {"value": 0.2, "unit": "kg_co2e_per_serving", "source": "Estimated: tamarind lentil broth, Poore & Nemecek (2018) legume baseline"},
    "food.medu_vada_item": {"value": 0.32, "unit": "kg_co2e_per_item", "source": "Estimated: deep-fried lentil doughnut, Poore & Nemecek (2018) legume + frying oil"},
    "food.appam_item": {"value": 0.2, "unit": "kg_co2e_per_item", "source": "Estimated: fermented rice batter, Poore & Nemecek (2018) grain baseline"},
    # --- Snacks / street food ---
    "food.samosa_item": {"value": 0.35, "unit": "kg_co2e_per_item", "source": "Estimated: deep-fried wheat + potato filling, Poore & Nemecek (2018)"},
    "food.pakora_serving": {"value": 0.3, "unit": "kg_co2e_per_serving", "source": "Estimated: deep-fried vegetable fritters, Poore & Nemecek (2018) vegetable + frying oil"},
    "food.vada_pav_item": {"value": 0.4, "unit": "kg_co2e_per_item", "source": "Estimated: fried potato patty + bread, Poore & Nemecek (2018)"},
    "food.dhokla_serving": {"value": 0.2, "unit": "kg_co2e_per_serving", "source": "Estimated: steamed chickpea/gram flour, Poore & Nemecek (2018) legume baseline"},
    "food.bhel_puri_serving": {"value": 0.25, "unit": "kg_co2e_per_serving", "source": "Estimated: puffed rice + vegetables + chutney, Poore & Nemecek (2018)"},
    "food.pani_puri_serving": {"value": 0.2, "unit": "kg_co2e_per_serving", "source": "Estimated: fried wheat shells + light filling, Poore & Nemecek (2018)"},
    "food.kachori_item": {"value": 0.35, "unit": "kg_co2e_per_item", "source": "Estimated: deep-fried wheat + lentil filling, Poore & Nemecek (2018)"},
    "food.aloo_tikki_item": {"value": 0.28, "unit": "kg_co2e_per_item", "source": "Estimated: fried potato patty, Poore & Nemecek (2018) vegetable + frying oil"},
    "food.sev_puri_serving": {"value": 0.25, "unit": "kg_co2e_per_serving", "source": "Estimated: fried wheat crisps + vegetables, Poore & Nemecek (2018)"},
    "food.cutlet_item": {"value": 0.3, "unit": "kg_co2e_per_item", "source": "Estimated: fried vegetable/potato patty, Poore & Nemecek (2018) vegetable + frying oil"},
    # --- Dairy / sides ---
    "food.curd_serving": {"value": 0.25, "unit": "kg_co2e_per_serving", "source": "Estimated: plain yogurt, Poore & Nemecek (2018) dairy baseline"},
    "food.raita_serving": {"value": 0.2, "unit": "kg_co2e_per_serving", "source": "Estimated: yogurt + vegetables, Poore & Nemecek (2018) dairy baseline"},
    "food.lassi_serving": {"value": 0.4, "unit": "kg_co2e_per_serving", "source": "Estimated: yogurt-based drink, Poore & Nemecek (2018) dairy baseline"},
    "food.buttermilk_serving": {"value": 0.15, "unit": "kg_co2e_per_serving", "source": "Estimated: diluted yogurt drink, Poore & Nemecek (2018) dairy baseline"},
    "food.papad_item": {"value": 0.05, "unit": "kg_co2e_per_item", "source": "Estimated: lentil/gram flour wafer, Poore & Nemecek (2018) legume baseline"},
    "food.pickle_serving": {"value": 0.03, "unit": "kg_co2e_per_serving", "source": "Estimated: preserved vegetable condiment, Poore & Nemecek (2018) vegetable baseline"},
    "food.ghee_serving": {"value": 0.3, "unit": "kg_co2e_per_serving", "source": "Estimated: clarified butter, Poore & Nemecek (2018) dairy fat baseline"},
    "food.butter_serving": {"value": 0.25, "unit": "kg_co2e_per_serving", "source": "Estimated: dairy butter, Poore & Nemecek (2018) dairy fat baseline"},
    # --- Sweets ---
    "food.gulab_jamun_item": {"value": 0.35, "unit": "kg_co2e_per_item", "source": "Estimated: fried milk-solid dumpling in syrup, Poore & Nemecek (2018) dairy + frying oil"},
    "food.jalebi_serving": {"value": 0.3, "unit": "kg_co2e_per_serving", "source": "Estimated: deep-fried batter in syrup, Poore & Nemecek (2018) grain + frying oil"},
    "food.rasgulla_item": {"value": 0.25, "unit": "kg_co2e_per_item", "source": "Estimated: milk-solid dumpling in syrup, Poore & Nemecek (2018) dairy baseline"},
    "food.kheer_serving": {"value": 0.4, "unit": "kg_co2e_per_serving", "source": "Estimated: milk + rice pudding, Poore & Nemecek (2018) dairy + grain"},
    "food.halwa_serving": {"value": 0.45, "unit": "kg_co2e_per_serving", "source": "Estimated: grain/vegetable + ghee + sugar, Poore & Nemecek (2018) dairy fat baseline"},
    "food.laddoo_item": {"value": 0.35, "unit": "kg_co2e_per_item", "source": "Estimated: flour/lentil + ghee + sugar, Poore & Nemecek (2018) dairy fat baseline"},
    "food.barfi_item": {"value": 0.4, "unit": "kg_co2e_per_item", "source": "Estimated: milk solids + sugar, Poore & Nemecek (2018) dairy baseline"},
    "food.kaju_katli_item": {"value": 0.4, "unit": "kg_co2e_per_item", "source": "Estimated: cashew + sugar + ghee, Poore & Nemecek (2018) dairy fat baseline"},
    "food.rabri_serving": {"value": 0.5, "unit": "kg_co2e_per_serving", "source": "Estimated: reduced/condensed milk dessert, Poore & Nemecek (2018) dairy baseline"},
    "food.shrikhand_serving": {"value": 0.4, "unit": "kg_co2e_per_serving", "source": "Estimated: strained yogurt dessert, Poore & Nemecek (2018) dairy baseline"},
    # --- Soups / beverages ---
    "food.veg_soup_serving": {"value": 0.15, "unit": "kg_co2e_per_serving", "source": "Estimated: vegetable broth, Poore & Nemecek (2018) vegetable baseline"},
    "food.tomato_soup_serving": {"value": 0.12, "unit": "kg_co2e_per_serving", "source": "Estimated: tomato-based broth, Poore & Nemecek (2018) vegetable baseline"},
    "food.tea_serving": {"value": 0.1, "unit": "kg_co2e_per_serving", "source": "Estimated: tea + milk, Poore & Nemecek (2018) dairy baseline (small serving)"},
    "food.coffee_serving": {"value": 0.12, "unit": "kg_co2e_per_serving", "source": "Estimated: coffee + milk, Poore & Nemecek (2018) dairy baseline (small serving)"},
    # --- Combos / thali ---
    "food.veg_thali_serving": {"value": 1.3, "unit": "kg_co2e_per_serving", "source": "Estimated: sum of rice + dal + 2 sabzi + roti + curd, Poore & Nemecek (2018)"},
    "food.non_veg_thali_serving": {"value": 3.2, "unit": "kg_co2e_per_serving", "source": "Estimated: veg thali + one poultry/meat item, Poore & Nemecek (2018)"},
    "food.mini_meal_serving": {"value": 0.8, "unit": "kg_co2e_per_serving", "source": "Estimated: light combo (grain + one side), Poore & Nemecek (2018)"},

    # --- Waste: kg CO2e per kg ---
    "waste.landfill_kg": {
        "value": 0.6, "unit": "kg_co2e_per_kg", "source": "EPA WARM model, mixed MSW to landfill",
    },
    "waste.composted_kg": {
        "value": 0.1, "unit": "kg_co2e_per_kg", "source": "EPA WARM model, composting pathway",
    },
    "waste.recycled_kg": {
        "value": 0.05, "unit": "kg_co2e_per_kg", "source": "EPA WARM model, recycling pathway (processing only)",
    },
}


# Reference point for the dashboard's "how you compare" stat. This is a
# national per-capita total (all sectors — industry, power generation, etc.),
# not a like-for-like sum of just transport/energy/food/waste, so it's shown
# as illustrative context rather than a precise apples-to-apples comparison —
# same honesty standard as the "illustrative — seed data" leaderboard label.
NATIONAL_AVG_DAILY_KG_CO2E = {
    "value": 5.2,
    "unit": "kg_co2e_per_day",
    "source": (
        "World Bank / Global Carbon Project: India per-capita CO2 emissions "
        "~1.9 t/year, averaged per day. Covers all national emissions, not just "
        "personal transport/energy/food/waste — illustrative context, not a "
        "precise methodology match."
    ),
}


def get_factor(key: str) -> dict:
    """Look up a factor by key. Raises KeyError loudly rather than silently
    defaulting — a missing factor should fail a test, not fail a demo."""
    if key not in EMISSION_FACTORS:
        raise KeyError(
            f"No emission factor registered for '{key}'. "
            f"Add it to EMISSION_FACTORS in data/emission_factors.py first."
        )
    return EMISSION_FACTORS[key]
