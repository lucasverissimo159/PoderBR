import { useQuery } from "@tanstack/react-query";
import { apiClient } from "../client";

export interface AffordabilityDataPoint {
  date: string;
  basket_cost: number | null;
  income: number | null;
  income_burden_pct: number | null;
  affordability_ratio: number | null;
  purchasing_power_index: number | null;
  quality_flag: "complete" | "partial" | "estimated" | "missing";
  components: Record<string, number | null>;
}

export interface AffordabilityMeta {
  basket_id: string;
  geography: {
    id: string;
    name: string;
  };
  income_basis: string;
  methodology_version: string;
  last_updated: string;
}

export interface AffordabilityResponse {
  meta: AffordabilityMeta;
  data: AffordabilityDataPoint[];
}

export interface AffordabilityParams {
  basket_id: string;
  geography_id: string;
  income_basis: string;
  start_date?: string;
  end_date?: string;
  base_date?: string;
}

export const fetchAffordabilityData = async (
  params: AffordabilityParams
): Promise<AffordabilityResponse> => {
  return apiClient.fetch<AffordabilityResponse>("/api/v1/affordability", {
    params: {
      ...params,
    },
  });
};

export const useAffordabilityData = (params: AffordabilityParams) => {
  return useQuery({
    queryKey: ["affordability", params],
    queryFn: () => fetchAffordabilityData(params),
    enabled: !!params.basket_id && !!params.geography_id && !!params.income_basis,
  });
};
