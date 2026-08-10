# Urban Carbon Footprint Calculator

A lightweight, interactive web tool that helps university students and faculty measure their daily carbon footprint and receive personalized, campus-specific reduction strategies.

> Built for campus sustainability. Powered by data. Driven by behavior change.

---

## Problem Statement

Universities and urban communities generate significant greenhouse gas emissions through daily activities such as transportation, energy use, and waste disposal. While quantifying these emissions is a crucial step toward sustainability, individuals often lack accessible, localized tools to measure and understand their personal environmental impact.

**Goal:** Empower students and faculty with clear, data-driven insights about their personal environmental impact, fostering a culture of sustainability and encouraging actionable behavioral changes across campus.

---

## Why This Matters

- Scope 3 indirect emissions (commuting, food, paper, waste) account for **50% to 92%** of total campus carbon footprints at higher education institutions worldwide [1]
- Student and staff commuting alone contributes **18% to 71.5%** of total institutional emissions depending on campus [2][3]
- Students show a "high support but low motivation" paradox: high climate awareness with limited low-carbon behavior [4]
- Generic consumer calculators rely on national averages, take 10 to 25 minutes to complete, and offer no campus-specific guidance [5]

---

## Core Features

### 1. 4-Step Quick Onboarding Quiz
Captures commute method, living situation (dorm vs. off-campus), diet preference, and energy habits. Baseline footprint computed in under 60 seconds.

### 2. Personal Footprint Dashboard
Interactive visual breakdown of total **kg CO₂e** across four categories:

- Transport
- Energy
- Food
- Waste

### 3. Automated Micro-Action Reduction Engine
Personalized recommendations with concrete, measurable CO₂ savings, e.g.:

> "Take the West Campus Shuttle instead of driving: saves 2.4 kg CO₂e/day"

### 4. Campus Carbon Rivalry Leaderboard
Gamified inter-dorm and inter-department rankings that visualize collective carbon savings. Peer-comparison feedback has been shown to reduce energy use by up to 7% [6].

### 5. Hyper-Local Emission Factors
Calculations grounded in IPCC / EPA / GHG Protocol emission coefficients rather than generic national averages [7].

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React / Next.js, Tailwind CSS, Recharts / Chart.js |
| Backend | Python FastAPI (or Node.js) |
| Database | SQLite (MVP) / PostgreSQL (production) |
| Emission Data | IPCC, US EPA, GHG Protocol Scope 1-3 factors |
| Maps (optional) | Leaflet / Mapbox for campus hotspot visualization |
| AI (stretch goal) | Vision model for photo-based dining plate logging |

---

## Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│  React Frontend │ ──► │   FastAPI Backend    │ ──► │  Emission Engine    │
│  Dashboard /    │     │  /api/calculate      │     │  (IPCC / EPA / GHG  │
│  Onboarding /   │ ◄── │  /api/recommend      │     │   Protocol factors) │
│  Leaderboard    │     │  /api/leaderboard    │     │                     │
└─────────────────┘     └──────────────────────┘     └─────────┬───────────┘
                                                               │
                                                    ┌──────────▼──────────┐
                                                    │  User Profiles &    │
                                                    │  Daily Logs (SQLite)│
                                                    └─────────────────────┘
```

---

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-team/campus-carbon-calculator.git
cd campus-carbon-calculator

# 2. Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 3. Frontend
cd ../frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Emission Calculation Methodology

Emissions are estimated using activity-based calculations following the GHG Protocol:

```
Emissions (kg CO₂e) = Activity Data × Emission Factor
```

Examples of emission factors used:

| Activity | Unit | Factor (kg CO₂e) |
| --- | --- | --- |
| Gasoline car commute | per km | ~0.17 |
| Campus shuttle / bus | per km | ~0.10 |
| Electricity (grid) | per kWh | varies by regional grid mix |
| Plant-based meal | per meal | ~0.9 |
| Meat-based meal | per meal | ~3.5 |
| Landfill waste | per kg | ~0.6 |

*Note: MVP factors are seeded from IPCC / EPA / GHG Protocol sources. Production builds should use location-specific grid emission factors.*

---

## MVP Scope (Hackathon Deliverable)

1. ✅ Interactive 4-step onboarding wizard
2. ✅ Personal footprint dashboard with category breakdown
3. ✅ Reduction engine with 3+ personalized micro-actions per user
4. ✅ Campus leaderboard with synthetic demo data
5. ✅ Responsive mobile-first UI

---

## Roadmap

- **Phase 1 - Campus Level:** Deploy to a single university's dormitories and student groups
- **Phase 2 - Multi-Campus SaaS:** License to university sustainability offices for AASHE STARS / Scope 3 reporting
- **Phase 3 - Municipal Level:** Adapt engine for city-wide civic engagement and corporate programs

---

## Team

| Role | Responsibility |
| --- | --- |
| Frontend Engineer | UI components, charts, dashboard, responsive flow |
| Backend Engineer | FastAPI endpoints, calculation logic, data storage |
| Data / Sustainability Analyst | Emission factors, formula models, synthetic datasets |
| UX/UI Designer | Wireframes, visual design, micro-interactions |
| Product Strategist & Pitch Lead | Scope control, pitch deck, presentation |

---

## References

1. Delponte, I., & Costa, V. (2026). Navigating Climate Neutrality Planning. *Future Transportation*. https://doi.org/10.3390/futuretransp6010019
2. Khodayari, A., et al. (2023). Development of Carbon Emission Assessment Tool Towards Promoting Sustainability in Cal State LA. *CSU Journal of Sustainability and Climate Change*. https://doi.org/10.55671/2771-5582.1016
3. Cano, N., et al. (2022). Assessing the carbon footprint of a Colombian University Campus. *Environmental Science and Pollution Research*. https://doi.org/10.1007/s11356-022-22119-4
4. Zhu, W., Li, D., & Liu, W. (2026). From intention to action: Modeling student lifestyle carbon emissions and reduction scenarios. *Cleaner and Responsible Consumption*. https://doi.org/10.1016/j.clrc.2026.100391
5. Sustainability Atlas. (2026). Carbon footprint calculators compared: accuracy, usability, and actionability. https://sustainableatlas.org/post/comparison-carbon-footprint-calculators-accuracy-usability-actionability-1716
6. Eco-Bee: A Personalised Multi-Modal Agent for Advancing Student Climate Awareness and Sustainable Behaviour in Campus Ecosystems. https://doi.org/10.48550/arxiv.2604.15327
7. Auger, C., et al. (2021). Open-Source Carbon Footprint Estimator: Development and University Declination. *Sustainability*. https://doi.org/10.3390/su13084315

---

## License

MIT
