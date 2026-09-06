import type { AffordabilityDataPoint } from "@/api/hooks/useAffordabilityData";

interface DataTableProps {
  data: AffordabilityDataPoint[];
  caption: string;
}

export function DataTable({ data, caption }: DataTableProps) {
  if (!data || data.length === 0) return null;

  return (
    <div className="overflow-x-auto border border-border rounded-md my-4">
      <table className="w-full text-sm text-left text-text-primary">
        <caption className="p-4 font-semibold text-lg bg-surface border-b border-border text-left">
          {caption}
        </caption>
        <thead className="text-xs uppercase bg-background text-text-secondary">
          <tr>
            <th scope="col" className="px-6 py-3">Date</th>
            <th scope="col" className="px-6 py-3 text-right">Basket Cost (R$)</th>
            <th scope="col" className="px-6 py-3 text-right">Income (R$)</th>
            <th scope="col" className="px-6 py-3 text-right">Burden (%)</th>
            <th scope="col" className="px-6 py-3 text-right">Affordability Ratio</th>
            <th scope="col" className="px-6 py-3 text-right">Purchasing Power Index</th>
            <th scope="col" className="px-6 py-3">Quality</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr
              key={row.date}
              className={i % 2 === 0 ? "bg-surface" : "bg-background/50"}
            >
              <th scope="row" className="px-6 py-4 font-medium whitespace-nowrap">
                {row.date}
              </th>
              <td className="px-6 py-4 text-right">
                {row.basket_cost !== null ? row.basket_cost.toFixed(2) : "-"}
              </td>
              <td className="px-6 py-4 text-right">
                {row.income !== null ? row.income.toFixed(2) : "-"}
              </td>
              <td className="px-6 py-4 text-right">
                {row.income_burden_pct !== null ? row.income_burden_pct.toFixed(2) : "-"}
              </td>
              <td className="px-6 py-4 text-right">
                {row.affordability_ratio !== null ? row.affordability_ratio.toFixed(2) : "-"}
              </td>
              <td className="px-6 py-4 text-right">
                {row.purchasing_power_index !== null ? row.purchasing_power_index.toFixed(2) : "-"}
              </td>
              <td className="px-6 py-4">
                <span
                  className={`inline-block px-2 py-1 text-xs rounded-full ${
                    row.quality_flag === "complete"
                      ? "bg-green-100 text-green-800"
                      : row.quality_flag === "estimated"
                      ? "bg-yellow-100 text-yellow-800"
                      : "bg-red-100 text-red-800"
                  }`}
                >
                  {row.quality_flag}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
