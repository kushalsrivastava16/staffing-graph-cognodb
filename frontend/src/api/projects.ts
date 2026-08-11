import { apiGet } from "./client";
import type { ProjectDetail, ProjectListResponse } from "../types";

export function listProjects(params: { status?: string; domain?: string; skip?: number; limit?: number }) {
  return apiGet<ProjectListResponse>("/projects", params);
}

export function getProject(projectId: string) {
  return apiGet<ProjectDetail>(`/projects/${projectId}`);
}
