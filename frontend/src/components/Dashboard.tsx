import { useEffect, useState } from "react";
import type { FootprintResult, OnboardingAnswers, Strategy } from "../types";
import CategoryBreakdown from "./CategoryBreakdown";
import MealPhotoUpload from "./MealPhotoUpload";
import RecommendationCard from "./RecommendationCard";
import BenchmarkComparison from "./BenchmarkComparison";
import Leaderboard from "./Leaderboard";
import WhatIfSlider from "./WhatIfSlider";
import ScrollExpand from "./effects/ScrollExpand";
import { getRecommendation } from "../api/recommend";
import campusWoods from "../assets/campus-woods.jpg";

export default function Dashboard({
  initial,
  answers,
  onRestart,
}: {
  initial: FootprintResult;
  answers: OnboardingAnswers;
  onRestart: () => void;
}) {
  const [result, setResult] = useState(initial);
  const [strategies, setStrategies] = useState<Strategy[] | null>(null);
  const [recLoading, setRecLoading] = useState(true);
  const [recMock, setRecMock] = useState(false);

  useEffect(() => {
    setRecLoading(true);
    getRecommendation(result.total_kg_co2e, result.by_category)
      .then((r) => {
        setStrategies(r.strategies);
        setRecMock(r.is_mock);
      })
      .catch(() => setStrategies(null))
      .finally(() => setRecLoading(false));
  }, [result.total_kg_co2e]);

  function handleMealLogged(kgCo2e: number) {
    setResult((prev) => ({
      ...prev,
      total_kg_co2e: prev.total_kg_co2e + kgCo2e,
      by_category: { ...prev.by_category, food: (prev.by_category.food ?? 0) + kgCo2e },
    }));
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="rounded-2xl overflow-hidden -mt-2 mb-2" style={{ height: 280 }}>
        <ScrollExpand
          src={campusWoods}
          alt="Wooded stream connecting the campus lakes, IIT Guwahati"
          title="Your Campus Footprint"
          scrollHint="scroll to reveal"
          useWindowScroll
          scrollDistance={0.6}
          holdDistance={0.1}
          startWidth={100}
          startHeight={40}
          startRadius={16}
          endRadius={16}
          mediaZoom={1.2}
          overlayScrim={0.35}
        />
      </div>

      <div className="flex items-baseline justify-between">
        <div>
          <p className="font-data text-xs uppercase tracking-wider text-ink/50">
            Today's footprint
          </p>
          <p className="font-display text-5xl font-semibold text-moss">
            {result.total_kg_co2e.toFixed(1)}
            <span className="text-lg font-normal text-ink/50 ml-2">kg CO2e</span>
          </p>
        </div>
        <button className="text-sm text-river underline" onClick={onRestart}>
          Start over
        </button>
      </div>

      <div className="bg-white/60 rounded-2xl p-6 border border-moss/10">
        <h3 className="font-display text-lg font-semibold mb-3">By category</h3>
        <CategoryBreakdown byCategory={result.by_category} />
      </div>

      <RecommendationCard strategies={strategies} isMock={recMock} loading={recLoading} />

      <BenchmarkComparison totalKgCo2e={result.total_kg_co2e} />

      <WhatIfSlider answers={answers} currentTotalKgCo2e={result.total_kg_co2e} />

      <MealPhotoUpload onLogged={handleMealLogged} />

      <Leaderboard />

      <details className="text-xs text-ink/50">
        <summary className="cursor-pointer font-data">Where these numbers come from</summary>
        <ul className="mt-2 space-y-1 font-data">
          {result.factors_used.map((f, i) => (
            <li key={i}>
              {f.key}: {f.value} {f.unit} × {f.quantity} — {f.source}
            </li>
          ))}
        </ul>
      </details>
    </div>
  );
}
