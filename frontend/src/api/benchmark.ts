import type { BenchmarkResponse } from "../types";

export async function getBenchmark(): Promise<BenchmarkResponse> {
  const res = await fetch("/api/benchmark");
  if (!res.ok) throw new Error(`benchmark failed: ${res.status}`);
  return res.json();
}
