"""Generates realistic in-memory staffing-graph data. No DB calls here --
`load.py` is responsible for persisting whatever this module returns.
Deterministic (Faker + random are both seeded) so re-runs during
development and for the demo recording are reproducible.
"""

import random
import uuid
from datetime import date, timedelta

from faker import Faker

SEED = 42

DEPARTMENTS = [
    "Cloud Engineering",
    "Data & AI",
    "Enterprise Applications",
    "Cybersecurity",
    "Digital Experience",
    "Strategy & Consulting",
]

# category -> skills. Kept as a realistic consulting-firm skill taxonomy
# rather than random words, so the seeded graph "reads" as a believable org.
SKILL_TAXONOMY: dict[str, list[str]] = {
    "Cloud": ["AWS", "Azure", "GCP", "Kubernetes", "Terraform", "Docker"],
    "Data & AI": [
        "Python",
        "SQL",
        "Data Engineering",
        "Apache Spark",
        "Power BI",
        "Machine Learning",
        "Prompt Engineering",
    ],
    "Frontend": ["React", "TypeScript", "Angular", "UI/UX Design"],
    "Backend": ["Java", "Node.js", ".NET", "Microservices Architecture"],
    "Enterprise Apps": ["SAP FICO", "SAP MM", "Salesforce", "ServiceNow"],
    "Security": ["Cybersecurity", "Identity & Access Management", "Penetration Testing"],
    "Consulting": [
        "Change Management",
        "Agile Coaching",
        "Stakeholder Management",
        "Business Analysis",
    ],
}

# archetype -> (primary skill pool weight 3x, secondary pool weight 1x, department)
PERSONA_POOLS: dict[str, dict] = {
    "cloud_engineer": {"primary": "Cloud", "secondary": "Backend", "department": "Cloud Engineering"},
    "data_scientist": {"primary": "Data & AI", "secondary": "Consulting", "department": "Data & AI"},
    "frontend_dev": {"primary": "Frontend", "secondary": "Backend", "department": "Digital Experience"},
    "backend_dev": {"primary": "Backend", "secondary": "Cloud", "department": "Digital Experience"},
    "enterprise_consultant": {
        "primary": "Enterprise Apps",
        "secondary": "Consulting",
        "department": "Enterprise Applications",
    },
    "security_specialist": {"primary": "Security", "secondary": "Cloud", "department": "Cybersecurity"},
    "business_consultant": {
        "primary": "Consulting",
        "secondary": "Data & AI",
        "department": "Strategy & Consulting",
    },
}

CLIENTS = [
    ("Meridian Retail Group", "Retail"),
    ("Northbridge Bank", "Banking"),
    ("Atlas Insurance Co.", "Insurance"),
    ("Vantage Telecom", "Telecom"),
    ("Horizon Public Health Authority", "Public Sector"),
    ("Summit Manufacturing", "Manufacturing"),
    ("Beacon Logistics", "Logistics"),
    ("Cascade Energy", "Energy"),
    ("Pinecrest Healthcare", "Healthcare"),
    ("Ironclad Defense Systems", "Public Sector"),
    ("Lumen Media Group", "Media"),
    ("Anchor Retail Bank", "Banking"),
]

PROJECT_TEMPLATES = [
    "{client} Core Platform Modernization",
    "{client} Cloud Migration Program",
    "{client} Data Platform & Analytics Rollout",
    "{client} Customer Experience Redesign",
    "{client} Claims/Ops Process Automation",
    "{client} Identity & Access Overhaul",
    "{client} Enterprise Resource Planning Upgrade",
    "{client} AI-Assisted Support Rollout",
    "{client} Regulatory Compliance Remediation",
    "{client} Digital Storefront Relaunch",
]

STATUSES = ["active", "active", "active", "completed", "completed", "upcoming"]


def _all_skills() -> list[dict]:
    return [
        {"name": name, "category": category}
        for category, names in SKILL_TAXONOMY.items()
        for name in names
    ]


def _random_date(fake: Faker, start_years_ago: int, end_years_ago: int) -> date:
    start = fake.date_between(start_date=f"-{start_years_ago}y", end_date=f"-{end_years_ago}y")
    return start


