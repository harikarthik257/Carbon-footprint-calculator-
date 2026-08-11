import type { OnboardingAnswers, FootprintResult } from "../types";

export async function calculateFootprint(answers: OnboardingAnswers): Promise<FootprintResult> {
  const res = await fetch("/api/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(answers),
  });
  if (!res.ok) throw new Error(`calculate failed: ${res.status}`);
  return res.json();
}
