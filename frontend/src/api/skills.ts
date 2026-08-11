import { apiGet } from "./client";
import type { DepartmentSummary, SkillSummary } from "../types";

export function listSkills() {
  return apiGet<SkillSummary[]>("/skills");
}

export function listDepartments() {
  return apiGet<DepartmentSummary[]>("/departments");
}
