from pydantic import BaseModel


class PersonSummary(BaseModel):
    id: str
    name: str
    title: str
    location: str
    capacityPct: int


class SkillEntry(BaseModel):
    skill: str
    category: str | None = None
    proficiency: int
    years: float


class ProjectHistoryEntry(BaseModel):
    id: str
    project: str
    role: str
    client: str | None = None
    startDate: str
    endDate: str | None = None


class CollaboratorEntry(BaseModel):
    id: str
    name: str
    title: str | None = None
    projectCount: int


class PersonDetail(BaseModel):
    person: PersonSummary
    bio: str | None = None
    email: str | None = None
    department: str | None = None
    skills: list[SkillEntry]
    projects: list[ProjectHistoryEntry]
    collaborators: list[CollaboratorEntry]


class PersonListResponse(BaseModel):
    items: list[PersonSummary]
    total: int
    skip: int
    limit: int
