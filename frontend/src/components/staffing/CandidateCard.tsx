import type { StaffingCandidate } from "../../types";
import { CapacityPill } from "../people/CapacityPill";
import { SkillBadge } from "../people/SkillBadge";

export function CandidateCard({
  candidate,
  expanded,
  onToggle,
  pathContent,
}: {
  candidate: StaffingCandidate;
  expanded: boolean;
  onToggle: () => void;
  pathContent?: React.ReactNode;
}) {
  return (
    <div className="candidate-card">
      <button className="candidate-card__header" onClick={onToggle} aria-expanded={expanded}>
        <div className="candidate-card__identity">
          <h3 className="candidate-card__name">{candidate.name}</h3>
          <p className="candidate-card__title">{candidate.title}</p>
        </div>
        <div className="candidate-card__stats">
          <CapacityPill capacityPct={candidate.capacityPct} />
          <span className="candidate-card__score" title="Connection score: weighted count of direct + indirect collaboration links to the current team">
            {candidate.connectionScore} connection score
          </span>
          <span className="candidate-card__chevron">{expanded ? "▲" : "▼"}</span>
        </div>
      </button>
      <div className="candidate-card__skills">
        {candidate.matchedSkills.map((skill) => (
          <SkillBadge key={skill} name={skill} emphasis />
        ))}
      </div>
      {expanded && <div className="candidate-card__path">{pathContent}</div>}
    </div>
  );
}
