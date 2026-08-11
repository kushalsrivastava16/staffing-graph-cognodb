# All queries are parameterised — parameters are passed via the driver, never
# string-concatenated into the Cypher text.
#
# NOTE on a CognoDB compatibility quirk: this instance's Cypher engine does
# not correctly apply a property filter on the *target* node of an
# EXISTS {} subquery or OPTIONAL MATCH when the source node already has
# multiple matches of that relationship type -- it silently ignores the
# filter and returns every match instead (confirmed by direct comparison
# against ground-truth counts). LIST_PEOPLE/COUNT_PEOPLE and
# RECOMMEND_STAFFING below work around this by collecting the full
# unfiltered set first and then filtering via plain list membership
# (`x IN list`), which is unaffected.

HEALTH_CHECK = "RETURN 1 AS ok"

LIST_PEOPLE = """
MATCH (p:Person)
OPTIONAL MATCH (p)-[:HAS_SKILL]->(skillNode:Skill)
OPTIONAL MATCH (p)-[:MEMBER_OF]->(deptNode:Department)
WITH p, collect(DISTINCT skillNode.name) AS skillNames, collect(DISTINCT deptNode.name) AS deptNames
WHERE ($skill IS NULL OR $skill IN skillNames)
  AND ($department IS NULL OR $department IN deptNames)
RETURN p { .id, .name, .title, .location, .capacityPct } AS person
ORDER BY p.name
SKIP $skip LIMIT $limit
"""

COUNT_PEOPLE = """
MATCH (p:Person)
OPTIONAL MATCH (p)-[:HAS_SKILL]->(skillNode:Skill)
OPTIONAL MATCH (p)-[:MEMBER_OF]->(deptNode:Department)
WITH p, collect(DISTINCT skillNode.name) AS skillNames, collect(DISTINCT deptNode.name) AS deptNames
WHERE ($skill IS NULL OR $skill IN skillNames)
  AND ($department IS NULL OR $department IN deptNames)
RETURN count(p) AS total
"""

GET_PERSON_DETAIL = """
MATCH (p:Person {id: $personId})
OPTIONAL MATCH (p)-[hs:HAS_SKILL]->(s:Skill)
OPTIONAL MATCH (p)-[w:WORKED_ON]->(proj:Project)-[:FOR_CLIENT]->(c:Client)
OPTIONAL MATCH (p)-[cw:COLLABORATED_WITH]-(colleague:Person)
OPTIONAL MATCH (p)-[:MEMBER_OF]->(dept:Department)
RETURN p { .id, .name, .title, .bio, .location, .capacityPct, .email } AS person,
       dept.name AS department,
       [x IN collect(DISTINCT CASE WHEN s IS NULL THEN NULL ELSE
         { skill: s.name, category: s.category, proficiency: hs.proficiency, years: hs.yearsExperience }
       END) WHERE x IS NOT NULL] AS skills,
       [x IN collect(DISTINCT CASE WHEN proj IS NULL THEN NULL ELSE
         { id: proj.id, project: proj.name, role: w.role, client: c.name, startDate: w.startDate, endDate: w.endDate }
       END) WHERE x IS NOT NULL] AS projects,
       [x IN collect(DISTINCT CASE WHEN colleague IS NULL THEN NULL ELSE
         { id: colleague.id, name: colleague.name, title: colleague.title, projectCount: cw.projectCount }
       END) WHERE x IS NOT NULL] AS collaborators
"""

LIST_PROJECTS = """
MATCH (proj:Project)-[:FOR_CLIENT]->(c:Client)
WHERE ($status IS NULL OR proj.status = $status)
  AND ($domain IS NULL OR proj.domain = $domain)
RETURN proj { .id, .name, .description, .status, .startDate, .endDate, .domain } AS project,
       c.name AS clientName
ORDER BY proj.startDate DESC
SKIP $skip LIMIT $limit
"""

COUNT_PROJECTS = """
MATCH (proj:Project)
WHERE ($status IS NULL OR proj.status = $status)
  AND ($domain IS NULL OR proj.domain = $domain)
RETURN count(proj) AS total
"""

