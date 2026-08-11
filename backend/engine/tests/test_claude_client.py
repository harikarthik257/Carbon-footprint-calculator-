import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from engine.claude_client import generate_recommendation, _strip_json_wrapping


def test_mock_recommendation_returns_two_to_three_ranked_strategies():
    breakdown = {
        "total_kg_co2e": 7.4,
        "by_category": {"transport": 0.5, "energy": 1.4, "food": 5.0, "waste": 0.5},
    }
    result = generate_recommendation(breakdown)

    assert result["is_mock"] is True
    assert 2 <= len(result["strategies"]) <= 3
    for strategy in result["strategies"]:
        assert isinstance(strategy["action"], str) and strategy["action"]
        assert isinstance(strategy["estimated_savings_kg_co2e_per_day"], (int, float))

    savings = [s["estimated_savings_kg_co2e_per_day"] for s in result["strategies"]]
    assert savings == sorted(savings, reverse=True)


def test_strip_json_wrapping_handles_markdown_fenced_response():
    fenced = '```json\n{"items": []}\n```'
    cleaned = _strip_json_wrapping(fenced)
    assert json.loads(cleaned) == {"items": []}
