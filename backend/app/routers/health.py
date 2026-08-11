from fastapi import APIRouter

from app.db.driver import verify_connectivity

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    healthy = verify_connectivity()
    return {"status": "ok" if healthy else "database_unavailable"}
