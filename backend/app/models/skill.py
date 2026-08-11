from pydantic import BaseModel


class SkillSummary(BaseModel):
    name: str
    category: str | None = None
    peopleCount: int


class DepartmentSummary(BaseModel):
    name: str
