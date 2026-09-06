
import { PageTitle, Text } from "@/components/ui/Typography";

import { useState } from "react";
import { GeographySelector } from "@/components/controls/GeographySelector";
import { IncomeBasisSelector } from "@/components/controls/IncomeBasisSelector";
import { DateSelector } from "@/components/controls/DateSelector";
import { useAffordabilityData } from "@/api/hooks/useAffordabilityData";
import { KPICards } from "@/components/ui/KPICards";
import { TrendChart } from "@/components/charts/TrendChart";
import { CompositionChart } from "@/components/charts/CompositionChart";
import { MethodologyDisclosure } from "@/components/disclosure/MethodologyDisclosure";
import { LoadingState } from "@/components/ui/LoadingState";
import { ErrorState } from "@/components/ui/ErrorState";
import { EmptyState } from "@/components/ui/EmptyState";

export default function Dashboard() {
  const [geography, setGeography] = useState("BR");
  const [incomeBasis, setIncomeBasis] = useState("minimum_wage");
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");

  const { data, isLoading, isError, refetch } = useAffordabilityData({
    basket_id: "protein_v1",
    geography_id: geography,
    income_basis: incomeBasis,
    start_date: startDate || undefined,
    end_date: endDate || undefined,
  });

  const latestDataPoint = data?.data && data.data.length > 0 ? data.data[data.data.length - 1] : undefined;

  return (
    <div className="space-y-6">
      <div>
        <PageTitle>Dashboard</PageTitle>
        <Text>
          Welcome to PoderBR. Select your geographic region and income basis to see how purchasing power has changed.
        </Text>
      </div>

      <section
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4 bg-surface border border-border rounded-md shadow-sm"
        aria-label="Dashboard Filters"
      >
        <GeographySelector value={geography} onChange={setGeography} />
        <IncomeBasisSelector value={incomeBasis} onChange={setIncomeBasis} />
        <DateSelector id="start-date" label="Start Date" value={startDate} onChange={setStartDate} />
        <DateSelector id="end-date" label="End Date" value={endDate} onChange={setEndDate} />
      </section>

      {isLoading && <LoadingState message="Fetching affordability data..." />}

      {isError && (
        <ErrorState
          title="Failed to load dashboard"
          message="We could not retrieve the affordability index data. Please try again."
          onRetry={() => refetch()}
        />
      )}

      {!isLoading && !isError && data?.data && data.data.length === 0 && (
        <EmptyState
          title="No data found"
          message={`There is no data available for ${geography} from ${startDate || "the beginning"} to ${endDate || "now"}.`}
        />
      )}

      {!isLoading && !isError && data?.data && data.data.length > 0 && (
        <div className="space-y-8 animate-in fade-in duration-500">
          <section aria-labelledby="kpi-heading">
            <h2 id="kpi-heading" className="sr-only">Current Status</h2>
            <KPICards latestData={latestDataPoint} />
          </section>

          <section className="grid grid-cols-1 lg:grid-cols-2 gap-6" aria-label="Charts">
            <TrendChart data={data.data} />
            <CompositionChart data={data.data} />
          </section>

          <MethodologyDisclosure meta={data.meta} />
        </div>
      )}
    </div>
  );
}
