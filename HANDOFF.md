# HANDOFF.md — current build status

Everything below is built, wired, and verified end to end in a real browser against
a real running backend — not just read from source. `CLAUDE.md` has the permanent
stack/convention memory; this file is the snapshot of what actually exists right now.

---

## What's built and verified

**Backend — FastAPI, 7 endpoints, 12 tests passing (`pytest engine/tests -v`).**

- `/api/health` — `{"status": "ok", "mock_ai": bool}`
- `/api/calculate` — daily footprint from onboarding answers (transport/energy/food/waste)
- `/api/calculate-meal` — confirmed meal items → kg CO2e
- `/api/log-meal` — photo → structured food items (Gemini vision, mock-fallback)
- `/api/recommend` — footprint breakdown → 2–3 ranked strategies (Gemini text, mock-fallback)
- `/api/leaderboard` — synthetic hostel leaderboard (`is_synthetic: true`)
- `/api/benchmark` — India national daily per-capita average, for the dashboard's
  "how you compare" stat (sourced: World Bank / Global Carbon Project, ~1.9 t/year;
  labeled illustrative since it's a national all-sector figure, not a precise
  like-for-like match to this app's four categories)

`backend/data/emission_factors.py` is still the single source of truth for every
number the app shows — including the new benchmark constant.

**Frontend — full flow verified live via Playwright, zero console errors across
one continuous session touching every feature in order.**

- **Onboarding wizard** — 4 steps (transport, energy, food, waste)
- **Dashboard** — footprint total, category breakdown chart (Recharts)
- **Multi-strategy recommendations** — 2–3 ranked strategies, each with its own
  estimated kg CO2e/day saving, mock-labeled when running on mock data
- **Benchmark comparison** ("How you compare") — user's total vs. the India daily
  average, with a plain-language delta and the source cited inline
- **Meal logging, two paths into the same confirm step:**
  - **Manual entry** — an "Add a food item manually" button starts an empty,
    editable item row (name + quantity) with no photo required
  - **Photo upload** — Gemini vision extracts items from a tray photo into the
    same editable list; manual entry autocompletes against 100+ Indian dishes
  - Both paths share one "Confirm and log" step before anything affects the
    total — the editable-confirm requirement from `PRD.md`, satisfied either way
- **What-if slider** — live recalculation through the existing `/api/calculate`
  endpoint (no duplicated emission math in the frontend), confirmed to produce a
  real, correct delta when transport mode or distance changes
- **Hostel leaderboard** — ranked list plus a drag-to-rotate 3D sphere of the five
  hostels, each named after and photographed as a real Northeast India river/lake
  (Brahmaputra, Kopili, Burhi Dihing, Manas, Umiam), linked to their Wikipedia articles

**Visual/motion layer — all real, wired, and verified rendering correctly:**

- `MaskedHeading` — the "Campus Carbon" header title, a campus photo masked
  through the letters
- `ScrollExpand` — the "Your Campus Footprint" panel at the top of the dashboard,
  driven by the page's own scroll (not an isolated scroll trap — fixed after an
  earlier version locked users inside a small box)
- `ParticleText` — the small "Ways to cut your footprint" label inside the
  recommendation card
- `InfiniteMenu` — the leaderboard's 3D hostel sphere (WebGL2, `gl-matrix`)

**Explicitly NOT wired in, by request — code still exists in
`frontend/src/components/effects/` if wanted later:**

- `Galaxy` (starfield background) and `SplashCursor` (fluid cursor trail) were
  built, wired page-wide, then explicitly reverted back out. Don't be confused
  finding the component files — they're unused.
- `RippleDistortion` was requested twice but its source was truncated both times
  in the chat that specified it. Never built. If it's wanted, it needs the
  complete component source pasted again.

## AI provider: Google Gemini (swapped from Anthropic/Claude)

The AI layer originally used the Anthropic SDK. It was swapped to Google Gemini
(`google-genai` SDK, `backend/engine/claude_client.py` — filename kept for now,
content fully rewritten) because the Anthropic account ran out of credits and it
wasn't worth topping up; Gemini has a real, ongoing free tier that covers this
project's call volume.

Both AI calls (`extract_meal_from_photo`, `generate_recommendation`) fall back to
mock data (tagged `is_mock: true`) whenever `GEMINI_API_KEY` isn't set, `MOCK_AI=true`
is forced, or the Gemini API call itself fails for any reason (rate limit, network
error, a `503` under high demand — all confirmed live). Every mock-derived value in
the UI is labeled `mock response` so it's always clear which numbers came from a
live model call versus a canned one.

Both calls tolerate a model response wrapped in a markdown code fence or prose
(strips it before parsing, falls back to mock if it's still not valid JSON) — this
**has** been exercised against live Gemini responses, unlike the Anthropic-era
version of this doc claimed. Live testing against a real `GEMINI_API_KEY` surfaced
and fixed three real bugs: the configured model name had been deprecated (now
`gemini-3.6-flash`), `max_output_tokens` was too low because Gemini's internal
"thinking" tokens share the same budget as visible output (raised to 4096, confirmed
live with `finish_reason=STOP` on a complete 3-strategy response), and an attempt to
disable thinking via `thinking_config` was confirmed live to be rejected outright by
this model (`400 INVALID_ARGUMENT`) — removed.

Swapping in a `GEMINI_API_KEY` requires zero code changes — drop it into
`backend/.env`, restart the server, and real calls take over automatically
(`/api/health` returns `mock_ai: false` once a key is present).

## Known gaps / judgment calls, worth a second look later

- **India grid electricity factor**: `energy.grid_electricity_kwh` uses the
  *national* CEA average (0.71 kg CO2e/kWh). There's also a
  `..._hydro_weighted` factor (0.30) for a hydro-heavy regional grid, more
  accurate for some regions — wired into the calculator but not surfaced as a
  choice in onboarding yet.
- **Meal photo → factor matching** (`FOOD_ITEM_TO_FACTOR_KEY` in `calculator.py`)
  now covers 100+ everyday Indian dishes with fuzzy substring matching for name
  variants, up from the original ~10; anything still unmatched falls back to a
  conservative default rather than zero.
- **Benchmark comparison is a national, all-sector figure**, not a precise
  like-for-like sum of just transport/energy/food/waste. Labeled as illustrative
  context in the UI; a more defensible v2 would benchmark against a
  transport+energy+food+waste-only reference if one can be sourced.
- **CORS is wide open** (`allow_origins=["*"]`) — fine for local dev, tighten
  before any real deployment.
- **No auth, no persistence** — deliberate, per `PRD.md` cut list.

## Where the context lives

- `PRD.md` — scope, cut list, roadmap
- `CLAUDE.md` — permanent stack/convention memory, loads automatically every session
- `.claude/skills/carbon-footprint-stack/SKILL.md` — API contract, emission-factor conventions
- `pitch/screenshots/` — current, freshly captured screenshots
- `HOOKS.md` — why each hook in `.claude/settings.json` exists
