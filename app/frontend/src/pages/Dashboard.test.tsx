import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Dashboard from "./Dashboard";

// Mock the API hook since we are only testing the UI logic
vi.mock("@/api/hooks/useAffordabilityData", () => ({
  useAffordabilityData: vi.fn(() => ({
    data: {
      meta: { basket_id: "test", last_updated: "2024-01-01" },
      data: [{
        date: "2024-01-01",
        basket_cost: 100,
        income: 1000,
        income_burden_pct: 10,
        affordability_ratio: 10,
        purchasing_power_index: 100,
        quality_flag: "complete",
        components: { beef: 50, pork: 20, chicken: 20, eggs: 10 }
      }]
    },
    isLoading: false,
    isError: false,
    refetch: vi.fn(),
  })),
}));

// Mock Recharts to avoid DOM measurement issues in JSDOM
vi.mock("recharts", async () => {
  const OriginalModule = await vi.importActual("recharts");
  return {
    ...OriginalModule,
    ResponsiveContainer: ({ children }: any) => (
      <div style={{ width: 800, height: 400 }}>{children}</div>
    ),
  };
});

describe("Dashboard Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the dashboard title and description", () => {
    render(<Dashboard />);
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText(/Welcome to PoderBR/i)).toBeInTheDocument();
  });

  it("renders the control selectors", () => {
    render(<Dashboard />);
    expect(screen.getByLabelText(/Geography/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Income Basis/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Start Date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/End Date/i)).toBeInTheDocument();
  });

  it("updates geography state when selector changes", () => {
    render(<Dashboard />);
    const geoSelect = screen.getByLabelText(/Geography/i);
    expect(geoSelect).toHaveValue("BR");

    fireEvent.change(geoSelect, { target: { value: "SP" } });
    expect(geoSelect).toHaveValue("SP");
  });

  it("displays the KPI cards when data is loaded", () => {
    render(<Dashboard />);
    expect(screen.getByText("R$ 100.00")).toBeInTheDocument();
    expect(screen.getByText("10.00%")).toBeInTheDocument();
    expect(screen.getByText("10.00x")).toBeInTheDocument();
  });
});
