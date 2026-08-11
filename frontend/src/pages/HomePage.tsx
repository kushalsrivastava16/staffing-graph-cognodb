import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <main className="page page--home">
      <section className="hero">
        <span className="hero__eyebrow">Consulting bench, as a graph</span>
        <h1 className="hero__title">Staff your next project by who people actually worked with.</h1>
        <p className="hero__lead">
          This is a small demo application backed by a graph database (CognoDB). Instead of just matching
          skills to project requirements, it also looks at who's already{" "}
          <strong>collaborated with the current team</strong> — directly, or through a mutual colleague — so
          staffing suggestions favor people likely to onboard smoothly, not just people who tick a skills box.
        </p>
        <div className="hero__actions">
          <Link to="/staffing" className="btn btn--primary">
            Find staffing for a project
          </Link>
          <Link to="/people" className="btn btn--secondary">
            Browse people
          </Link>
          <Link to="/projects" className="btn btn--secondary">
            Browse projects
          </Link>
        </div>
      </section>

      <section className="home-grid">
        <div className="info-card">
          <h2>Why a graph, not a table?</h2>
          <p>
            Staffing questions are really path questions: "who has the right skills <em>and</em> is within a
            couple of collaboration hops of this team?" That's a natural pattern match in Cypher, and a
            recursive, unbounded-depth self-join in SQL.
          </p>
        </div>
        <div className="info-card">
          <h2>What's underneath</h2>
          <p>
            People, Skills, Projects, Clients and Departments, connected by typed relationships like{" "}
            <code>HAS_SKILL</code>, <code>WORKED_ON</code>, and a materialized <code>COLLABORATED_WITH</code>{" "}
            edge derived from shared project history. See the README for the full model.
          </p>
        </div>
        <div className="info-card">
          <h2>Try it</h2>
          <p>
            Head to <Link to="/staffing">Find Staffing</Link>, pick any active project, and expand a candidate
            to see the actual chain of people connecting them to the team.
          </p>
        </div>
      </section>
    </main>
  );
}
