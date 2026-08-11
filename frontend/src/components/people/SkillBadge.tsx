export function SkillBadge({
  name,
  detail,
  emphasis = false,
}: {
  name: string;
  detail?: string;
  emphasis?: boolean;
}) {
  return (
    <span className={"skill-badge" + (emphasis ? " skill-badge--emphasis" : "")}>
      {name}
      {detail && <span className="skill-badge__detail">{detail}</span>}
    </span>
  );
}
