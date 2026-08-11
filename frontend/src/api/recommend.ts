import type { RecommendationResponse } from "../types";

export async function getRecommendation(
  totalKgCo2e: number,
  byCategory: Record<string, number>
): Promise<RecommendationResponse> {
  const res = await fetch("/api/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ total_kg_co2e: totalKgCo2e, by_category: byCategory }),
  });
  if (!res.ok) throw new Error(`recommend failed: ${res.status}`);
  return res.json();
}
