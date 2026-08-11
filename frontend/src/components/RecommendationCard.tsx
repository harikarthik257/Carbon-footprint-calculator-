import type { Strategy } from "../types";
import ParticleText from "./effects/ParticleText";

export default function RecommendationCard({
  strategies,
  isMock,
  loading,
}: {
  strategies: Strategy[] | null;
  isMock: boolean;
  loading: boolean;
}) {
  return (
    <div className="bg-moss text-paper rounded-2xl p-6">
      <div style={{ height: 40, overflow: "hidden" }} className="mb-2 -ml-1">
        <ParticleText
          text="WAYS TO CUT YOUR FOOTPRINT"
          fontSize="0.8rem"
          fontWeight={600}
          fontFamily="'IBM Plex Mono', monospace"
          particleSize={1.6}
          density={2}
          color="#EEF1EA"
          highlightColor="#C98A2C"
          scatter={60}
          gatherDuration={900}
          stagger={140}
          pointerRepel={18}
          repelRadius={50}
          idleDrift={0.3}
          trigger="mount"
          glow={false}
          style={{ height: 40, minHeight: 40 }}
        />
      </div>
      {loading && <p className="font-display text-lg">Thinking it through…</p>}
      {!loading && strategies && (
        <ol className="space-y-3">
          {strategies.map((strategy, i) => (
            <li key={i} className="flex gap-3">
              <span className="font-data text-sm text-paper/50 mt-0.5">{i + 1}</span>
              <div>
                <p className="font-display text-lg leading-snug">{strategy.action}</p>
                <p className="font-data text-xs text-paper/60 mt-0.5">
                  ~{strategy.estimated_savings_kg_co2e_per_day} kg CO2e/day saved
                </p>
              </div>
            </li>
          ))}
        </ol>
      )}
      {isMock && (
        <p className="mt-3 text-xs font-data text-paper/50">
          mock response — connect ANTHROPIC_API_KEY for a live recommendation
        </p>
      )}
    </div>
  );
}
