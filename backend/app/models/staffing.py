from pydantic import BaseModel


class StaffingCandidate(BaseModel):
    personId: str
    name: str
    title: str
    capacityPct: int
    matchedSkills: list[str]
    directConnections: int
    indirectConnections: int
    connectionScore: int


class CollaborationPathHop(BaseModel):
    teammateId: str
    teammateName: str
    hops: int
    pathNames: list[str]
    pathStrength: int
