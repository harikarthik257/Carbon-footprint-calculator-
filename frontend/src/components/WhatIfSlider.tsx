import { useEffect, useState } from "react";
import type { OnboardingAnswers, TransportMode } from "../types";
import { TRANSPORT_OPTIONS } from "./OnboardingWizard";
import { calculateFootprint } from "../api/footprint";

const DEBOUNCE_MS = 250;

export default function WhatIfSlider({
  answers,
  currentTotalKgCo2e,
}: {
  answers: OnboardingAnswers;
  currentTotalKgCo2e: number;
}) {
  const [mode, setMode] = useState<TransportMode>(answers.transport.mode);
  const [km, setKm] = useState(answers.transport.km_per_day);
  const [whatIfTotal, setWhatIfTotal] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    const timer = setTimeout(() => {
      calculateFootprint({ ...answers, transport: { mode, km_per_day: km } })
        .then((res) => setWhatIfTotal(res.total_kg_co2e))
        .catch(() => setWhatIfTotal(null))
        .finally(() => setLoading(false));
    }, DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [mode, km, answers]);

  const delta = whatIfTotal === null ? null : currentTotalKgCo2e - whatIfTotal;
  const modeLabel = TRANSPORT_OPTIONS.find((o) => o.value === mode)?.label ?? mode;

  return (
    <div className="bg-white/60 rounded-2xl p-6 border border-moss/10">
      <h3 className="font-display text-lg font-semibold mb-1">What if you changed your commute?</h3>
      <p className="text-sm text-ink/60 mb-4">
        Drag to see how switching transport would change today's footprint.
      </p>

      <label className="block text-sm mb-4">
        Transport mode
        <select
          className="mt-1 w-full rounded-lg border border-moss/20 p-2 font-data bg-white"
          value={mode}
          onChange={(e) => setMode(e.target.value as TransportMode)}
        >
          {TRANSPORT_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label>

      <label className="block text-sm">
        Distance per day: <span className="font-data">{km} km</span>
        <input
          type="range"
          min={0}
          max={30}
          step={1}
          className="mt-2 w-full accent-moss"
          value={km}
          onChange={(e) => setKm(Number(e.target.value))}
        />
      </label>

      <p className="mt-4 font-data text-sm">
        {loading && "Recalculating…"}
        {!loading && delta !== null && delta > 0.001 && (
          <span className="text-moss font-semibold">
            Switching to {modeLabel.toLowerCase()} at {km} km/day would save {delta.toFixed(2)} kg CO2e/day.
          </span>
        )}
        {!loading && delta !== null && delta < -0.001 && (
          <span className="text-alert font-semibold">
            Switching to {modeLabel.toLowerCase()} at {km} km/day would cost {Math.abs(delta).toFixed(2)} kg CO2e/day more.
          </span>
        )}
        {!loading && delta !== null && Math.abs(delta) <= 0.001 && (
          <span className="text-ink/50">No change from today's footprint.</span>
        )}
      </p>
    </div>
  );
}