def generate(num_people: int = 150) -> dict:
    fake = Faker()
    Faker.seed(SEED)
    random.seed(SEED)

    skills = _all_skills()
    skills_by_category: dict[str, list[str]] = {}
    for s in skills:
        skills_by_category.setdefault(s["category"], []).append(s["name"])

    departments = [{"name": d} for d in DEPARTMENTS]

    clients = [{"id": str(uuid.uuid4()), "name": name, "industry": industry} for name, industry in CLIENTS]

    projects = []
    requires_skill_edges = []
    for client in clients:
        num_projects = random.randint(2, 4)
        templates = random.sample(PROJECT_TEMPLATES, k=num_projects)
        for template in templates:
            project_id = str(uuid.uuid4())
            status = random.choice(STATUSES)
            start = _random_date(fake, 3, 0)
            end = None
            if status == "completed":
                end = start + timedelta(days=random.randint(120, 540))
            elif status == "active":
                end = start + timedelta(days=random.randint(200, 600))
            projects.append(
                {
                    "id": project_id,
                    "name": template.format(client=client["name"].split(" ")[0]),
                    "description": f"{template.format(client=client['name'])} for {client['industry']} operations.",
                    "status": status,
                    "startDate": start.isoformat(),
                    "endDate": end.isoformat() if end else None,
                    "domain": client["industry"],
                    "clientId": client["id"],
                }
            )
            required_categories = random.sample(list(SKILL_TAXONOMY.keys()), k=random.randint(2, 4))
            for category in required_categories:
                skill_name = random.choice(skills_by_category[category])
                requires_skill_edges.append(
                    {
                        "projectId": project_id,
                        "skillName": skill_name,
                        "minProficiency": random.randint(2, 4),
                        "priority": random.choices(["must-have", "nice-to-have"], weights=[0.7, 0.3])[0],
                    }
                )

    people = []
    has_skill_edges = []
    member_of_edges = []
    archetypes = list(PERSONA_POOLS.keys())

    for _ in range(num_people):
        person_id = str(uuid.uuid4())
        archetype = random.choice(archetypes)
        pool = PERSONA_POOLS[archetype]
        primary_pool = skills_by_category[pool["primary"]]
        secondary_pool = skills_by_category[pool["secondary"]]

        chosen_primary = random.sample(primary_pool, k=min(len(primary_pool), random.randint(2, 4)))
        chosen_secondary = random.sample(secondary_pool, k=min(len(secondary_pool), random.randint(1, 2)))

        for skill_name in chosen_primary:
            has_skill_edges.append(
                {
                    "personId": person_id,
                    "skillName": skill_name,
                    "proficiency": random.randint(3, 5),
                    "yearsExperience": round(random.uniform(1, 10), 1),
                }
            )
        for skill_name in chosen_secondary:
            has_skill_edges.append(
                {
                    "personId": person_id,
                    "skillName": skill_name,
                    "proficiency": random.randint(1, 4),
                    "yearsExperience": round(random.uniform(0.5, 5), 1),
                }
            )

        titles = {
            "cloud_engineer": ["Cloud Engineer", "Senior Cloud Architect", "DevOps Engineer"],
            "data_scientist": ["Data Scientist", "Data Engineer", "AI/ML Consultant"],
            "frontend_dev": ["Frontend Engineer", "UI Developer", "Digital Experience Consultant"],
            "backend_dev": ["Backend Engineer", "Software Engineer", "Solutions Architect"],
            "enterprise_consultant": ["SAP Consultant", "Enterprise Applications Analyst", "ERP Lead"],
            "security_specialist": ["Security Engineer", "Cybersecurity Consultant", "IAM Specialist"],
            "business_consultant": ["Management Consultant", "Business Analyst", "Change Manager"],
        }
        people.append(
            {
                "id": person_id,
                "name": fake.name(),
                "title": random.choice(titles[archetype]),
                "location": f"{fake.city()}, {fake.country_code()}",
                "bio": fake.sentence(nb_words=12),
                "email": fake.unique.email(),
                "capacityPct": random.choices([0, 20, 50, 80, 100], weights=[0.15, 0.15, 0.2, 0.25, 0.25])[0],
            }
        )
        member_of_edges.append({"personId": person_id, "departmentName": pool["department"]})

    worked_on_edges = []
    roles = ["Team Lead", "Senior Consultant", "Consultant", "Engineer", "Architect", "Analyst"]
    for project in projects:
        team_size = random.randint(4, 9)
        team = random.sample(people, k=team_size)
        p_start = date.fromisoformat(project["startDate"])
        for person in team:
            role_start = p_start + timedelta(days=random.randint(0, 30))
            role_end = None
            if project["endDate"]:
                role_end = date.fromisoformat(project["endDate"]) - timedelta(days=random.randint(0, 20))
            worked_on_edges.append(
                {
                    "personId": person["id"],
                    "projectId": project["id"],
                    "role": random.choice(roles),
                    "startDate": role_start.isoformat(),
                    "endDate": role_end.isoformat() if role_end else None,
                    "allocationPct": random.choice([25, 50, 75, 100]),
                }
            )

    return {
        "departments": departments,
        "skills": skills,
        "clients": clients,
        "projects": projects,
        "people": people,
        "has_skill": has_skill_edges,
        "requires_skill": requires_skill_edges,
        "member_of": member_of_edges,
        "worked_on": worked_on_edges,
    }
