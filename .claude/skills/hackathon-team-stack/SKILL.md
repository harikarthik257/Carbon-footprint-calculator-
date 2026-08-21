---
name: hackathon-team-stack
description: "Use this whenever writing, editing, or reviewing code in this hackathon
repo (Urban Carbon Footprint Calculator, Avinya 2026: Prakriti EcoInnovate Challenge).
Covers the team's stack, folder conventions, the emission-calculation API contract,
and how to add/change an emission factor without breaking the calculation engine.
Trigger for any frontend, backend, or emission-engine work in this repo."
---

# Team stack — Urban Carbon Footprint Calculator

Place this at `.claude/skills/hackathon-team-stack/SKILL.md` (or repo-root `SKILL.md`
if you're not using the skills folder convention). Claude Code loads it automatically
whenever a task in this repo matches its description — no re-explaining per session.

**Timing note:** Round 1 (due 15 Aug) only needs a thin, screenshot-able slice built
this way — see `PRD.md` §5 for the cut list. This skill earns its full value in
Round 2 (27–30 Aug), when the team is building for real under time pressure and every
session benefiting from the same conventions actually matters.

## Stack

- **Frontend:** React + Vite + TypeScript + Tailwind CSS + Recharts
- **Backend:** Python FastAPI, no database (deliberate — no auth/persistence for Round 1)
- **AI:** Google Gemini (`google-genai` package) — vision calls for meal-photo
  logging, text calls for personalized recommendations. Swapped in from the
  Anthropic SDK after the funded Anthropic account ran out of credits; Gemini's
  free tier covers this project's call volume.
- **Tests:** `pytest` for backend, especially the calculation engine
- **Lint:** `ruff` (Python), `eslint` (frontend)

## Folder conventions

```
/frontend/src/components   one component per file, PascalCase filenames
/frontend/src/api          typed fetch wrappers, one file per resource (footprint.ts, leaderboard.ts)
/backend/api/routes        one FastAPI router per resource, mounted in main.py
/backend/engine            pure functions only — no I/O, no FastAPI imports, so it's independently testable
/backend/engine/tests      pytest, one test file per engine module
/backend/data              emission_factors.py (single source of truth) + seed_leaderboard.py
```

## API contract (don't drift from this without updating both sides)

```
POST /api/calculate
  body: { transport: {...}, energy: {...}, food: {...}, waste: {...} }
  returns: { total_kg_co2e, by_category: {...}, factors_used: [...] }

POST /api/log-meal
  body: { image_base64: str, media_type: str }
  returns: { items: [{name, quantity, confidence}], is_mock: bool, preview_total_kg_co2e: float, note: str }
  (preview only — items are editable before logging; call /calculate-meal to finalize)

POST /api/calculate-meal
  body: { items: [{name: str, quantity: float}] }
  returns: { total_kg_co2e, by_category: {...}, factors_used: [...] }
  (used by both the manual-entry and photo-upload meal-logging paths — same
  editable-confirm step either way, per PRD.md §4)

POST /api/recommend
  body: { total_kg_co2e: float, by_category: {...} }
  returns: { strategies: [{action: str, estimated_savings_kg_co2e_per_day: float}], is_mock: bool }
  (2-3 strategies, ranked by impact, highest saving first)

GET /api/leaderboard
  returns: { entries: [{group_name, avg_kg_co2e_saved_per_day}], is_synthetic: true }

GET /api/benchmark
  returns: { national_avg_kg_co2e_per_day: float, unit: str, source: str }
  (India daily per-capita average, for the dashboard's "how you compare" stat —
  a national all-sector figure, shown as illustrative context)
```

Every response that includes a number also includes what it was computed from
(`factors_used` / `grounded_in`). This is a hard rule — it's what makes the AI layer
defensible in front of a judge instead of a black box.

## Emission-factor conventions

- All factors live in `backend/data/emission_factors.py`, structured as:
  ```python
  EMISSION_FACTORS = {
      "transport.gasoline_car_km": {"value": 0.17, "unit": "kg_co2e_per_km", "source": "EPA"},
      "food.plant_meal": {"value": 0.9, "unit": "kg_co2e_per_meal", "source": "GHG Protocol"},
      ...
  }
  ```
- Never inline a numeric emission factor anywhere else in the codebase — always
  reference this table, so the "one source of truth" claim in the pitch is actually
  true when a judge checks.
- Adding a new factor: add the entry here, add one test in
  `backend/engine/tests/test_factors.py` asserting the calculation engine uses it
  correctly, then wire it into the relevant route.

## AI call conventions

- The calculation engine (pure Python, deterministic) always runs **before** any
  Gemini call. Gemini never invents an emissions number — it receives already-computed
  numbers and factors, and its job is (a) structured extraction from an image, or (b)
  turning numbers into a specific, personalized recommendation string.
- Keep prompts in `backend/engine/prompts.py`, not inlined in route handlers, so the
  architect can review/tune wording in one place during integration.
- Every Gemini response used in the UI should be short enough to read in the demo
  without scrolling — cap recommendation text server-side if needed.

## Running things

```bash
cd backend && pip install -r requirements.txt --break-system-packages && uvicorn api.main:app --reload --port 8001
cd frontend && npm install && npm run dev
cd backend && pytest engine/tests -q
```
