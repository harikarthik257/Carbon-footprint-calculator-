# CLAUDE.md

Project memory for Claude Code. Loads automatically at the start of every session in
this repo — keep it current as the build evolves.

## What this is

**Urban Carbon Footprint Calculator** — the team's answer to Problem Statement #2 of
**Avinya 2026: Prakriti EcoInnovate Challenge** (Prakriti × Techniche, IIT Guwahati).
Full scope and rationale live in `PRD.md` — read that first if you're planning, not
just executing.

## Where this fits in the actual competition (read before doing anything)

This is a two-round competition, not a single build sprint:

- **Round 1 — due 15 Aug 2026, 11:59 PM IST.** The literal deliverable is a
  **solution proposal + PPT deck**, not code. A thin working prototype is optional
  but strongly recommended — screenshots/clips of it strengthen the Technical
  Feasibility (25%) and Innovation (30%) scores in the deck.
- **Shortlist announced 20 Aug.**
- **Round 2 — 27–30 Aug, on-campus.** Half the score is presenting this *same* idea
  live; the other half is a brand-new problem revealed on-site, solved in a 24–30hr
  sprint.

**Practical implication:** don't over-invest in production-grade code before 15 Aug —
that time is worth more in the deck and a thin, clean, demoable slice. This repo's
CLAUDE.md/SKILL.md/hooks setup is really being built *for Round 2's on-site sprint*,
where a fast, well-scaffolded Claude Code workflow is the actual differentiator.

## The one thing this project lives or dies on

The AI-powered layer (photo → food emissions, numbers → ranked personalized
strategies) is the differentiator versus every other "carbon calculator"
submission — and Solution Innovation is 30% of the Round 1 score, the single largest
line item. Never treat this feature as optional polish.

## Tech stack (decided — don't relitigate mid-build)

- **Frontend:** React + Vite + TypeScript + Tailwind CSS + Recharts. Vite over
  Next.js on purpose — this is a client-rendered single demo flow, SSR buys nothing
  and costs setup time either team is short on right now.
- **Backend:** Python FastAPI. No database — deliberate, per PRD.md §5 cut list
  (no auth, no persistence for Round 1); every response is computed fresh from
  `backend/data/emission_factors.py`, nothing is stored.
- **AI:** Google Gemini (`google-genai` SDK) — for (1) structured extraction from a
  meal-tray photo, (2) turning computed numbers into a personalized recommendation.
  Swapped in from the Anthropic SDK after the funded Anthropic account ran out of
  credits and the team chose not to purchase more before the deadline; Gemini has
  a real ongoing free tier. Gemini never computes the emissions math itself — the
  calculation engine is deterministic Python; Gemini explains and personalizes
  numbers it's given, not numbers it invents. This is what keeps the AI feature
  "grounded" instead of a wrapper that can hallucinate a footprint.
- **Package managers:** npm (frontend), pip with `requirements.txt` (backend).

Override this once, early, if the team's actual strengths differ — then don't switch
again (see the playbook's "learning a new tool mid-event" failure mode).

## Repo layout

```
/frontend            React app — onboarding, dashboard, leaderboard, photo upload
/backend/api          FastAPI routes: /calculate /calculate-meal /log-meal /recommend
                       /leaderboard /benchmark
/backend/engine        Emission calculation engine + emission-factor data + Gemini calls
/backend/data          Seed/synthetic leaderboard + emission-factor + benchmark tables
/pitch                 Round 1 deck source, screenshots, demo clips, submission files
CLAUDE.md
SKILL.md               (or .claude/skills/hackathon-team-stack/SKILL.md)
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
  number, so the frontend (and the deck) can show "where this number comes from."
- Commit messages: semantic (`feat:`, `fix:`, `mock:`) — tag hardcoded demo shortcuts
  with `mock:` so they're easy to find later.
- Each workstream (see `PRD.md` §6) only edits its own directory.

## What's currently mocked

- Auth — single hardcoded demo user, no login flow.
- Leaderboard — synthetic seed data, labeled as illustrative if shown at all before 15 Aug.
- Map/hotspot visualization — not built for Round 1.
- AI calls (meal-photo extraction, recommendations) — fall back to realistic mock
  data, tagged `is_mock: true` in the UI, whenever no `GEMINI_API_KEY` is
  available or the Gemini call itself fails. See `HANDOFF.md` for why this is
  the accepted Round 1 posture, not a shortcut to fix later.
- Benchmark comparison — a national per-capita average used as illustrative
  context, not a precise like-for-like sum of this app's own four categories.

## Non-goals before 15 Aug

No production deployment, no multi-tenant auth, no real per-user data collection.
Phase 2/3 roadmap material goes on a slide, not in code, until Round 2 (if reached).

## Team

2–3 people. See `PRD.md` §6 for who owns what.
