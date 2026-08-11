import type { RequiredSkill } from "../../types";
import { SkillBadge } from "../people/SkillBadge";

export function RequiredSkillList({ skills }: { skills: RequiredSkill[] }) {
  if (skills.length === 0) return <p className="muted">No skill requirements recorded.</p>;
  return (
    <div className="skill-list">
      {skills.map((s) => (
        <SkillBadge
          key={s.skill}
          name={s.skill}
          detail={`min lvl ${s.minProficiency}`}
          emphasis={s.priority === "must-have"}
        />
      ))}
    </div>
  );
}
