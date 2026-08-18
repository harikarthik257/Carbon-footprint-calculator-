"""
The AI layer. Two calls only:
  1. extract_meal_from_photo() — vision, image -> structured food items
  2. generate_recommendation() — text, computed numbers -> 2-3 ranked, grounded strategies

Hard rule (see CLAUDE.md): the AI never computes emissions math. It receives
numbers already computed by engine/calculator.py and either (a) extracts
structured data from an image, or (b) explains numbers it's handed. This
keeps the "AI-grounded" claim in the pitch deck literally true.

Provider: Google Gemini (google-genai SDK), swapped in from Anthropic/Claude.
Chosen for a real, ongoing free tier (rate-limited, not a time-limited trial
credit) that includes vision/multimodal calls at no cost — see the model
picked below.

MOCK_AI: if GEMINI_API_KEY isn't set (or MOCK_AI=true), both functions
return realistic canned responses instead of raising. This isn't a demo
trick — it lets the frontend workstream build against these endpoints on
day one without waiting on an API key, and it's a real fallback if the
network is flaky on the actual demo day. Every mock response is tagged
"is_mock": true so it's never mistaken for a real call in the UI or logs.

The same mock fallback also covers any Gemini API error at call time (rate
limits, network issues, an out-of-quota account — the exact failure we hit
with Anthropic during Round 1 prep, before this provider swap). A failed API
call degrades to a mock response rather than a 500, so a demo never crashes
because a call to Gemini failed.

Both functions tolerate a model response that isn't bare JSON:
_strip_json_wrapping() strips whitespace and, if it detects a ```-fenced
response (with or without a "json" language tag, or with prose around it),
falls back to the text between the first '{' and the last '}'. If the
result still isn't valid JSON, that also degrades to the mock response
(with the raw text logged to stderr for debugging) rather than a 500.

Both calls use a generous max_output_tokens (4096). This isn't precautionary
— the first live test against a real key hit exactly this failure: with
max_output_tokens=400, generate_recommendation's response came back
truncated mid-JSON (finish_reason=MAX_TOKENS — gemini-3.6-flash's "thinking"
tokens count against the same budget as visible output and ate most of it),
which is what motivated giving it the same JSON-tolerance
extract_meal_from_photo already had. Both failure modes are now handled the
same way in both functions, not just one. Tried explicitly disabling
thinking via thinking_config=ThinkingConfig(thinking_budget=0) to fix this
at the root — confirmed live that this model rejects that parameter outright
(400 INVALID_ARGUMENT), so the fix is the larger token budget alone, not a
thinking toggle. 4096 was confirmed live to be enough headroom for a real
3-strategy recommendation to complete with finish_reason=STOP (not
MAX_TOKENS) — if the model or prompt changes later, re-verify this isn't
still too tight.
"""
from __future__ import annotations
import json
import os
import sys

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")


def _mock_enabled() -> bool:
    if os.environ.get("MOCK_AI", "").lower() == "true":
        return True
    return not bool(os.environ.get("GEMINI_API_KEY"))


def _get_client():
    from google import genai  # imported lazily so MOCK_AI mode never needs the package installed
    return genai.Client()  # reads GEMINI_API_KEY (or GOOGLE_API_KEY) from the environment


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
    from google.genai import types
    from google.genai import errors as genai_errors

    client = _get_client()
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=media_type)

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[image_part, "Identify the food items on this tray."],
            config=types.GenerateContentConfig(
                system_instruction=MEAL_EXTRACTION_SYSTEM_PROMPT,
                max_output_tokens=4096,
            ),
        )
    except genai_errors.APIError as e:
        print(f"[claude_client] extract_meal_from_photo: Gemini API call failed, "
              f"falling back to mock ({e}).", file=sys.stderr)
        return _mock_meal_extraction()

    text = response.text or ""
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
    from google.genai import types
    from google.genai import errors as genai_errors

    client = _get_client()
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=build_recommendation_user_prompt(breakdown),
            config=types.GenerateContentConfig(
                system_instruction=RECOMMENDATION_SYSTEM_PROMPT,
                max_output_tokens=4096,
            ),
        )
    except genai_errors.APIError as e:
        print(f"[claude_client] generate_recommendation: Gemini API call failed, "
              f"falling back to mock ({e}).", file=sys.stderr)
        return _mock_recommendation(breakdown)

    text = response.text or ""
    try:
        parsed = json.loads(_strip_json_wrapping(text))
    except json.JSONDecodeError as e:
        print(f"[claude_client] generate_recommendation: model response was not valid JSON "
              f"({e}), falling back to mock. Raw text:\n{text}", file=sys.stderr)
        return _mock_recommendation(breakdown)
    parsed["is_mock"] = False
    return parsed
