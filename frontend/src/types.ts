export type TransportMode =
  | "gasoline_car"
  | "campus_shuttle"
  | "two_wheeler"
  | "cycle_or_walk"
  | "shared_auto";

export interface OnboardingAnswers {
  transport: { mode: TransportMode; km_per_day: number };
  energy: { kwh_per_day: number; grid: "national" | "ne_hydro_weighted" };
  food: { plant_meals_per_day: number; meat_meals_per_day: number };
  waste: { landfill_kg_per_day: number; composted_kg_per_day: number; recycled_kg_per_day: number };
}

export interface FactorUse {
  key: string;
  value: number;
  unit: string;
  source: string;
  quantity: number;
  subtotal_kg_co2e: number;
}

export interface FootprintResult {
  total_kg_co2e: number;
  by_category: Record<string, number>;
  factors_used: FactorUse[];
}

export interface MealItem {
  name: string;
  quantity: number;
  confidence?: "high" | "medium" | "low";
}

export interface LogMealResponse {
  items: MealItem[];
  is_mock: boolean;
  preview_total_kg_co2e: number;
  note: string;
}

export interface Strategy {
  action: string;
  estimated_savings_kg_co2e_per_day: number;
}

export interface RecommendationResponse {
  strategies: Strategy[];
  is_mock: boolean;
}

export interface LeaderboardEntry {
  group_name: string;
  avg_kg_co2e_saved_per_day: number;
}

export interface LeaderboardResponse {
  is_synthetic: boolean;
  entries: LeaderboardEntry[];
}

export interface BenchmarkResponse {
  national_avg_kg_co2e_per_day: number;
  unit: string;
  source: string;
}
