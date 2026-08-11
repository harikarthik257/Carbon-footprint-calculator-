"""
The AI layer. Two calls only:
  1. extract_meal_from_photo() — vision, image -> structured food items
  2. generate_recommendation() — text, computed numbers -> 2-3 ranked, grounded strategies

Hard rule (see CLAUDE.md): Claude never computes emissions math. It receives
numbers already computed by engine/calculator.py and either (a) extracts
structured data from an image, or (b) explains numbers it's handed. This
keeps the "AI-grounded" claim in the pitch deck literally true.

MOCK_AI: if ANTHROPIC_API_KEY isn't set (or MOCK_AI=true), both functions
return realistic canned responses instead of raising. This isn't a demo
trick — it lets the frontend workstream build against these endpoints on
day one without waiting on an API key, and it's a real fallback if the
network is flaky on the actual demo day. Every mock response is tagged
"is_mock": true so it's never mistaken for a real call in the UI or logs.

The same mock fallback also covers any Anthropic API error at call time
(rate limits, network issues, an out-of-credits account — the exact failure
we hit during Round 1 prep). A failed API call degrades to a mock response
rather than a 500, so a demo never crashes because a call to Anthropic
failed.

extract_meal_from_photo() additionally tolerates a model response that isn't
bare JSON: _strip_json_wrapping() strips whitespace and, if it detects a
```-fenced response (with or without a "json" language tag, or with prose
around it), falls back to the text between the first '{' and the last '}'.
If the result still isn't valid JSON, that also degrades to the mock
response (with the raw text logged to stderr for debugging) rather than a
500. generate_recommendation() does not have this same tolerance yet — its
json.loads() still raises on malformed output — since that failure mode
hasn't been observed there and doesn't need a fix pre-emptively.
"""
from __future__ import annotations
import base64
import json
import os
import sys

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")


def _mock_enabled() -> bool:
    if os.environ.get("MOCK_AI", "").lower() == "true":
        return True
    return not bool(os.environ.get("ANTHROPIC_API_KEY"))


def _get_client():
    import anthropic  # imported lazily so MOCK_AI mode never needs the package installed
    return anthropic.Anthropic()


def _mock_meal_extraction() -> dict:
    return {
        "items": [
            {"name": "rice", "quantity": 1, "confidence": "high"},
            {"name": "dal", "quantity": 1, "confidence": "high"},
            {"name": "mixed vegetables", "quantity": 1, "confidence": "medium"},
        ],
        "is_mock": True,
    }


def _strip_json_wrapping(text: str) -> str:
    """LLMs sometimes wrap JSON in prose or a ```json ... ``` / ``` ... ``` fence
    despite being told to return it bare. Strip whitespace and, if a fence is
    present, fall back to the text between the first '{' and the last '}' so a
    fenced or prose-wrapped response still parses."""
    text = text.strip()
    if "```" in text:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start:end + 1]
    return text


def _mock_recommendation(breakdown: dict) -> dict:
    by_cat = breakdown.get("by_category", {})
    biggest = max(by_cat, key=by_cat.get) if by_cat else "transport"
    return {
        "strategies": [
            {
                "action": "Swapping one meat meal for a plant-based one saves about 0.6 kg CO2e that day.",
                "estimated_savings_kg_co2e_per_day": 0.6,
            },
            {
                "action": (
                    f"{biggest.capitalize()} is your largest category today — swapping one "
                    f"gasoline-car trip for the campus shuttle saves about "
                    f"{round(0.17 * 4 - 0.10 * 4, 2)} kg CO2e per 4 km."
                ),
                "estimated_savings_kg_co2e_per_day": round(0.17 * 4 - 0.10 * 4, 2),
            },
        ],
        "is_mock": True,
    }


def extract_meal_from_photo(image_bytes: bytes, media_type: str = "image/jpeg") -> dict:
    """Returns {"items": [{"name": str, "quantity": float, "confidence": str}], "is_mock": bool}"""
    if _mock_enabled():
        return _mock_meal_extraction()

    from .prompts import MEAL_EXTRACTION_SYSTEM_PROMPT
    import anthropic

    client = _get_client()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=512,
            system=MEAL_EXTRACTION_SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": media_type, "data": image_b64},
                    },
                    {"type": "text", "text": "Identify the food items on this tray."},
                ],
            }],
        )
    except anthropic.APIError as e:
        print(f"[claude_client] extract_meal_from_photo: Anthropic API call failed, "
              f"falling back to mock ({e}).", file=sys.stderr)
        return _mock_meal_extraction()

    text = "".join(block.text for block in response.content if block.type == "text")
    try:
        parsed = json.loads(_strip_json_wrapping(text))
    except json.JSONDecodeError as e:
        print(f"[claude_client] extract_meal_from_photo: model response was not valid JSON "
              f"({e}), falling back to mock. Raw text:\n{text}", file=sys.stderr)
        return _mock_meal_extraction()
    parsed["is_mock"] = False
    return parsed


def generate_recommendation(breakdown: dict) -> dict:
    """Returns {"strategies": [{"action": str, "estimated_savings_kg_co2e_per_day": float}], "is_mock": bool}"""
    if _mock_enabled():
        return _mock_recommendation(breakdown)

    from .prompts import RECOMMENDATION_SYSTEM_PROMPT, build_recommendation_user_prompt
    import anthropic

    client = _get_client()
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            system=RECOMMENDATION_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_recommendation_user_prompt(breakdown)}],
        )
    except anthropic.APIError as e:
        print(f"[claude_client] generate_recommendation: Anthropic API call failed, "
              f"falling back to mock ({e}).", file=sys.stderr)
        return _mock_recommendation(breakdown)

    text = "".join(block.text for block in response.content if block.type == "text")
    parsed = json.loads(text)
    parsed["is_mock"] = False
    return parsed
