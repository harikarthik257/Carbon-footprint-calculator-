import type { LeaderboardResponse } from "../types";

export async function getLeaderboard(): Promise<LeaderboardResponse> {
  const res = await fetch("/api/leaderboard");
  if (!res.ok) throw new Error(`leaderboard failed: ${res.status}`);
  return res.json();
}
