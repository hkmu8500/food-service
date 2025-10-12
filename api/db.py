import os
import sqlite3
from pathlib import Path


def _default_db_path() -> str:
    env_path = os.getenv("SQLITE_DB_PATH")
    if env_path:
        return env_path

    if os.getenv("VERCEL"):
        return "/tmp/database.sqlite"

    return str(Path(__file__).resolve().parent.parent / "database.sqlite")


DB_PATH = _default_db_path()


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db(conn: sqlite3.Connection) -> None:
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                count INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            "INSERT OR IGNORE INTO visits (id, count) VALUES (1, 0)"
        )


def increment_and_get_count(conn: sqlite3.Connection) -> int:
    """Increment the visit counter and return the updated value."""
    with conn:
        conn.execute("UPDATE visits SET count = count + 1 WHERE id = 1")
        cur = conn.execute("SELECT count FROM visits WHERE id = 1")
        row = cur.fetchone()
    return int(row[0]) if row else 0