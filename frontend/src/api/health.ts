import { apiGet } from "./client";

export interface HealthStatus {
  status: "ok" | "database_unavailable";
}

export function getHealth(): Promise<HealthStatus> {
  return apiGet<HealthStatus>("/health");
}
