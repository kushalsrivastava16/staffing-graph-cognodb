from collections.abc import Generator
from contextlib import contextmanager

from neo4j import Driver, GraphDatabase, Session
from neo4j.exceptions import AuthError, DriverError

from app.config import get_settings
from app.errors import DatabaseUnavailableError

# Connection-level failures -- can't reach the host (DriverError covers
# ServiceUnavailable/SessionExpired), a DNS resolution ValueError for a bad
# host, a raw socket OSError, or bad credentials (AuthError). Deliberately
# narrower than the full Neo4jError tree so a genuine Cypher bug (bad
# syntax, a constraint violation) still surfaces as a real 500 instead of
# being mislabeled as "database unavailable."
CONNECTIVITY_ERRORS = (DriverError, AuthError, OSError, ValueError)

_driver: Driver | None = None


def get_driver() -> Driver:
    global _driver
    if _driver is None:
        settings = get_settings()
        _driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )
    return _driver


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def verify_connectivity() -> bool:
    try:
        get_driver().verify_connectivity()
        return True
    except CONNECTIVITY_ERRORS:
        return False


@contextmanager
def get_session() -> Generator[Session, None, None]:
    settings = get_settings()
    try:
        with get_driver().session(database=settings.NEO4J_DATABASE) as session:
            yield session
    except CONNECTIVITY_ERRORS as exc:
        raise DatabaseUnavailableError(
            "Could not reach the graph database. Check NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD."
        ) from exc
