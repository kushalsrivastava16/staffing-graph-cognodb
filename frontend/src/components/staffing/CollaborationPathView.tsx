import type { CollaborationPathHop } from "../../types";
import { EmptyState } from "../common/EmptyState";
import { LoadingSpinner } from "../common/LoadingSpinner";

export function CollaborationPathView({
  loading,
  error,
  paths,
}: {
  loading: boolean;
  error: string | null;
  paths: CollaborationPathHop[] | null;
}) {
  if (loading) return <LoadingSpinner label="Tracing collaboration paths…" />;
  if (error) return <p className="error-inline">{error}</p>;
  if (!paths || paths.length === 0) {
    return (
      <EmptyState
        title="No collaboration path to the current team"
        hint="This candidate hasn't previously worked with anyone on the project team, directly or through a mutual colleague."
      />
    );
  }

  return (
    <div className="path-list">
      <p className="path-list__caption">How this candidate connects to the current team:</p>
      {paths.map((p) => (
        <div key={p.teammateId} className="path-chain">
          {p.pathNames.map((name, i) => (
            <span key={i} className="path-chain__node-wrap">
              <span className="path-chain__node">{name}</span>
              {i < p.pathNames.length - 1 && <span className="path-chain__connector">→</span>}
            </span>
          ))}
          <span className="path-chain__hops">
            {p.hops} hop{p.hops === 1 ? "" : "s"}
          </span>
        </div>
      ))}
    </div>
  );
}
