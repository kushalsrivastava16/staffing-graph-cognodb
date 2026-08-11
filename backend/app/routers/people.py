from fastapi import APIRouter, Query

from app.models.person import PersonDetail, PersonListResponse
from app.services import graph_service

router = APIRouter(prefix="/people", tags=["people"])


@router.get("", response_model=PersonListResponse)
def list_people(
    skill: str | None = Query(default=None),
    department: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    return graph_service.list_people(skill, department, skip, limit)


@router.get("/{person_id}", response_model=PersonDetail)
def get_person(person_id: str):
    return graph_service.get_person_detail(person_id)
