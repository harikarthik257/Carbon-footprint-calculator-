# PRD — Urban Carbon Footprint Calculator
### Problem Statement #2, Avinya 2026: Prakriti EcoInnovate Challenge (Prakriti × Techniche, IIT Guwahati)

**Status: v2 — rebuilt from the actual problem-statement deck the team shared.** No more
flagged assumptions on dates, rubric, or format — these are the confirmed facts.

---

## 0. Confirmed event facts

- Organizer: Prakriti Club × Techniche, IIT Guwahati.
- **"Urban Carbon Footprint Calculator" is problem statement #2 of the official list**,
  under the "Software & Web Development" track. The repo README is written almost
  verbatim to this brief — this is a direct answer to the real prompt, not a
  freestanding idea hoping it fits.
- **Two-round structure, not one build sprint:**
  - **Round 1 (idea round):** choose one problem statement, submit a solution
    proposal + presentation deck (PPT format). **Deadline: 15 Aug 2026, 11:59 PM
    IST.** No working code is required for this round — but nothing stops you from
    including one, and it will help (see §2).
  - Shortlist announced **20 Aug 2026**.
  - **Round 2 (on-campus, 27–30 Aug 2026):** shortlisted teams present their
    *original* Round 1 idea live to an expert jury (Phase-1, 50% of Round 2 score),
    then run a 24–30 hour on-site sprint on a **new** problem statement introduced by
    industry mentors (Phase-2, the other 50%). You will not know that second problem
    until you're on-site.
- Team size: 2–5 members (your 2–3 fits).
- Prize pool: ₹1,00,000 (₹65,000 cash) + goodies, certificates, mentorship, networking.
- Judging decisions are final; submissions must be original; plagiarism = disqualification.

## 1. Marking scheme — this decides where your hours go

**Round 1 (100% of that stage's score):**

| Criterion | Weight |
|---|---|
| Solution Innovation | **30%** |
| Technical Feasibility | 25% |
| Scalability & Practicality | 25% |
| Sustainability Impact | 20% |

Innovation is the single biggest line item. That's the concrete case for promoting the
AI photo-logging feature from "stretch goal" (as the README has it) to the centerpiece
of the pitch — it's the one part of this idea that isn't identical to every other
team's calculator-and-dashboard submission, and it's scored at nearly a third of the
Round 1 total.

**Round 2:** Phase-1 (live presentation of your original idea) 50%, Phase-2 (the new
on-site sprint challenge) 50%.

## 2. What actually needs to exist, and by when

| Deliverable | Deadline | Format |
|---|---|---|
| Solution proposal + pitch deck | **15 Aug** | PPT — the literal Round 1 submission |
| *(strongly recommended, not required)* a thin working prototype — just the calculation engine + one working AI call | by 15 Aug, to screenshot/clip into the deck | Code |
| If shortlisted: a working demo of the *same* idea, rehearsed for live presentation | before 27 Aug | Code + demo script |
| A reusable Claude Code setup, battle-tested, ready to point at an unknown new problem | before 27 Aug | Tooling |

The four files built for this repo (`CLAUDE.md`, `SKILL.md`, this `PRD.md`,
`HOOKS.md`) are real infrastructure for **Round 2's on-site sprint**, where speed
matters and the problem is unknown until you're there. For the next 5 days, the
actual scored artifact is the deck — treat code as supporting evidence for it, not
the deliverable itself.

## 3. Core user story

"As an IITG student, I open the app, answer a 60-second onboarding quiz (or snap a
photo of my dining-hall tray), and immediately see my footprint by category, one
AI-explained action I can take today, and where my hostel ranks."

## 4. The one feature that must be real, even in a thin prototype

**AI-grounded footprint + recommendation engine:**
1. Deterministic calculation engine (`activity × IPCC/EPA/GHG Protocol factor`) — the
   numbers must never be hand-wavy.
2. Gemini reads a tray photo → structured food-item estimates, shown as an
   **editable, pre-filled guess** the student can correct before it's logged (turns
   the vision model's imprecision into a transparency feature instead of a liability
   — which also helps the Technical Feasibility score, since you're not overclaiming
   accuracy).
3. Gemini turns the computed numbers into one sharp, specific, campus-grounded
   recommendation — never a static lookup-table line.

## 5. Cut list — for the Round 1 prototype specifically

Given 5 days and 2–3 people, if you build anything before the 15th, build only enough
to screenshot cleanly:
1. Skip auth entirely — one hardcoded demo user.
2. Skip a live leaderboard — a static seeded mockup screenshot is enough for a deck.
3. Skip maps/hotspot visualization entirely.
4. Skip cross-session persistence — in-memory or a reset-on-demand SQLite file is fine.

One clean, working flow (onboarding → dashboard → photo log → recommendation) beats
five half-built ones in a deck.

## 6. Task breakdown for a 2–3 person team, 5 days to Round 1

| Person | Owns |
|---|---|
| **A** | Backend + emission engine + Gemini calls — the feature that must be real |
| **B** | Frontend — onboarding, dashboard, photo upload UI |
| **C** *(if 3)* | Deck, proposal narrative, screenshots/demo capture, submission logistics — starts day 1, not day 4 |

If it's 2 people, one of you owns both the deck and whichever side of the stack has
slack once the core flow works end-to-end.

## 7. Rubric-mapped pitch structure — what actually goes in the PPT

- **Sustainability Impact (20%):** lead with the citation-backed emission factors
  (IPCC/EPA/GHG Protocol) — already in the README, now maps to an explicit scored
  criterion, so say it explicitly rather than letting it sit in a footnote.
- **Solution Innovation (30%):** the AI vision + grounded-recommendation layer,
  named explicitly as what's different from a form-based calculator.
- **Technical Feasibility (25%):** one real screenshot or 15-second clip beats a
  paragraph describing the feature — the argument for spending part of the 5 days on
  a thin prototype instead of slides alone.
- **Scalability & Practicality (25%):** the README's own 3-phase roadmap (campus →
  multi-campus SaaS → municipal) — it's already written, just needs a slide.

## 8. Demo/pitch success criteria

- A judge reading the deck can tell, within ~10 seconds per slide, which of the four
  scored criteria that slide is answering.
- At least one real screenshot or short clip — not a mockup.
- The innovation claim is specific ("Gemini reads a tray photo and explains your
  footprint in one line grounded in an EPA factor"), never generic ("we use AI").
- Buffer before the 15th: submission logistics, file formats, and a proofread pass —
  don't build anything new in the final hours.
