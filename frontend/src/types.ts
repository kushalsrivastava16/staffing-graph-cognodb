export interface PersonSummary {
  id: string;
  name: string;
  title: string;
  location: string;
  capacityPct: number;
}

export interface SkillEntry {
  skill: string;
  category: string | null;
  proficiency: number;
  years: number;
}

export interface ProjectHistoryEntry {
  id: string;
  project: string;
  role: string;
  client: string | null;
  startDate: string;
  endDate: string | null;
}

export interface CollaboratorEntry {
  id: string;
  name: string;
  title: string | null;
  projectCount: number;
}

export interface PersonDetail {
  person: PersonSummary;
  bio: string | null;
  email: string | null;
  department: string | null;
  skills: SkillEntry[];
  projects: ProjectHistoryEntry[];
  collaborators: CollaboratorEntry[];
}

export interface PersonListResponse {
  items: PersonSummary[];
  total: number;
  skip: number;
  limit: number;
}

export interface ProjectSummary {
  id: string;
  name: string;
  description: string | null;
  status: "active" | "completed" | "upcoming";
  startDate: string;
  endDate: string | null;
  domain: string;
  clientName: string | null;
}

export interface RequiredSkill {
  skill: string;
  category: string | null;
  minProficiency: number;
  priority: "must-have" | "nice-to-have";
}

export interface TeamMember {
  id: string;
  name: string;
  role: string;
}

export interface ProjectDetail {
  project: ProjectSummary;
  requiredSkills: RequiredSkill[];
  team: TeamMember[];
}

export interface ProjectListResponse {
  items: ProjectSummary[];
  total: number;
  skip: number;
  limit: number;
}

export interface SkillSummary {
  name: string;
  category: string | null;
  peopleCount: number;
}

export interface DepartmentSummary {
  name: string;
}

export interface StaffingCandidate {
  personId: string;
  name: string;
  title: string;
  capacityPct: number;
  matchedSkills: string[];
  directConnections: number;
  indirectConnections: number;
  connectionScore: number;
}

export interface CollaborationPathHop {
  teammateId: string;
  teammateName: string;
  hops: number;
  pathNames: string[];
  pathStrength: number;
}
