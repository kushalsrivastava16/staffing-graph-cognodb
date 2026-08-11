import { apiGet } from "./client";
import type { PersonDetail, PersonListResponse } from "../types";

export function listPeople(params: { skill?: string; department?: string; skip?: number; limit?: number }) {
  return apiGet<PersonListResponse>("/people", params);
}

export function getPerson(personId: string) {
  return apiGet<PersonDetail>(`/people/${personId}`);
}
