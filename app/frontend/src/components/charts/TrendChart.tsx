
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { AccessibleChart } from "./AccessibleChart";
import type { AffordabilityDataPoint } from "@/api/hooks/useAffordabilityData";

interface TrendChartProps {
  data: AffordabilityDataPoint[];
}

export function TrendChart({ data }: TrendChartProps) {
  // Filter out completely missing data for the trend line, but Recharts also handles nulls
  // gracefully if connectNulls={false}, which visually represents the gaps to the user.

  return (
    <AccessibleChart
      title="Purchasing Power Trend"
      description="Historical trend of the Purchasing Power Index. A higher index indicates the income can buy more baskets."
      data={data}
    >
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12, fill: '#475569' }}
            tickMargin={10}
            minTickGap={30}
          />
          <YAxis
            domain={['auto', 'auto']}
            tick={{ fontSize: 12, fill: '#475569' }}
            tickFormatter={(value) => `${value}`}
            width={60}
          />
          <Tooltip
            contentStyle={{ borderRadius: '0.375rem', borderColor: '#e2e8f0', boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)' }}
            formatter={(value: any) => [value ? Number(value).toFixed(2) : "Missing", "Index"]}
            labelStyle={{ fontWeight: 'bold', color: '#0f172a', marginBottom: '0.25rem' }}
          />
          <Line
            type="monotone"
            dataKey="purchasing_power_index"
            stroke="#1d4ed8"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 6, fill: "#1d4ed8" }}
            connectNulls={false} // CRITICAL: Preserves statistical honesty by showing gaps
          />
        </LineChart>
      </ResponsiveContainer>
    </AccessibleChart>
  );
}
