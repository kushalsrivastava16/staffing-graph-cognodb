import { useState } from "react";
import { listProjects } from "../api/projects";
import { EmptyState } from "../components/common/EmptyState";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { PageLayout } from "../components/layout/PageLayout";
import { ProjectCard } from "../components/projects/ProjectCard";
import { useApi } from "../hooks/useApi";

const PAGE_SIZE = 12;

export function ProjectsPage() {
  const [status, setStatus] = useState("");
  const [page, setPage] = useState(0);

  const { data, loading, error } = useApi(
    () => listProjects({ status: status || undefined, skip: page * PAGE_SIZE, limit: PAGE_SIZE }),
    [status, page],
  );

  return (
    <PageLayout
      title="Projects"
      subtitle="Every engagement in the graph, with its client and required skills."
      actions={
        <div className="filter-row">
          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setPage(0);
            }}
          >
            <option value="">All statuses</option>
            <option value="active">Active</option>
            <option value="upcoming">Upcoming</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      }
    >
      {loading && <LoadingSpinner label="Loading projects…" />}
      {error && <ErrorBanner message={error} />}
      {!loading && !error && data && (
        <>
          {data.items.length === 0 ? (
            <EmptyState title="No projects match this filter" />
          ) : (
            <div className="card-grid">
              {data.items.map((project) => (
                <ProjectCard key={project.id} project={project} />
              ))}
            </div>
          )}
          <div className="pagination">
            <button disabled={page === 0} onClick={() => setPage((p) => Math.max(0, p - 1))}>
              Previous
            </button>
            <span>
              Page {page + 1} of {Math.max(1, Math.ceil(data.total / PAGE_SIZE))}
            </span>
            <button disabled={(page + 1) * PAGE_SIZE >= data.total} onClick={() => setPage((p) => p + 1)}>
              Next
            </button>
          </div>
        </>
      )}
    </PageLayout>
  );
}
