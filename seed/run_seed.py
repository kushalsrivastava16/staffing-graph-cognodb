"""CLI entrypoint for seeding CognoDB with realistic staffing-graph data.

Usage:
    python -m seed.run_seed            # load data (idempotent MERGE-based)
    python -m seed.run_seed --reset    # wipe all nodes first, then reload
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

from seed import data_gen, load

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed CognoDB with staffing graph demo data")
    parser.add_argument("--reset", action="store_true", help="Delete all existing nodes before loading")
    parser.add_argument("--people", type=int, default=150, help="Number of Person nodes to generate")
    args = parser.parse_args()

    load_dotenv(REPO_ROOT / ".env")

    uri = os.environ.get("NEO4J_URI")
    user = os.environ.get("NEO4J_USER")
    password = os.environ.get("NEO4J_PASSWORD")
    database = os.environ.get("NEO4J_DATABASE", "neo4j")

    if not all([uri, user, password]):
        print("Missing NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD. Copy .env.example to .env and fill it in.")
        sys.exit(1)

    def log(msg: str) -> None:
        print(msg)

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
    except Exception as exc:  # noqa: BLE001
        print(f"Could not connect to {uri}: {exc}")
        sys.exit(1)

    with driver.session(database=database) as session:
        if args.reset:
            if input(f"This will DELETE ALL nodes in database '{database}'. Type 'yes' to continue: ") != "yes":
                print("Aborted.")
                sys.exit(1)
            log("Wiping existing data...")
            load.wipe(session)

        log("Creating constraints/indexes...")
        load.create_constraints(session, log)

        log(f"Generating {args.people} people + related graph data...")
        data = data_gen.generate(num_people=args.people)

        load.load_all(session, data, log)

        log("Done. Summary:")
        result = load.summary(session)
        for label, count in sorted(result["nodes"].items()):
            log(f"  ({label}): {count}")
        for rel, count in sorted(result["relationships"].items()):
            log(f"  [{rel}]: {count}")

    driver.close()


if __name__ == "__main__":
    main()
