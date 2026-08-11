from fastapi import APIRouter, Query

from app.models.staffing import CollaborationPathHop, StaffingCandidate
from app.services import graph_service

router = APIRouter(prefix="/staffing", tags=["staffing"])


@router.get("/recommend", response_model=list[StaffingCandidate])
def recommend(project_id: str = Query(..., alias="projectId"), limit: int = Query(default=10, ge=1, le=50)):
    return graph_service.recommend_staffing(project_id, limit)


@router.get("/path", response_model=list[CollaborationPathHop])
def collaboration_path(
    candidate_id: str = Query(..., alias="candidateId"),
    project_id: str = Query(..., alias="projectId"),
):
    return graph_service.get_collaboration_path(candidate_id, project_id)
