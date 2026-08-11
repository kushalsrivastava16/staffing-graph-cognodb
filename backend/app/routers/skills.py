from fastapi import APIRouter

from app.models.skill import DepartmentSummary, SkillSummary
from app.services import graph_service

router = APIRouter(tags=["skills"])


@router.get("/skills", response_model=list[SkillSummary])
def list_skills():
    return graph_service.list_skills()


@router.get("/departments", response_model=list[DepartmentSummary])
def list_departments():
    return graph_service.list_departments()
