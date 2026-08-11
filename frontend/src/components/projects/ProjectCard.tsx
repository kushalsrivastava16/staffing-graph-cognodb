import { Link } from "react-router-dom";
import type { ProjectSummary } from "../../types";
import { StatusPill } from "./StatusPill";

export function ProjectCard({ project }: { project: ProjectSummary }) {
  return (
    <Link to={`/projects/${project.id}`} className="card card--link">
      <div className="card__top-row">
        <h3 className="card__title">{project.name}</h3>
        <StatusPill status={project.status} />
      </div>
      <p className="card__subtitle">
        {project.clientName} &middot; {project.domain}
      </p>
      <p className="card__meta">
        {project.startDate}
        {project.endDate ? ` – ${project.endDate}` : " – ongoing"}
      </p>
    </Link>
  );
}
