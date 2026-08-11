from fastapi import APIRouter

from data.emission_factors import NATIONAL_AVG_DAILY_KG_CO2E

router = APIRouter()


@router.get("/benchmark")
def benchmark():
    return {
        "national_avg_kg_co2e_per_day": NATIONAL_AVG_DAILY_KG_CO2E["value"],
        "unit": NATIONAL_AVG_DAILY_KG_CO2E["unit"],
        "source": NATIONAL_AVG_DAILY_KG_CO2E["source"],
    }
