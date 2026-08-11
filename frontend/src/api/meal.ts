import type { LogMealResponse, MealItem, FootprintResult } from "../types";

export async function logMealPhoto(imageBase64: string, mediaType: string): Promise<LogMealResponse> {
  const res = await fetch("/api/log-meal", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image_base64: imageBase64, media_type: mediaType }),
  });
  if (!res.ok) throw new Error(`log-meal failed: ${res.status}`);
  return res.json();
}

export async function calculateMeal(items: MealItem[]): Promise<FootprintResult> {
  const res = await fetch("/api/calculate-meal", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items }),
  });
  if (!res.ok) throw new Error(`calculate-meal failed: ${res.status}`);
  return res.json();
}
