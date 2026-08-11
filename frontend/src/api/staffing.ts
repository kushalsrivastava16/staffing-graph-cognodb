import { apiGet } from "./client";
import type { CollaborationPathHop, StaffingCandidate } from "../types";

export function recommendStaffing(projectId: string, limit = 10) {
  return apiGet<StaffingCandidate[]>("/staffing/recommend", { projectId, limit });
}

export function getCollaborationPath(candidateId: string, projectId: string) {
  return apiGet<CollaborationPathHop[]>("/staffing/path", { candidateId, projectId });
}