GET_PROJECT_DETAIL = """
MATCH (proj:Project {id: $projectId})-[:FOR_CLIENT]->(c:Client)
OPTIONAL MATCH (proj)-[req:REQUIRES_SKILL]->(s:Skill)
OPTIONAL MATCH (member:Person)-[w:WORKED_ON]->(proj)
RETURN proj { .id, .name, .description, .status, .startDate, .endDate, .domain } AS project,
       c.name AS clientName,
       [x IN collect(DISTINCT CASE WHEN s IS NULL THEN NULL ELSE
         { skill: s.name, category: s.category, minProficiency: req.minProficiency, priority: req.priority }
       END) WHERE x IS NOT NULL] AS requiredSkills,
       [x IN collect(DISTINCT CASE WHEN member IS NULL THEN NULL ELSE
         { id: member.id, name: member.name, role: w.role }
       END) WHERE x IS NOT NULL] AS team
"""

LIST_SKILLS = """
MATCH (s:Skill)
OPTIONAL MATCH (p:Person)-[:HAS_SKILL]->(s)
RETURN s.name AS name, s.category AS category, count(DISTINCT p) AS peopleCount
ORDER BY s.category, s.name
"""

LIST_DEPARTMENTS = """
MATCH (d:Department)
RETURN d.name AS name
ORDER BY d.name
"""

# Q1 -- multi-hop (3 hop) staffing recommendation. Walks Project -> required
# Skills -> qualified/available Person, then scores each candidate by how
# closely they're already connected (1 or 2 collaboration hops) to the
# project's current team. The current-team id set is precomputed once
# (staffedIds) and every connection check is a plain `IN` membership test
# against it -- see the CognoDB compatibility note above.
RECOMMEND_STAFFING = """
MATCH (proj:Project {id: $projectId})
OPTIONAL MATCH (staffed:Person)-[:WORKED_ON]->(proj)
WITH proj, collect(DISTINCT staffed.id) AS staffedIds
MATCH (proj)-[req:REQUIRES_SKILL]->(skill:Skill)
WHERE req.priority = 'must-have'
MATCH (candidate:Person)-[hs:HAS_SKILL]->(skill)
WHERE hs.proficiency >= req.minProficiency
  AND candidate.capacityPct > 0
  AND NOT candidate.id IN staffedIds
OPTIONAL MATCH (candidate)-[:COLLABORATED_WITH]-(direct:Person)
WITH candidate, skill, staffedIds,
     [x IN collect(DISTINCT direct.id) WHERE x IN staffedIds] AS directHits
OPTIONAL MATCH (candidate)-[:COLLABORATED_WITH]-(bridge:Person)-[:COLLABORATED_WITH]-(indirect:Person)
WHERE bridge <> candidate AND indirect <> candidate
WITH candidate, skill, staffedIds, directHits,
     [x IN collect(DISTINCT indirect.id) WHERE x IN staffedIds AND NOT x IN directHits] AS indirectHits
WITH candidate,
     collect(DISTINCT skill.name) AS matchedSkills,
     size(directHits) AS directConnections,
     size(indirectHits) AS indirectConnections
RETURN candidate.id AS personId, candidate.name AS name, candidate.title AS title,
       candidate.capacityPct AS capacityPct,
       matchedSkills, directConnections, indirectConnections,
       (directConnections * 2 + indirectConnections) AS connectionScore
ORDER BY size(matchedSkills) DESC, connectionScore DESC
LIMIT $limit
"""

# Q2 -- variable-length collaboration path between a candidate and everyone
# currently on the target project's team. This is the "a relational database
# would find awkward" query: unbounded-depth self-joins with cycle avoidance
# and path aggregation are painful as recursive CTEs; here it's one pattern.
COLLABORATION_PATH = """
MATCH (candidate:Person {id: $candidateId})
MATCH (teammate:Person)-[:WORKED_ON]->(:Project {id: $projectId})
WHERE teammate.id <> $candidateId
MATCH path = allShortestPaths((candidate)-[:COLLABORATED_WITH*1..4]-(teammate))
RETURN teammate.id AS teammateId, teammate.name AS teammateName,
       length(path) AS hops,
       [n IN nodes(path) | n.name] AS pathNames,
       reduce(s = 0, r IN relationships(path) | s + r.projectCount) AS pathStrength
ORDER BY hops ASC, pathStrength DESC
"""
