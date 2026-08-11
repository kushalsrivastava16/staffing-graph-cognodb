import { useState } from "react";
import { listPeople } from "../api/people";
import { listDepartments, listSkills } from "../api/skills";
import { EmptyState } from "../components/common/EmptyState";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { PageLayout } from "../components/layout/PageLayout";
import { PersonCard } from "../components/people/PersonCard";
import { useApi } from "../hooks/useApi";

const PAGE_SIZE = 12;

export function PeoplePage() {
  const [skill, setSkill] = useState("");
  const [department, setDepartment] = useState("");
  const [page, setPage] = useState(0);

  const skillsState = useApi(() => listSkills(), []);
  const departmentsState = useApi(() => listDepartments(), []);
  const peopleState = useApi(
    () => listPeople({ skill: skill || undefined, department: department || undefined, skip: page * PAGE_SIZE, limit: PAGE_SIZE }),
    [skill, department, page],
  );

  function updateFilter(setter: (v: string) => void, value: string) {
    setter(value);
    setPage(0);
  }

  return (
    <PageLayout
      title="People"
      subtitle="Browse the bench. Filter by skill or department to narrow things down."
      actions={
        <div className="filter-row">
          <select value={skill} onChange={(e) => updateFilter(setSkill, e.target.value)}>
            <option value="">All skills</option>
            {skillsState.data?.map((s) => (
              <option key={s.name} value={s.name}>
                {s.name} ({s.peopleCount})
              </option>
            ))}
          </select>
          <select value={department} onChange={(e) => updateFilter(setDepartment, e.target.value)}>
            <option value="">All departments</option>
            {departmentsState.data?.map((d) => (
              <option key={d.name} value={d.name}>
                {d.name}
              </option>
            ))}
          </select>
        </div>
      }
    >
      {peopleState.loading && <LoadingSpinner label="Loading people…" />}
      {peopleState.error && (
        <ErrorBanner message={peopleState.error} onRetry={() => setPage((p) => p)} />
      )}
      {!peopleState.loading && !peopleState.error && peopleState.data && (
        <>
          {peopleState.data.items.length === 0 ? (
            <EmptyState title="No one matches these filters" hint="Try clearing the skill or department filter." />
          ) : (
            <div className="card-grid">
              {peopleState.data.items.map((person) => (
                <PersonCard key={person.id} person={person} />
              ))}
            </div>
          )}
          <div className="pagination">
            <button disabled={page === 0} onClick={() => setPage((p) => Math.max(0, p - 1))}>
              Previous
            </button>
            <span>
              Page {page + 1} of {Math.max(1, Math.ceil(peopleState.data.total / PAGE_SIZE))}
            </span>
            <button
              disabled={(page + 1) * PAGE_SIZE >= peopleState.data.total}
              onClick={() => setPage((p) => p + 1)}
            >
              Next
            </button>
          </div>
        </>
      )}
    </PageLayout>
  );
}
