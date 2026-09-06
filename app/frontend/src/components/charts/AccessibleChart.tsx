import React, { useState } from "react";
import { DataTable } from "@/components/ui/DataTable";
import type { AffordabilityDataPoint } from "@/api/hooks/useAffordabilityData";
import { Table, LineChart as LineChartIcon } from "lucide-react";

interface AccessibleChartProps {
  title: string;
  description: string;
  data: AffordabilityDataPoint[];
  children: React.ReactNode; // The actual Recharts component
}

export function AccessibleChart({ title, description, data, children }: AccessibleChartProps) {
  const [showTable, setShowTable] = useState(false);

  return (
    <div className="flex flex-col space-y-4 border border-border p-4 rounded-md bg-surface">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-semibold text-text-primary">{title}</h3>
          <p className="text-sm text-text-secondary">{description}</p>
        </div>
        <button
          onClick={() => setShowTable(!showTable)}
          className="flex items-center space-x-2 px-3 py-1.5 bg-background border border-border rounded-md text-sm font-medium hover:bg-border/50 focus-ring transition-colors"
          aria-pressed={showTable}
        >
          {showTable ? (
            <>
              <LineChartIcon className="w-4 h-4" />
              <span>Show Chart</span>
            </>
          ) : (
            <>
              <Table className="w-4 h-4" />
              <span>Show Table</span>
            </>
          )}
        </button>
      </div>

      <div className="relative w-full h-[400px]">
        {showTable ? (
          <div className="absolute inset-0 overflow-auto bg-surface z-10">
            <DataTable data={data} caption={`${title} data table`} />
          </div>
        ) : (
          <div
            className="w-full h-full"
            role="img"
            aria-label={title}
            aria-describedby={`desc-${title.replace(/\s+/g, '-').toLowerCase()}`}
          >
            {/* Visually hidden description for screen readers */}
            <div id={`desc-${title.replace(/\s+/g, '-').toLowerCase()}`} className="sr-only">
              {description}. Tabular data is available by clicking the "Show Table" button.
            </div>

            {/* Recharts renders its SVG here */}
            {children}
          </div>
        )}
      </div>
    </div>
  );
}
