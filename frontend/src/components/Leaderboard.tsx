import { useEffect, useState } from "react";
import { getLeaderboard } from "../api/leaderboard";
import type { LeaderboardResponse } from "../types";
import InfiniteMenu from "./effects/InfiniteMenu";
import type { InfiniteMenuItem } from "./effects/InfiniteMenu";
import brahmaputra from "../assets/hostels/brahmaputra.jpg";
import kapili from "../assets/hostels/kapili.jpg";
import dihing from "../assets/hostels/dihing.jpg";
import manas from "../assets/hostels/manas.jpg";
import umiam from "../assets/hostels/umiam.jpg";

// Each hostel is named after a real Northeast India river or lake — the photo
// and link are the actual namesake, not stock/placeholder art.
const HOSTEL_MEDIA: Record<string, { image: string; link: string }> = {
  "Brahmaputra Hostel": { image: brahmaputra, link: "https://en.wikipedia.org/wiki/Brahmaputra_River" },
  "Kapili Hostel": { image: kapili, link: "https://en.wikipedia.org/wiki/Kopili_River" },
  "Dihing Hostel": { image: dihing, link: "https://en.wikipedia.org/wiki/Burhi_Dihing_River" },
  "Manas Hostel": { image: manas, link: "https://en.wikipedia.org/wiki/Manas_River" },
  "Umiam Hostel": { image: umiam, link: "https://en.wikipedia.org/wiki/Umiam_Lake" },
};

export default function Leaderboard() {
  const [data, setData] = useState<LeaderboardResponse | null>(null);

  useEffect(() => {
    getLeaderboard().then(setData).catch(() => setData(null));
  }, []);

  if (!data) return null;
  const max = Math.max(...data.entries.map((e) => e.avg_kg_co2e_saved_per_day));

  const menuItems: InfiniteMenuItem[] = data.entries
    .filter((entry) => HOSTEL_MEDIA[entry.group_name])
    .map((entry) => ({
      image: HOSTEL_MEDIA[entry.group_name].image,
      link: HOSTEL_MEDIA[entry.group_name].link,
      title: entry.group_name,
      description: `${entry.avg_kg_co2e_saved_per_day.toFixed(1)} kg CO2e/day saved`,
    }));

  return (
    <div className="bg-white/60 rounded-2xl p-6 border border-moss/10">
      <div className="flex items-baseline justify-between mb-4">
        <h3 className="font-display text-lg font-semibold">Hostel leaderboard</h3>
        {data.is_synthetic && (
          <span className="text-xs font-data text-ink/40">illustrative — seed data</span>
        )}
      </div>
      <ul className="space-y-3">
        {data.entries.map((entry, i) => (
          <li key={entry.group_name} className="flex items-center gap-3">
            <span className="font-data text-xs text-ink/40 w-5">{i + 1}</span>
            <span className="flex-1 text-sm">{entry.group_name}</span>
            <div className="w-24 h-2 rounded-full bg-moss/10 overflow-hidden">
              <div
                className="h-full bg-ochre rounded-full"
                style={{ width: `${(entry.avg_kg_co2e_saved_per_day / max) * 100}%` }}
              />
            </div>
            <span className="font-data text-xs w-16 text-right">
              {entry.avg_kg_co2e_saved_per_day.toFixed(1)} kg
            </span>
          </li>
        ))}
      </ul>

      {menuItems.length > 0 && (
        <div className="mt-5">
          <p className="font-data text-xs uppercase tracking-wider text-ink/40 mb-2">
            Drag to explore — each hostel is named for a real NE India river or lake
          </p>
          <div className="rounded-xl overflow-hidden bg-ink" style={{ height: 360 }}>
            <InfiniteMenu items={menuItems} />
          </div>
        </div>
      )}
    </div>
  );
}
