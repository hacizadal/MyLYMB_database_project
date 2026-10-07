"""Shared helpers: configuration, database connection, UTC timestamps.

Configuration comes from environment variables, optionally loaded from a `.env`
file next to this script (see `.env.example`). Real environment variables win
over `.env`. Defaults match the docker-compose.yml defaults, so the project
works without any `.env` file.
"""
import os
from datetime import datetime, timezone
from pathlib import Path

import pymysql

ROOT = Path(__file__).resolve().parent


def _load_dotenv(path):
    """Tiny KEY=VALUE parser (no inline comments, no export, no interpolation)."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv(ROOT / ".env")


def db_config(with_database=True):
    cfg = {
        "host": os.environ.get("MARIADB_HOST", "127.0.0.1"),
        "port": int(os.environ.get("MARIADB_PORT", "3306")),
        "user": os.environ.get("MARIADB_USER", "root"),
        "password": os.environ.get("MARIADB_ROOT_PASSWORD", "labpass"),
        "charset": "utf8mb4",
    }
    if with_database:
        cfg["database"] = os.environ.get("MARIADB_DATABASE", "schemalab")
    return cfg


def connect(autocommit=True, with_database=True, **extra):
    """Open a PyMySQL connection using the project configuration."""
    return pymysql.connect(autocommit=autocommit, **db_config(with_database), **extra)


def utc_now():
    return datetime.now(timezone.utc)


def utc_now_iso():
    """ISO-8601 UTC with millisecond precision, e.g. 2026-09-30T10:33:44.593+00:00."""
    return utc_now().isoformat(timespec="milliseconds")


def run_sql_file(conn, path):
    """Execute a simple .sql file (statements separated by ';', '--' comments)."""
    lines = [ln for ln in Path(path).read_text(encoding="utf-8").splitlines()
             if not ln.strip().startswith("--")]
    with conn.cursor() as cur:
        for statement in "\n".join(lines).split(";"):
            if statement.strip():
                cur.execute(statement)
