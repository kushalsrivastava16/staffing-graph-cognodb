import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Home", end: true },
  { to: "/people", label: "People" },
  { to: "/projects", label: "Projects" },
  { to: "/staffing", label: "Find Staffing" },
];

export function NavBar() {
  return (
    <header className="navbar">
      <div className="navbar__inner">
        <NavLink to="/" className="navbar__brand" end>
          <span className="navbar__brand-mark">◈</span> Staffing Graph
        </NavLink>
        <nav className="navbar__links">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.end}
              className={({ isActive }) => "navbar__link" + (isActive ? " navbar__link--active" : "")}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
