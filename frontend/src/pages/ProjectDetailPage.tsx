import { Link, useNavigate, useParams } from "react-router-dom";
import { getProject } from "../api/projects";
import { EmptyState } from "../components/common/EmptyState";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { PageLayout } from "../components/layout/PageLayout";
import { RequiredSkillList } from "../components/projects/RequiredSkillList";
import { StatusPill } from "../components/projects/StatusPill";
import { useApi } from "../hooks/useApi";

export function ProjectDetailPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const { data, loading, error } = useApi(() => getProject(projectId!), [projectId]);

  if (loading) return <PageLayout title="Loading…"><LoadingSpinner /></PageLayout>;
  if (error) return <PageLayout title="Projects"><ErrorBanner message={error} /></PageLayout>;
  if (!data) return null;

  const { project } = data;

  return (
    <PageLayout
      title={project.name}
      subtitle={`${project.clientName ?? "Unknown client"} · ${project.domain}`}
      actions={<StatusPill status={project.status} />}
    >
      {project.description && <p className="detail-bio">{project.description}</p>}

      <div className="detail-actions">
        <button className="btn btn--primary" onClick={() => navigate(`/staffing?projectId=${project.id}`)}>
          Find staffing for this project
        </button>
      </div>

      <section className="detail-section">
        <h2>Required skills</h2>
        <RequiredSkillList skills={data.requiredSkills} />
      </section>

      <section className="detail-section">
        <h2>Current team</h2>
        {data.team.length === 0 ? (
          <EmptyState title="No one is staffed on this project yet" />
        ) : (
          <ul className="history-list">
            {data.team.map((member) => (
              <li key={member.id} className="history-list__item">
                <Link to={`/people/${member.id}`} className="history-list__title">
                  {member.name}
                </Link>
                <span className="history-list__meta">{member.role}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </PageLayout>
  );
}
