from __future__ import annotations

import sqlite3
from datetime import date, datetime
from pathlib import Path

from .models import Act


SCHEMA = """
CREATE TABLE IF NOT EXISTS acts (
    id TEXT PRIMARY KEY,
    repertorio TEXT NOT NULL,
    title TEXT NOT NULL,
    typology TEXT NOT NULL,
    requester TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    detail_url TEXT NOT NULL,
    source_url TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_acts_start_date ON acts(start_date);
CREATE INDEX IF NOT EXISTS idx_acts_typology ON acts(typology);
"""


def connect(db_path: str) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def _date_to_str(value: date | None) -> str | None:
    return value.isoformat() if value else None


def _str_to_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def upsert_acts(db_path: str, acts: list[Act]) -> tuple[int, int]:
    """Salva gli atti. Ritorna (nuovi, aggiornati)."""
    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    new_count = 0
    updated_count = 0

    with connect(db_path) as conn:
        for act in acts:
            existing = conn.execute(
                "SELECT content_hash FROM acts WHERE id = ?", (act.stable_id,)
            ).fetchone()

            if existing is None:
                new_count += 1
                conn.execute(
                    """
                    INSERT INTO acts (
                        id, repertorio, title, typology, requester,
                        start_date, end_date, detail_url, source_url,
                        content_hash, first_seen_at, last_seen_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        act.stable_id,
                        act.repertorio,
                        act.title,
                        act.typology,
                        act.requester,
                        _date_to_str(act.start_date),
                        _date_to_str(act.end_date),
                        act.detail_url,
                        act.source_url,
                        act.content_hash,
                        now,
                        now,
                    ),
                )
            else:
                if existing["content_hash"] != act.content_hash:
                    updated_count += 1
                conn.execute(
                    """
                    UPDATE acts
                    SET repertorio = ?, title = ?, typology = ?, requester = ?,
                        start_date = ?, end_date = ?, detail_url = ?, source_url = ?,
                        content_hash = ?, last_seen_at = ?
                    WHERE id = ?
                    """,
                    (
                        act.repertorio,
                        act.title,
                        act.typology,
                        act.requester,
                        _date_to_str(act.start_date),
                        _date_to_str(act.end_date),
                        act.detail_url,
                        act.source_url,
                        act.content_hash,
                        now,
                        act.stable_id,
                    ),
                )
    return new_count, updated_count


def list_since(db_path: str, since: date) -> list[Act]:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT * FROM acts
            WHERE start_date IS NULL OR start_date >= ?
            ORDER BY COALESCE(start_date, '0001-01-01') DESC, repertorio DESC
            """,
            (since.isoformat(),),
        ).fetchall()

    return [
        Act(
            repertorio=row["repertorio"],
            title=row["title"],
            typology=row["typology"],
            requester=row["requester"],
            start_date=_str_to_date(row["start_date"]),
            end_date=_str_to_date(row["end_date"]),
            detail_url=row["detail_url"],
            source_url=row["source_url"],
            content_hash=row["content_hash"],
        )
        for row in rows
    ]
