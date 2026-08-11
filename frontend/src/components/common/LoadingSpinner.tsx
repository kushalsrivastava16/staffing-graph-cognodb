export function LoadingSpinner({ label = "Loading…" }: { label?: string }) {
  return (
    <div className="state-block state-block--loading" role="status">
      <div className="spinner" aria-hidden="true" />
      <p>{label}</p>
    </div>
  );
}
