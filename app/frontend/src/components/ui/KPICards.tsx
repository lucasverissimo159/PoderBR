
import type { AffordabilityDataPoint } from "@/api/hooks/useAffordabilityData";
import { AlertCircle } from "lucide-react";

interface KPICardsProps {
  latestData?: AffordabilityDataPoint;
}

export function KPICards({ latestData }: KPICardsProps) {
  if (!latestData) {
    return null;
  }

  const { basket_cost, income_burden_pct, affordability_ratio, quality_flag } = latestData;
  const isMissing = quality_flag === "missing" || quality_flag === "partial";

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4" aria-label="Key Performance Indicators">
      <KPICard
        title="Basket Cost"
        value={isMissing || basket_cost === null ? "Missing" : `R$ ${basket_cost.toFixed(2)}`}
        description="Cost of the protein basket"
        isMissing={isMissing}
      />
      <KPICard
        title="Income Burden"
        value={isMissing || income_burden_pct === null ? "Missing" : `${income_burden_pct.toFixed(2)}%`}
        description="Percentage of income consumed by the basket"
        isMissing={isMissing}
      />
      <KPICard
        title="Affordability Ratio"
        value={isMissing || affordability_ratio === null ? "Missing" : `${affordability_ratio.toFixed(2)}x`}
        description="Number of baskets the income can buy"
        isMissing={isMissing}
      />
    </div>
  );
}

interface KPICardProps {
  title: string;
  value: string | number;
  description: string;
  isMissing: boolean;
}

function KPICard({ title, value, description, isMissing }: KPICardProps) {
  return (
    <div className="p-6 bg-surface border border-border rounded-md shadow-sm flex flex-col justify-between">
      <div>
        <h3 className="text-sm font-medium text-text-secondary">{title}</h3>
        <div className="mt-2 flex items-baseline gap-2">
          <p
            className={`text-3xl font-bold tracking-tight ${
              isMissing ? "text-text-secondary/50 italic" : "text-text-primary"
            }`}
          >
            {value}
          </p>
          {isMissing && (
            <AlertCircle className="w-5 h-5 text-yellow-500" aria-label="Data missing for this period" />
          )}
        </div>
      </div>
      <p className="mt-2 text-xs text-text-secondary">{description}</p>
    </div>
  );
}
