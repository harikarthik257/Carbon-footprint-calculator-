import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from data.emission_factors import NATIONAL_AVG_DAILY_KG_CO2E


def test_national_average_benchmark_is_sourced_and_positive():
    assert NATIONAL_AVG_DAILY_KG_CO2E["value"] > 0
    assert NATIONAL_AVG_DAILY_KG_CO2E["unit"] == "kg_co2e_per_day"
    assert len(NATIONAL_AVG_DAILY_KG_CO2E["source"]) > 0
