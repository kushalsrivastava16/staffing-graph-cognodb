"""Loads generated data into CognoDB. Every write here uses parameterised
Cypher via UNWIND batches -- no query string ever has data spliced into it.
"""

CONSTRAINTS = [
    "CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE",
    "CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
    "CREATE CONSTRAINT project_id IF NOT EXISTS FOR (p:Project) REQUIRE p.id IS UNIQUE",
    "CREATE CONSTRAINT client_id IF NOT EXISTS FOR (c:Client) REQUIRE c.id IS UNIQUE",
    "CREATE CONSTRAINT department_name IF NOT EXISTS FOR (d:Department) REQUIRE d.name IS UNIQUE",
]

# Fallback if CognoDB doesn't support CREATE CONSTRAINT syntax identically to
# Neo4j 5.x -- plain indexes still make MERGE lookups fast without requiring
# uniqueness enforcement.
INDEX_FALLBACKS = [
    "CREATE INDEX person_id_idx IF NOT EXISTS FOR (p:Person) ON (p.id)",
    "CREATE INDEX skill_name_idx IF NOT EXISTS FOR (s:Skill) ON (s.name)",
    "CREATE INDEX project_id_idx IF NOT EXISTS FOR (p:Project) ON (p.id)",
    "CREATE INDEX client_id_idx IF NOT EXISTS FOR (c:Client) ON (c.id)",
]

WIPE_ALL = "MATCH (n) DETACH DELETE n"

CREATE_DEPARTMENTS = "UNWIND $rows AS row MERGE (d:Department {name: row.name})"

CREATE_SKILLS = """
UNWIND $rows AS row
MERGE (s:Skill {name: row.name})
SET s.category = row.category
"""

CREATE_CLIENTS = """
UNWIND $rows AS row
MERGE (c:Client {id: row.id})
SET c.name = row.name, c.industry = row.industry
"""

CREATE_PROJECTS = """
UNWIND $rows AS row
MERGE (p:Project {id: row.id})
SET p.name = row.name, p.description = row.description, p.status = row.status,
    p.startDate = row.startDate, p.endDate = row.endDate, p.domain = row.domain
WITH p, row
MATCH (c:Client {id: row.clientId})
MERGE (p)-[:FOR_CLIENT]->(c)
"""

CREATE_PEOPLE = """
UNWIND $rows AS row
MERGE (p:Person {id: row.id})
SET p.name = row.name, p.title = row.title, p.location = row.location,
    p.bio = row.bio, p.email = row.email, p.capacityPct = row.capacityPct
"""

CREATE_HAS_SKILL = """
UNWIND $rows AS row
MATCH (p:Person {id: row.personId})
MATCH (s:Skill {name: row.skillName})
MERGE (p)-[r:HAS_SKILL]->(s)
SET r.proficiency = row.proficiency, r.yearsExperience = row.yearsExperience
"""

CREATE_REQUIRES_SKILL = """
UNWIND $rows AS row
MATCH (proj:Project {id: row.projectId})
MATCH (s:Skill {name: row.skillName})
MERGE (proj)-[r:REQUIRES_SKILL]->(s)
SET r.minProficiency = row.minProficiency, r.priority = row.priority
"""

CREATE_MEMBER_OF = """
UNWIND $rows AS row
MATCH (p:Person {id: row.personId})
MATCH (d:Department {name: row.departmentName})
MERGE (p)-[r:MEMBER_OF]->(d)
"""

CREATE_WORKED_ON = """
UNWIND $rows AS row
MATCH (p:Person {id: row.personId})
MATCH (proj:Project {id: row.projectId})
MERGE (p)-[r:WORKED_ON]->(proj)
SET r.role = row.role, r.startDate = row.startDate, r.endDate = row.endDate,
    r.allocationPct = row.allocationPct
"""

# Materializes COLLABORATED_WITH from co-occurrence on WORKED_ON: any two
# people who share a project get (or strengthen) an undirected edge counting
# how many projects they've overlapped on.
MATERIALIZE_COLLABORATED_WITH = """
MATCH (a:Person)-[:WORKED_ON]->(proj:Project)<-[:WORKED_ON]-(b:Person)
WHERE a.id < b.id
WITH a, b, count(DISTINCT proj) AS projectCount
MERGE (a)-[r:COLLABORATED_WITH]-(b)
SET r.projectCount = projectCount, r.strength = projectCount
"""


def _run_write(session, query, rows):
    if rows:
        session.execute_write(lambda tx: tx.run(query, rows=rows).consume())


def create_constraints(session, log):
    for stmt in CONSTRAINTS:
        try:
            session.execute_write(lambda tx, s=stmt: tx.run(s).consume())
        except Exception as exc:  # noqa: BLE001 -- constraint syntax may not be supported
            log(f"  constraint failed ({exc}); will rely on index fallback")
            for idx_stmt in INDEX_FALLBACKS:
                session.execute_write(lambda tx, s=idx_stmt: tx.run(s).consume())
            return


def wipe(session):
    session.execute_write(lambda tx: tx.run(WIPE_ALL).consume())


def load_all(session, data: dict, log):
    log("Creating departments...")
    _run_write(session, CREATE_DEPARTMENTS, data["departments"])

    log("Creating skills...")
    _run_write(session, CREATE_SKILLS, data["skills"])

    log("Creating clients...")
    _run_write(session, CREATE_CLIENTS, data["clients"])

    log("Creating projects (+ FOR_CLIENT)...")
    _run_write(session, CREATE_PROJECTS, data["projects"])

    log("Creating people...")
    _run_write(session, CREATE_PEOPLE, data["people"])

    log("Creating HAS_SKILL edges...")
    _run_write(session, CREATE_HAS_SKILL, data["has_skill"])

    log("Creating REQUIRES_SKILL edges...")
    _run_write(session, CREATE_REQUIRES_SKILL, data["requires_skill"])

    log("Creating MEMBER_OF edges...")
    _run_write(session, CREATE_MEMBER_OF, data["member_of"])

    log("Creating WORKED_ON edges...")
    _run_write(session, CREATE_WORKED_ON, data["worked_on"])

    log("Materializing COLLABORATED_WITH from shared project history...")
    session.execute_write(lambda tx: tx.run(MATERIALIZE_COLLABORATED_WITH).consume())


def summary(session) -> dict:
    query = """
    MATCH (n) WITH labels(n)[0] AS label, count(*) AS c RETURN label, c
    """
    with session.begin_transaction() as tx:
        node_counts = {r["label"]: r["c"] for r in tx.run(query)}
    rel_query = "MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS c"
    with session.begin_transaction() as tx:
        rel_counts = {r["rel"]: r["c"] for r in tx.run(rel_query)}
    return {"nodes": node_counts, "relationships": rel_counts}
