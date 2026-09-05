import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { KPICards } from "./KPICards";
import type { AffordabilityDataPoint } from "@/api/hooks/useAffordabilityData";

describe("KPICards Component", () => {
  const completeData: AffordabilityDataPoint = {
    date: "2024-01-01",
    basket_cost: 250.5,
    income: 1412.0,
    income_burden_pct: 17.74,
    affordability_ratio: 5.63,
    purchasing_power_index: 100.0,
    quality_flag: "complete",
    components: {},
  };

  const missingData: AffordabilityDataPoint = {
    date: "2024-02-01",
    basket_cost: 260.0,
    income: null,
    income_burden_pct: null,
    affordability_ratio: null,
    purchasing_power_index: null,
    quality_flag: "missing",
    components: {},
  };

  it("renders nothing if no data is provided", () => {
    const { container } = render(<KPICards />);
    expect(container.firstChild).toBeNull();
  });

  it("renders formatted metrics when data is complete", () => {
    render(<KPICards latestData={completeData} />);

    expect(screen.getByText("R$ 250.50")).toBeInTheDocument();
    expect(screen.getByText("17.74%")).toBeInTheDocument();
    expect(screen.getByText("5.63x")).toBeInTheDocument();
  });

  it("renders 'Missing' when quality flag is missing or data is null", () => {
    render(<KPICards latestData={missingData} />);

    // Basket cost is available but flag is missing, we still show missing
    // or if we decide to show basket cost anyway, we check the other two
    // Based on implementation: if quality_flag === 'missing', all show missing.
    const missingTexts = screen.getAllByText("Missing");
    expect(missingTexts).toHaveLength(3);
  });
});
