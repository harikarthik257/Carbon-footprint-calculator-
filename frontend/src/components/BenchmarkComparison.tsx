import { useEffect, useState } from "react";
import { getBenchmark } from "../api/benchmark";
import type { BenchmarkResponse } from "../types";

export default function BenchmarkComparison({ totalKgCo2e }: { totalKgCo2e: number }) {
  const [benchmark, setBenchmark] = useState<BenchmarkResponse | null>(null);

  useEffect(() => {
    getBenchmark().then(setBenchmark).catch(() => setBenchmark(null));
  }, []);

  if (!benchmark) return null;

  const avg = benchmark.national_avg_kg_co2e_per_day;
  const max = Math.max(totalKgCo2e, avg, 0.01);
  const delta = totalKgCo2e - avg;
  const isAbove = delta > 0.05;
  const isBelow = delta < -0.05;

  return (
    <div className="bg-white/60 rounded-2xl p-6 border border-moss/10">
      <h3 className="font-display text-lg font-semibold mb-3">How you compare</h3>

      <div className="space-y-3">
        <div>
          <div className="flex justify-between text-xs font-data text-ink/50 mb-1">
            <span>You, today</span>
            <span>{totalKgCo2e.toFixed(1)} kg</span>
          </div>
          <div className="h-2 rounded-full bg-moss/10 overflow-hidden">
            <div
              className="h-full bg-ochre rounded-full"
              style={{ width: `${(totalKgCo2e / max) * 100}%` }}
            />
          </div>
        </div>
        <div>
          <div className="flex justify-between text-xs font-data text-ink/50 mb-1">
            <span>India daily average</span>
            <span>{avg.toFixed(1)} kg</span>
          </div>
          <div className="h-2 rounded-full bg-moss/10 overflow-hidden">
            <div
              className="h-full bg-river rounded-full"
              style={{ width: `${(avg / max) * 100}%` }}
            />
          </div>
        </div>
      </div>

      <p className="text-sm mt-3">
        {isAbove && (
          <>You're <span className="font-semibold text-alert">{Math.abs(delta).toFixed(1)} kg</span> above the national daily average.</>
        )}
        {isBelow && (
          <>You're <span className="font-semibold text-moss">{Math.abs(delta).toFixed(1)} kg</span> below the national daily average.</>
        )}
        {!isAbove && !isBelow && <>You're right around the national daily average.</>}
      </p>
      <p className="text-xs font-data text-ink/40 mt-2">{benchmark.source}</p>
    </div>
  );
}
