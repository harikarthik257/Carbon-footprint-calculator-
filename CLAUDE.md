# CLAUDE.md

Project memory for Claude Code. Loads automatically at the start of every session in
this repo — keep it current as the build evolves.

## What this is

**Urban Carbon Footprint Calculator** — a personal project. It measures a student's
daily carbon footprint across transport, energy, food, and waste, then uses AI to
turn those numbers into personalized, ranked reduction strategies — grounded in a
deterministic emissions engine, not invented by the model. Full scope and rationale
live in `PRD.md` — read that first if you're planning, not just executing.

## The one thing this project lives or dies on

The AI-powered layer (photo → food emissions, numbers → ranked personalized
strategies) is the differentiator versus every other plain "carbon calculator" —
it's what makes this more than a form-and-dashboard app. Never treat this feature
as optional polish.

## Tech stack (decided — don't relitigate mid-build)

- **Frontend:** React + Vite + TypeScript + Tailwind CSS + Recharts. Vite over
  Next.js on purpose — this is a client-rendered single demo flow, SSR buys nothing
  and costs setup time not worth spending right now.
- **Backend:** Python FastAPI. No database — deliberate, per PRD.md cut list
  (no auth, no persistence for now); every response is computed fresh from
  `backend/data/emission_factors.py`, nothing is stored.
- **AI:** Google Gemini (`google-genai` SDK) — for (1) structured extraction from a
  meal-tray photo, (2) turning computed numbers into a personalized recommendation.
  Swapped in from the Anthropic SDK after the funded Anthropic account ran out of
  credits and it wasn't worth topping up; Gemini has a real ongoing free tier.
  Gemini never computes the emissions math itself — the calculation engine is
  deterministic Python; Gemini explains and personalizes numbers it's given, not
  numbers it invents. This is what keeps the AI feature "grounded" instead of a
  wrapper that can hallucinate a footprint.
- **Package managers:** npm (frontend), pip with `requirements.txt` (backend).

Override this once, early, if actual needs differ — then don't switch again mid-build.

## Repo layout

```
/frontend            React app — onboarding, dashboard, leaderboard, photo upload
/backend/api          FastAPI routes: /calculate /calculate-meal /log-meal /recommend
                       /leaderboard /benchmark
/backend/engine        Emission calculation engine + emission-factor data + Gemini calls
/backend/data          Seed/synthetic leaderboard + emission-factor + benchmark tables
/pitch                 Deck source, screenshots, demo clips
CLAUDE.md
SKILL.md               (or .claude/skills/carbon-footprint-stack/SKILL.md)
PRD.md
.claude/settings.json  hooks — see HOOKS.md for what's suggested and why
```

## Commands

```bash
# Backend — port 8001, not the uvicorn default 8000: Windows blocks 8000 on some
# dev machines (WinError 10013, a WSL2/Hyper-V port reservation), so the whole
# project standardizes on 8001. frontend/vite.config.ts proxies /api to it.
cd backend && pip install -r requirements.txt --break-system-packages
uvicorn api.main:app --reload --port 8001

# Frontend
cd frontend && npm install && npm run dev

# Backend tests (must pass before touching the calculation engine further)
cd backend && pytest engine/tests -q

# Frontend lint
cd frontend && npm run lint
```

## Conventions

- Emission factors live only in `backend/data/emission_factors.py` — one source of
  truth, never hardcode a factor inline in a route or component.
- API responses always return the emission factor and source used alongside the
  number, so the UI can show "where this number comes from."
- Commit messages: semantic (`feat:`, `fix:`, `mock:`) — tag hardcoded demo shortcuts
  with `mock:` so they're easy to find later.

## What's currently mocked

- Auth — single hardcoded demo user, no login flow.
- Leaderboard — synthetic seed data, labeled as illustrative.
- Map/hotspot visualization — not built yet.
- AI calls (meal-photo extraction, recommendations) — fall back to realistic mock
  data, tagged `is_mock: true` in the UI, whenever no `GEMINI_API_KEY` is
  available or the Gemini call itself fails. See `HANDOFF.md` for why this is
  the accepted posture, not a shortcut to fix later.
- Benchmark comparison — a national per-capita average used as illustrative
  context, not a precise like-for-like sum of this app's own four categories.

## Non-goals for now

No production deployment, no multi-tenant auth, no real per-user data collection.
Roadmap material (multi-campus, municipal-scale) stays conceptual until there's a
reason to build it.
