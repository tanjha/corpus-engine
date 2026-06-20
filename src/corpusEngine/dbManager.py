import sqlite3
from pathlib import Path
import numpy as np
from .entryObj import entry


def initSQL(db: sqlite3.Connection):
    db.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id      INTEGER PRIMARY KEY,
            path         TEXT UNIQUE NOT NULL,
            time_updated TEXT NOT NULL
        );
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id         INTEGER PRIMARY KEY,
            file_id    INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
            start_line INTEGER,
            end_line   INTEGER,
            raw_text   TEXT NOT NULL,
            embedding  BLOB NOT NULL
        );
    """)
    db.execute("CREATE INDEX IF NOT EXISTS idx_chunks_file_id ON chunks(file_id);")
    db.execute("file_id INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE")
    db.commit()


def getEmbeddings(db: sqlite3.Connection):
    rows = db.execute("""
        SELECT c.id, c.start_line, c.end_line, f.path, c.embedding, c.raw_text
        FROM chunks c
        JOIN files f ON c.file_id = f.id
    """)
    return [
        {
            "id": row[0],
            "start_line": row[1],
            "end_line": row[2],
            "path": Path(row[3]),
            "embedding": np.frombuffer(row[4], dtype=np.float32),
            "raw_text": str(row[5]),
        }
        for row in rows
    ]


def insertFull(db: sqlite3.Connection, entries: list[entry]):
    if entries:
        _insertFile(db, str(entries[0].path.absolute()), entries[0].time)
        print(f"inserting {str(entries[0].path.absolute())}")
        db.commit()
        for ent in entries:
            file_id = _getFileId(db, str(ent.path.absolute()))
            _insertChunk(
                db,
                file_id,
                ent.start_line,
                ent.end_line,
                ent.raw_text,
                ent.embedding,
            )
        db.commit()


def removeAll(db: sqlite3.Connection, paths: list[Path]):
    for path in paths:
        p = str(path)
        fileId = _getFileId(db, path)
        if fileId is not None:
            db.execute("DELETE FROM files where path = ?", (p,))
    db.commit()


def removeFile(db: sqlite3.Connection, path: Path):
    p = str(path)
    fileId = _getFileId(db, path)
    if fileId is not None:
        db.execute("DELETE FROM files where path = ?", (p,))
        db.commit()


def _insertFile(
    db: sqlite3.Connection,
    path: Path,
    time: str,
):
    db.execute(
        """INSERT INTO files (path, time_updated)
           VALUES (?, ?)""",
        (
            path,
            time,
        ),
    )


def _getFileId(db: sqlite3.Connection, path: Path) -> int:
    p = str(path)
    row = db.execute("SELECT id FROM files WHERE path = ?", (p,)).fetchone()
    if row is None:
        return row
    return row[0]


def getFileTime(db: sqlite3.Connection, path: Path):
    p = str(path)
    row = db.execute("SELECT time_updated FROM files where path = ?", (p,)).fetchone()
    if row is None:
        return row
    return row[0]


def _insertChunk(
    db: sqlite3.Connection,
    file_id: int,
    start_line: int,
    end_line: int,
    raw_text: str,
    embedding: np.ndarray,
):
    db.execute(
        """INSERT INTO chunks (file_id, start_line, end_line, raw_text, embedding)
           VALUES (?, ?, ?, ?, ?)""",
        (
            file_id,
            start_line,
            end_line,
            raw_text,
            embedding.astype(np.float32).tobytes(),
        ),
    )
