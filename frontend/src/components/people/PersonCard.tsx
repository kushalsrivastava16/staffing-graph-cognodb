import { Link } from "react-router-dom";
import type { PersonSummary } from "../../types";
import { CapacityPill } from "./CapacityPill";

export function PersonCard({ person }: { person: PersonSummary }) {
  return (
    <Link to={`/people/${person.id}`} className="card card--link">
      <div className="card__top-row">
        <h3 className="card__title">{person.name}</h3>
        <CapacityPill capacityPct={person.capacityPct} />
      </div>
      <p className="card__subtitle">{person.title}</p>
      <p className="card__meta">{person.location}</p>
    </Link>
  );
}
