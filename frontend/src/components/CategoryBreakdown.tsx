import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

const CATEGORY_COLORS: Record<string, string> = {
  transport: "#1F3D2B",
  energy: "#46606B",
  food: "#C98A2C",
  waste: "#B4472A",
};

export default function CategoryBreakdown({ byCategory }: { byCategory: Record<string, number> }) {
  const data = Object.entries(byCategory).map(([category, value]) => ({
    category: category[0].toUpperCase() + category.slice(1),
    key: category,
    value: Number(value.toFixed(2)),
  }));

  return (
    <div className="h-56 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ left: 10, right: 24 }}>
          <XAxis type="number" tick={{ fontFamily: "IBM Plex Mono", fontSize: 12 }} />
          <YAxis
            type="category"
            dataKey="category"
            width={80}
            tick={{ fontFamily: "Inter", fontSize: 13 }}
          />
          <Tooltip
            formatter={(value: number) => [`${value} kg CO2e`, "Subtotal"]}
            contentStyle={{ fontFamily: "IBM Plex Mono", fontSize: 12, borderRadius: 8 }}
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {data.map((entry) => (
              <Cell key={entry.key} fill={CATEGORY_COLORS[entry.key] ?? "#46606B"} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
