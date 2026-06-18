import sqlite3
from pathlib import Path
import numpy as np
from .entryObj import entry


def initSQL(db: sqlite3.Connection):
    db.execute("""
        CREATE TABLE IF NOT EXISTS files (
            path         TEXT PRIMARY KEY,
            time_updated TEXT NOT NULL
        );
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id         INTEGER PRIMARY KEY,
            path       TEXT NOT NULL REFERENCES files(path),
            start_line INTEGER,
            end_line   INTEGER,
            raw_text   TEXT NOT NULL,
            embedding  BLOB NOT NULL
        );
    """)
    db.commit()


def getEmbeddings(db: sqlite3.Connection):
    rows = db.execute("SELECT id, start_line, end_line, path, embedding FROM chunks")
    return [
        {
            "id": row[0],
            "start_line": row[1],
            "end_line": row[2],
            "path": Path(row[3]),
            "embedding": np.frombuffer(row[4], dtype=np.float32),
        }
        for row in rows
    ]


def insertAll(db: sqlite3.Connection, entries: list[entry]):
    for ent in entries:
        _insert(
            db,
            ent.path,
            ent.start_line,
            ent.end_line,
            ent.time,
            ent.raw_text,
            ent.embedding,
        )


def _insert(
    db: sqlite3.Connection,
    path: Path,
    start_line: int,
    end_line: int,
    time: str,
    raw_text: str,
    embedding: np.ndarray,
):
    print(f"Inserting {raw_text}")
    db.execute(
        """INSERT INTO chunks (path, file, start_line, end_line, time_updated, raw_text, embedding)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            path,
            path.name,
            start_line,
            end_line,
            time,
            raw_text,
            embedding.astype(np.float32).tobytes(),
        ),
    )
    db.commit()
