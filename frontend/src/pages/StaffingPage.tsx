import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getProject, listProjects } from "../api/projects";
import { getCollaborationPath, recommendStaffing } from "../api/staffing";
import { ApiError } from "../api/client";
import { EmptyState } from "../components/common/EmptyState";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { PageLayout } from "../components/layout/PageLayout";
import { RequiredSkillList } from "../components/projects/RequiredSkillList";
import { CandidateCard } from "../components/staffing/CandidateCard";
import { CollaborationPathView } from "../components/staffing/CollaborationPathView";
import { useApi } from "../hooks/useApi";
import type { CollaborationPathHop, StaffingCandidate } from "../types";

export function StaffingPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const projectId = searchParams.get("projectId") ?? "";

  const projectListState = useApi(() => listProjects({ status: "active", limit: 100 }), []);
  const projectState = useApi(() => (projectId ? getProject(projectId) : Promise.resolve(null)), [projectId]);

  const [candidates, setCandidates] = useState<StaffingCandidate[] | null>(null);
  const [candidatesLoading, setCandidatesLoading] = useState(false);
  const [candidatesError, setCandidatesError] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [paths, setPaths] = useState<Record<string, CollaborationPathHop[]>>({});
  const [pathLoading, setPathLoading] = useState<string | null>(null);
  const [pathError, setPathError] = useState<string | null>(null);

  useEffect(() => {
    setCandidates(null);
    setExpandedId(null);
    setPaths({});
    if (!projectId) return;

    setCandidatesLoading(true);
    setCandidatesError(null);
    recommendStaffing(projectId)
      .then(setCandidates)
      .catch((err) => setCandidatesError(err instanceof ApiError ? err.message : "Something went wrong."))
      .finally(() => setCandidatesLoading(false));
  }, [projectId]);

  function toggleCandidate(candidateId: string) {
    const next = expandedId === candidateId ? null : candidateId;
    setExpandedId(next);
    if (next && !paths[next]) {
      setPathLoading(next);
      setPathError(null);
      getCollaborationPath(next, projectId)
        .then((result) => setPaths((prev) => ({ ...prev, [next]: result })))
        .catch((err) => setPathError(err instanceof ApiError ? err.message : "Something went wrong."))
        .finally(() => setPathLoading(null));
    }
  }

  return (
    <PageLayout
      title="Find Staffing"
      subtitle="Pick a project. We'll rank available people by matching skills and how connected they already are to the team."
      actions={
        <select
          value={projectId}
          onChange={(e) => setSearchParams(e.target.value ? { projectId: e.target.value } : {})}
        >
          <option value="">Select a project…</option>
          {projectListState.data?.items.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
      }
    >
      {!projectId && (
        <EmptyState
          title="No project selected"
          hint="Choose an active project above to see ranked staffing candidates."
        />
      )}

      {projectId && projectState.loading && <LoadingSpinner label="Loading project…" />}
      {projectId && projectState.error && <ErrorBanner message={projectState.error} />}

      {projectId && projectState.data && (
        <>
          <section className="detail-section">
            <h2>Requirements for {projectState.data.project.name}</h2>
            <RequiredSkillList skills={projectState.data.requiredSkills} />
          </section>

          <section className="detail-section">
            <h2>Ranked candidates</h2>
            {candidatesLoading && <LoadingSpinner label="Scoring candidates against the team's collaboration graph…" />}
            {candidatesError && <ErrorBanner message={candidatesError} />}
            {!candidatesLoading && !candidatesError && candidates && (
              candidates.length === 0 ? (
                <EmptyState
                  title="No available candidates match the must-have skills"
                  hint="Every qualified person may already be fully booked or already staffed on this project."
                />
              ) : (
                <div className="candidate-list">
                  {candidates.map((candidate) => (
                    <CandidateCard
                      key={candidate.personId}
                      candidate={candidate}
                      expanded={expandedId === candidate.personId}
                      onToggle={() => toggleCandidate(candidate.personId)}
                      pathContent={
                        <CollaborationPathView
                          loading={pathLoading === candidate.personId}
                          error={expandedId === candidate.personId ? pathError : null}
                          paths={paths[candidate.personId] ?? null}
                        />
                      }
                    />
                  ))}
                </div>
              )
            )}
          </section>
        </>
      )}
    </PageLayout>
  );
}
