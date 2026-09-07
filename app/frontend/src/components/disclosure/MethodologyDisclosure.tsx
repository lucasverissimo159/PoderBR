import { useState } from "react";
import type { AffordabilityMeta } from "@/api/hooks/useAffordabilityData";
import { useQualityStatus } from "@/api/hooks/useQualityStatus";
import { ChevronDown, ChevronUp, Info, AlertTriangle } from "lucide-react";

interface MethodologyDisclosureProps {
  meta?: AffordabilityMeta;
}

export function MethodologyDisclosure({ meta }: MethodologyDisclosureProps) {
  const [isOpen, setIsOpen] = useState(false);
  const { data: qualityData } = useQualityStatus();

  const hasIssues = qualityData?.report.issues && qualityData.report.issues.length > 0;

  return (
    <div className="border border-border rounded-md bg-surface my-6">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 focus-ring hover:bg-background transition-colors text-left"
        aria-expanded={isOpen}
        aria-controls="methodology-content"
      >
        <div className="flex items-center space-x-2">
          <Info className="w-5 h-5 text-primary" aria-hidden="true" />
          <h2 className="text-lg font-semibold text-text-primary">Data Sources & Methodology</h2>
          {hasIssues && (
            <span className="flex items-center ml-2 px-2 py-0.5 bg-yellow-100 text-yellow-800 text-xs font-medium rounded-full">
              <AlertTriangle className="w-3 h-3 mr-1" />
              Data Quality Warning
            </span>
          )}
        </div>
        {isOpen ? (
          <ChevronUp className="w-5 h-5 text-text-secondary" aria-hidden="true" />
        ) : (
          <ChevronDown className="w-5 h-5 text-text-secondary" aria-hidden="true" />
        )}
      </button>

      {isOpen && (
        <div id="methodology-content" className="p-4 border-t border-border space-y-4 text-sm text-text-secondary leading-relaxed">
          <p className="font-medium text-text-primary">
            Disclaimer: This index measures the purchasing power specifically for this predefined protein basket and does not represent overall inflation or total cost of living.
          </p>

          <div>
            <h3 className="font-semibold text-text-primary mb-1">Basket Composition</h3>
            {meta?.basket_id === "protein_v1" ? (
              <ul className="list-disc pl-5 space-y-1">
                <li>Beef (Contrafilé/Coxão Mole): 5kg</li>
                <li>Pork (Pernil/Lombo): 3kg</li>
                <li>Chicken (Frango inteiro/Cortes): 4kg</li>
                <li>Eggs (Ovos brancos): 2 dozen</li>
              </ul>
            ) : (
              <p>Basket definition for {meta?.basket_id} is loaded dynamically.</p>
            )}
          </div>

          <div>
            <h3 className="font-semibold text-text-primary mb-1">Data Sources</h3>
            <ul className="list-disc pl-5 space-y-1">
              <li><strong>Prices:</strong> Nominal price data derived from IBGE SNIPC (Sistema Nacional de Índices de Preços ao Consumidor) and CEPEA/ESALQ.</li>
              <li><strong>Income:</strong> Federal Decree (Minimum Wage) or IBGE PNAD Contínua (Regional Average).</li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-text-primary mb-1">Uncertainty Markers</h3>
            <p>
              Missing data points for nominal prices or incomes result in <strong>Missing</strong> quality flags. The platform does not silently impute or interpolate data. Partial baskets (where 1 or more proteins are missing) are not calculated.
            </p>
          </div>

          {hasIssues && (
            <div className="bg-yellow-50 border border-yellow-200 p-3 rounded-md mt-4">
              <h3 className="font-semibold text-yellow-800 mb-2 flex items-center">
                <AlertTriangle className="w-4 h-4 mr-1" />
                Active Quality Issues
              </h3>
              <ul className="list-disc pl-5 space-y-1 text-yellow-800">
                {qualityData.report.issues.map((issue, idx) => (
                  <li key={idx}>
                    <strong>{issue.category}:</strong> {issue.message}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {meta?.last_updated && (
            <p className="text-xs mt-4 pt-4 border-t border-border">
              Last updated: {new Date(meta.last_updated).toLocaleString()}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
