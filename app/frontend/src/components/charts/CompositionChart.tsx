
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { AccessibleChart } from "./AccessibleChart";
import type { AffordabilityDataPoint } from "@/api/hooks/useAffordabilityData";

interface CompositionChartProps {
  data: AffordabilityDataPoint[];
}

const COLORS = {
  beef: "#b91c1c", // red-700
  pork: "#f59e0b", // amber-500
  chicken: "#eab308", // yellow-500
  eggs: "#fef08a", // yellow-200
};

export function CompositionChart({ data }: CompositionChartProps) {
  // We need to flatten the `components` dictionary for Recharts to consume it easily
  const formattedData = data.map((d) => ({
    date: d.date,
    ...d.components,
  }));

  // Extract unique keys from components
  const keys = Array.from(
    new Set(data.flatMap((d) => Object.keys(d.components || {})))
  );

  return (
    <AccessibleChart
      title="Protein Cost Composition"
      description="Stacked area chart showing the nominal cost breakdown of the protein basket over time in R$."
      data={data}
    >
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={formattedData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12, fill: '#475569' }}
            tickMargin={10}
            minTickGap={30}
          />
          <YAxis
            tick={{ fontSize: 12, fill: '#475569' }}
            tickFormatter={(value) => `R$ ${value}`}
            width={70}
          />
          <Tooltip
            contentStyle={{ borderRadius: '0.375rem', borderColor: '#e2e8f0', boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)' }}
            formatter={(value: any, name: any) => [value ? `R$ ${Number(value).toFixed(2)}` : "Missing", String(name).charAt(0).toUpperCase() + String(name).slice(1)]}
            labelStyle={{ fontWeight: 'bold', color: '#0f172a', marginBottom: '0.25rem' }}
          />
          <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: '12px' }} />
          {keys.map((key) => (
            <Area
              key={key}
              type="monotone"
              dataKey={key}
              stackId="1"
              stroke={COLORS[key as keyof typeof COLORS] || "#94a3b8"}
              fill={COLORS[key as keyof typeof COLORS] || "#cbd5e1"}
              connectNulls={false} // CRITICAL: Show gaps for missing prices
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    </AccessibleChart>
  );
}
