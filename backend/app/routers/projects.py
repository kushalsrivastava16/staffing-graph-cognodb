from fastapi import APIRouter, Query

from app.models.project import ProjectDetail, ProjectListResponse
from app.services import graph_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=ProjectListResponse)
def list_projects(
    status: str | None = Query(default=None),
    domain: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    return graph_service.list_projects(status, domain, skip, limit)


@router.get("/{project_id}", response_model=ProjectDetail)
def get_project(project_id: str):
    return graph_service.get_project_detail(project_id)
