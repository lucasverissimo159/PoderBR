import { useState } from "react";
import { PageTitle, Text } from "@/components/ui/Typography";
import { GeographySelector } from "@/components/controls/GeographySelector";
import { useAffordabilityData } from "@/api/hooks/useAffordabilityData";
import { TrendChart } from "@/components/charts/TrendChart";
import { LoadingState } from "@/components/ui/LoadingState";
import { ErrorState } from "@/components/ui/ErrorState";

export default function Comparison() {
  const [geoA, setGeoA] = useState("BR");
  const [geoB, setGeoB] = useState("SP");

  const queryA = useAffordabilityData({
    basket_id: "protein_v1",
    geography_id: geoA,
    income_basis: "minimum_wage",
  });

  const queryB = useAffordabilityData({
    basket_id: "protein_v1",
    geography_id: geoB,
    income_basis: "minimum_wage",
  });

  return (
    <div className="space-y-6">
      <div>
        <PageTitle>Regional Comparison</PageTitle>
        <Text>
          Compare the purchasing power trend between two different geographies using the national minimum wage.
        </Text>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Region A */}
        <section className="space-y-4 border border-border p-4 rounded-md bg-surface">
          <GeographySelector value={geoA} onChange={setGeoA} />
          {queryA.isLoading && <LoadingState />}
          {queryA.isError && <ErrorState onRetry={() => queryA.refetch()} />}
          {queryA.data?.data && <TrendChart data={queryA.data.data} />}
        </section>

        {/* Region B */}
        <section className="space-y-4 border border-border p-4 rounded-md bg-surface">
          <GeographySelector value={geoB} onChange={setGeoB} />
          {queryB.isLoading && <LoadingState />}
          {queryB.isError && <ErrorState onRetry={() => queryB.refetch()} />}
          {queryB.data?.data && <TrendChart data={queryB.data.data} />}
        </section>
      </div>
    </div>
  );
}
