import { useQuery } from "@tanstack/react-query";
import { apiClient } from "../client";

export interface QualityIssue {
  level: "warning" | "critical";
  category: string;
  message: string;
}

export interface ValidationReport {
  is_healthy: boolean;
  last_evaluated: string;
  issues: QualityIssue[];
}

export interface IngestionStatusSummary {
  source_id: string;
  last_run_status: string;
  last_run_time: string | null;
}

export interface QualityStatusResponse {
  report: ValidationReport;
  ingestion_summary: IngestionStatusSummary[];
}

export const fetchQualityStatus = async (): Promise<QualityStatusResponse> => {
  return apiClient.fetch<QualityStatusResponse>("/api/v1/quality/status");
};

export const useQualityStatus = () => {
  return useQuery({
    queryKey: ["quality-status"],
    queryFn: fetchQualityStatus,
    refetchInterval: 5 * 60 * 1000, // Refresh every 5 minutes
  });
};
