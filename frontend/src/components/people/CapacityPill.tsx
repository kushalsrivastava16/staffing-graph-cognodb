export function CapacityPill({ capacityPct }: { capacityPct: number }) {
  const level = capacityPct === 0 ? "none" : capacityPct <= 50 ? "low" : "high";
  const label = capacityPct === 0 ? "Fully booked" : `${capacityPct}% available`;
  return <span className={`capacity-pill capacity-pill--${level}`}>{label}</span>;
}
