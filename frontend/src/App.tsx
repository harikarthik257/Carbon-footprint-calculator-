import { useState } from "react";
import OnboardingWizard from "./components/OnboardingWizard";
import Dashboard from "./components/Dashboard";
import MaskedHeading from "./components/effects/MaskedHeading";
import { calculateFootprint } from "./api/footprint";
import type { FootprintResult, OnboardingAnswers } from "./types";
import campusHero from "./assets/campus-hero.jpg";

export default function App() {
  const [result, setResult] = useState<FootprintResult | null>(null);
  const [answers, setAnswers] = useState<OnboardingAnswers | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleComplete(newAnswers: OnboardingAnswers) {
    try {
      const res = await calculateFootprint(newAnswers);
      setResult(res);
      setAnswers(newAnswers);
      setError(null);
    } catch {
      setError("Couldn't reach the calculation engine — check the backend is running.");
    }
  }

  return (
    <div className="min-h-screen">
      <header className="relative" style={{ height: 240 }}>
        <div className="relative h-full max-w-3xl mx-auto px-4 flex flex-col justify-center">
          <p className="font-data text-xs uppercase tracking-wider text-river mb-2">
            A Personal Project
          </p>
          <MaskedHeading
            tag="h1"
            text="Campus Carbon"
            src={campusHero}
            className="font-display"
            align="left"
            weight={800}
            textScale={0.12}
            reveal="wipe"
            trigger="mount"
            duration={1.0}
            parallax={20}
            drift={8}
          />
        </div>
      </header>

      <div className="px-4 py-10">
        {error && (
          <p className="max-w-3xl mx-auto mb-4 text-sm text-alert">{error}</p>
        )}

        {!result && <OnboardingWizard onComplete={handleComplete} />}
        {result && answers && (
          <Dashboard initial={result} answers={answers} onRestart={() => setResult(null)} />
        )}
      </div>
    </div>
  );
}
