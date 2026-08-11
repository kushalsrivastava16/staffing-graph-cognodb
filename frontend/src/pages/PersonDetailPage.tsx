import { Link, useParams } from "react-router-dom";
import { getPerson } from "../api/people";
import { EmptyState } from "../components/common/EmptyState";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { PageLayout } from "../components/layout/PageLayout";
import { CapacityPill } from "../components/people/CapacityPill";
import { SkillBadge } from "../components/people/SkillBadge";
import { useApi } from "../hooks/useApi";

export function PersonDetailPage() {
  const { personId } = useParams<{ personId: string }>();
  const { data, loading, error } = useApi(() => getPerson(personId!), [personId]);

  if (loading) return <PageLayout title="Loading…"><LoadingSpinner /></PageLayout>;
  if (error) return <PageLayout title="People"><ErrorBanner message={error} /></PageLayout>;
  if (!data) return null;

  const { person } = data;

  return (
    <PageLayout
      title={person.name}
      subtitle={`${person.title}${data.department ? ` · ${data.department}` : ""} · ${person.location}`}
      actions={<CapacityPill capacityPct={person.capacityPct} />}
    >
      {data.bio && <p className="detail-bio">{data.bio}</p>}

      <section className="detail-section">
        <h2>Skills</h2>
        {data.skills.length === 0 ? (
          <EmptyState title="No skills recorded" />
        ) : (
          <div className="skill-list">
            {data.skills.map((s) => (
              <SkillBadge key={s.skill} name={s.skill} detail={`lvl ${s.proficiency} · ${s.years}y`} />
            ))}
          </div>
        )}
      </section>

      <section className="detail-section">
        <h2>Project history</h2>
        {data.projects.length === 0 ? (
          <EmptyState title="No project history recorded" />
        ) : (
          <ul className="history-list">
            {data.projects.map((p) => (
              <li key={p.id + p.role} className="history-list__item">
                <Link to={`/projects/${p.id}`} className="history-list__title">
                  {p.project}
                </Link>
                <span className="history-list__meta">
                  {p.role} {p.client && `· ${p.client}`} · {p.startDate}
                  {p.endDate ? ` – ${p.endDate}` : " – ongoing"}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="detail-section">
        <h2>Past collaborators</h2>
        {data.collaborators.length === 0 ? (
          <EmptyState title="No shared-project history with anyone yet" />
        ) : (
          <div className="collaborator-grid">
            {data.collaborators
              .sort((a, b) => b.projectCount - a.projectCount)
              .map((c) => (
                <Link key={c.id} to={`/people/${c.id}`} className="collaborator-chip">
                  {c.name}
                  <span className="collaborator-chip__count">{c.projectCount}x</span>
                </Link>
              ))}
          </div>
        )}
      </section>
    </PageLayout>
  );
}
