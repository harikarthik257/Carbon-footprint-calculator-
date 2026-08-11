import { useState } from "react";
import type { OnboardingAnswers, TransportMode } from "../types";

export const TRANSPORT_OPTIONS: { value: TransportMode; label: string }[] = [
  { value: "gasoline_car", label: "Personal car" },
  { value: "two_wheeler", label: "Two-wheeler" },
  { value: "shared_auto", label: "Shared auto" },
  { value: "campus_shuttle", label: "Campus shuttle / bus" },
  { value: "cycle_or_walk", label: "Cycle or walk" },
];

const STEPS = ["Transport", "Energy", "Food", "Waste"] as const;

export default function OnboardingWizard({
  onComplete,
}: {
  onComplete: (answers: OnboardingAnswers) => void;
}) {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<OnboardingAnswers>({
    transport: { mode: "campus_shuttle", km_per_day: 4 },
    energy: { kwh_per_day: 2, grid: "national" },
    food: { plant_meals_per_day: 2, meat_meals_per_day: 1 },
    waste: { landfill_kg_per_day: 0.5, composted_kg_per_day: 0, recycled_kg_per_day: 0 },
  });

  const isLast = step === STEPS.length - 1;

  return (
    <div className="max-w-lg mx-auto">
      <div className="flex items-center gap-2 mb-8">
        {STEPS.map((label, i) => (
          <div key={label} className="flex-1">
            <div
              className={`h-1 rounded-full ${i <= step ? "bg-moss" : "bg-moss/20"}`}
            />
            <p
              className={`mt-2 text-xs font-data ${
                i === step ? "text-moss font-semibold" : "text-ink/40"
              }`}
            >
              {String(i + 1).padStart(2, "0")} {label}
            </p>
          </div>
        ))}
      </div>

      <div className="bg-white/60 rounded-2xl p-6 border border-moss/10">
        {step === 0 && (
          <fieldset>
            <legend className="font-display text-xl font-semibold mb-4">
              How do you usually get to campus?
            </legend>
            <div className="space-y-2">
              {TRANSPORT_OPTIONS.map((opt) => (
                <label
                  key={opt.value}
                  className="flex items-center gap-3 p-3 rounded-lg border border-moss/10 cursor-pointer hover:bg-moss/5"
                >
                  <input
                    type="radio"
                    name="transport-mode"
                    checked={answers.transport.mode === opt.value}
                    onChange={() =>
                      setAnswers((a) => ({ ...a, transport: { ...a.transport, mode: opt.value } }))
                    }
                  />
                  {opt.label}
                </label>
              ))}
            </div>
            <label className="block mt-4 text-sm">
              Distance per day (km)
              <input
                type="number"
                min={0}
                className="mt-1 w-full rounded-lg border border-moss/20 p-2 font-data"
                value={answers.transport.km_per_day}
                onChange={(e) =>
                  setAnswers((a) => ({
                    ...a,
                    transport: { ...a.transport, km_per_day: Number(e.target.value) },
                  }))
                }
              />
            </label>
          </fieldset>
        )}

        {step === 1 && (
          <fieldset>
            <legend className="font-display text-xl font-semibold mb-4">
              Roughly how much electricity do you use daily?
            </legend>
            <label className="block text-sm">
              Estimated kWh per day (dorm room ≈ 1–3, off-campus flat ≈ 3–6)
              <input
                type="number"
                min={0}
                className="mt-1 w-full rounded-lg border border-moss/20 p-2 font-data"
                value={answers.energy.kwh_per_day}
                onChange={(e) =>
                  setAnswers((a) => ({
                    ...a,
                    energy: { ...a.energy, kwh_per_day: Number(e.target.value) },
                  }))
                }
              />
            </label>
          </fieldset>
        )}

        {step === 2 && (
          <fieldset>
            <legend className="font-display text-xl font-semibold mb-4">
              How many meals today were which kind?
            </legend>
            <label className="block text-sm mb-3">
              Plant-based meals
              <input
                type="number"
                min={0}
                className="mt-1 w-full rounded-lg border border-moss/20 p-2 font-data"
                value={answers.food.plant_meals_per_day}
                onChange={(e) =>
                  setAnswers((a) => ({
                    ...a,
                    food: { ...a.food, plant_meals_per_day: Number(e.target.value) },
                  }))
                }
              />
            </label>
            <label className="block text-sm">
              Meat / non-veg meals
              <input
                type="number"
                min={0}
                className="mt-1 w-full rounded-lg border border-moss/20 p-2 font-data"
                value={answers.food.meat_meals_per_day}
                onChange={(e) =>
                  setAnswers((a) => ({
                    ...a,
                    food: { ...a.food, meat_meals_per_day: Number(e.target.value) },
                  }))
                }
              />
            </label>
            <p className="mt-3 text-xs text-ink/50">
              Tip: you can log a specific meal precisely with a tray photo from the dashboard.
            </p>
          </fieldset>
        )}

        {step === 3 && (
          <fieldset>
            <legend className="font-display text-xl font-semibold mb-4">
              Waste today (kg, rough estimate is fine)
            </legend>
            <label className="block text-sm mb-3">
              To landfill
              <input
                type="number"
                min={0}
                step={0.1}
                className="mt-1 w-full rounded-lg border border-moss/20 p-2 font-data"
                value={answers.waste.landfill_kg_per_day}
                onChange={(e) =>
                  setAnswers((a) => ({
                    ...a,
                    waste: { ...a.waste, landfill_kg_per_day: Number(e.target.value) },
                  }))
                }
              />
            </label>
          </fieldset>
        )}
      </div>

      <div className="flex justify-between mt-6">
        <button
          className="px-4 py-2 rounded-lg text-sm font-medium text-river disabled:opacity-30"
          disabled={step === 0}
          onClick={() => setStep((s) => s - 1)}
        >
          Back
        </button>
        <button
          className="px-5 py-2 rounded-lg text-sm font-medium bg-moss text-paper hover:bg-moss-light"
          onClick={() => (isLast ? onComplete(answers) : setStep((s) => s + 1))}
        >
          {isLast ? "See my footprint" : "Next"}
        </button>
      </div>
    </div>
  );
}
