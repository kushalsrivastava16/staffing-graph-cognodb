from pydantic import BaseModel


class ProjectSummary(BaseModel):
    id: str
    name: str
    description: str | None = None
    status: str
    startDate: str
    endDate: str | None = None
    domain: str
    clientName: str | None = None


class RequiredSkill(BaseModel):
    skill: str
    category: str | None = None
    minProficiency: int
    priority: str


class TeamMember(BaseModel):
    id: str
    name: str
    role: str


class ProjectDetail(BaseModel):
    project: ProjectSummary
    requiredSkills: list[RequiredSkill]
    team: list[TeamMember]


class ProjectListResponse(BaseModel):
    items: list[ProjectSummary]
    total: int
    skip: int
    limit: int
