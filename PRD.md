# PRD — Urban Carbon Footprint Calculator

A personal project: an app that measures a student's daily carbon footprint across
transport, energy, food, and waste, and uses AI to turn those numbers into
personalized, ranked reduction strategies — grounded in a deterministic emissions
engine, not invented by the model.

---

## 1. Core user story

"I open the app, answer a 60-second onboarding quiz (or snap a photo of my
dining-hall tray), and immediately see my footprint by category, one AI-explained
action I can take today, and where I rank against a benchmark."

## 2. The one feature that must be real, even in a thin prototype

**AI-grounded footprint + recommendation engine:**
1. Deterministic calculation engine (`activity × IPCC/EPA/GHG Protocol factor`) — the
   numbers must never be hand-wavy.
2. Gemini reads a tray photo → structured food-item estimates, shown as an
   **editable, pre-filled guess** the user can correct before it's logged (turns the
   vision model's imprecision into a transparency feature instead of a liability).
3. Gemini turns the computed numbers into one sharp, specific, actionable
   recommendation — never a static lookup-table line.

## 3. Cut list — deliberately out of scope for the current build

Build only enough to work end-to-end and demo cleanly:
1. Skip auth entirely — one hardcoded demo user.
2. Skip a live leaderboard — a static seeded mockup is enough for now.
3. Skip maps/hotspot visualization entirely.
4. Skip cross-session persistence — in-memory or a reset-on-demand SQLite file is fine.

One clean, working flow (onboarding → dashboard → photo log → recommendation) beats
five half-built ones.

## 4. What makes this different from a plain calculator

- **Sustainability grounding:** every number traces back to a citation-backed
  emission factor (IPCC/EPA/GHG Protocol) in `backend/data/emission_factors.py`, not
  a guess.
- **AI-grounded innovation:** the vision + recommendation layer is what's different
  from a form-based calculator — named explicitly wherever the project is described.
- **Technical honesty:** real screenshots/clips over descriptions; the app never
  overclaims accuracy on AI-derived numbers (mock and estimated values are always
  labeled as such).
- **Scalability:** a rough roadmap — single app → multi-location → broader
  municipal-scale reference — exists conceptually but stays out of code until
  there's a reason to build it.
