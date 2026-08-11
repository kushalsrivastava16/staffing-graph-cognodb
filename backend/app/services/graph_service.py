from app.db import queries
from app.db.driver import get_session
from app.errors import NotFoundError
from app.models.person import PersonDetail, PersonListResponse, PersonSummary
from app.models.project import ProjectDetail, ProjectListResponse, ProjectSummary
from app.models.skill import DepartmentSummary, SkillSummary
from app.models.staffing import CollaborationPathHop, StaffingCandidate


def list_people(skill: str | None, department: str | None, skip: int, limit: int) -> PersonListResponse:
    params = {"skill": skill, "department": department, "skip": skip, "limit": limit}
    with get_session() as session:
        records = session.execute_read(lambda tx: list(tx.run(queries.LIST_PEOPLE, params)))
        total = session.execute_read(lambda tx: tx.run(queries.COUNT_PEOPLE, params).single()["total"])
    items = [PersonSummary(**r["person"]) for r in records]
    return PersonListResponse(items=items, total=total, skip=skip, limit=limit)


def get_person_detail(person_id: str) -> PersonDetail:
    with get_session() as session:
        record = session.execute_read(
            lambda tx: tx.run(queries.GET_PERSON_DETAIL, {"personId": person_id}).single()
        )
    if record is None or record["person"] is None:
        raise NotFoundError(f"No person with id {person_id}")
    return PersonDetail(
        person=PersonSummary(**record["person"]),
        bio=record["person"].get("bio"),
        email=record["person"].get("email"),
        department=record["department"],
        skills=record["skills"],
        projects=record["projects"],
        collaborators=record["collaborators"],
    )


def list_projects(status: str | None, domain: str | None, skip: int, limit: int) -> ProjectListResponse:
    params = {"status": status, "domain": domain, "skip": skip, "limit": limit}
    with get_session() as session:
        records = session.execute_read(lambda tx: list(tx.run(queries.LIST_PROJECTS, params)))
        total = session.execute_read(lambda tx: tx.run(queries.COUNT_PROJECTS, params).single()["total"])
    items = [ProjectSummary(**r["project"], clientName=r["clientName"]) for r in records]
    return ProjectListResponse(items=items, total=total, skip=skip, limit=limit)


def get_project_detail(project_id: str) -> ProjectDetail:
    with get_session() as session:
        record = session.execute_read(
            lambda tx: tx.run(queries.GET_PROJECT_DETAIL, {"projectId": project_id}).single()
        )
    if record is None or record["project"] is None:
        raise NotFoundError(f"No project with id {project_id}")
    return ProjectDetail(
        project=ProjectSummary(**record["project"], clientName=record["clientName"]),
        requiredSkills=record["requiredSkills"],
        team=record["team"],
    )


def list_skills() -> list[SkillSummary]:
    with get_session() as session:
        records = session.execute_read(lambda tx: list(tx.run(queries.LIST_SKILLS)))
    return [SkillSummary(**r) for r in records]


def list_departments() -> list[DepartmentSummary]:
    with get_session() as session:
        records = session.execute_read(lambda tx: list(tx.run(queries.LIST_DEPARTMENTS)))
    return [DepartmentSummary(**r) for r in records]


def recommend_staffing(project_id: str, limit: int) -> list[StaffingCandidate]:
    with get_session() as session:
        records = session.execute_read(
            lambda tx: list(tx.run(queries.RECOMMEND_STAFFING, {"projectId": project_id, "limit": limit}))
        )
    return [StaffingCandidate(**r) for r in records]


def get_collaboration_path(candidate_id: str, project_id: str) -> list[CollaborationPathHop]:
    with get_session() as session:
        records = session.execute_read(
            lambda tx: list(
                tx.run(queries.COLLABORATION_PATH, {"candidateId": candidate_id, "projectId": project_id})
            )
        )
    return [CollaborationPathHop(**r) for r in records]
