import sqlite3
from pathlib import Path
import numpy as np
from .entryObj import entry


class dbManager:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def initSQL(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id      INTEGER PRIMARY KEY,
                path         TEXT UNIQUE NOT NULL,
                time_updated TEXT NOT NULL
            );
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id         INTEGER PRIMARY KEY,
                file_id    INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
                start_line INTEGER,
                end_line   INTEGER,
                raw_text   TEXT NOT NULL,
                embedding  BLOB NOT NULL
            );
        """)
        self.db.execute(
            "CREATE INDEX IF NOT EXISTS idx_chunks_file_id ON chunks(file_id);"
        )
        self.db.commit()

    def getEmbeddings(self):
        rows = self.db.execute("""
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

    def getDB(self) -> sqlite3.Connection:
        return self.db

    def insertFull(self, entries: list[entry]):
        if entries:
            self._insertFile(str(entries[0].path.absolute()), entries[0].time)
            print(f"inserting {str(entries[0].path.absolute())}")
            self.db.commit()
            for ent in entries:
                file_id = self._getFileId(str(ent.path.absolute()))
                self._insertChunk(
                    file_id,
                    ent.start_line,
                    ent.end_line,
                    ent.raw_text,
                    ent.embedding,
                )
            self.db.commit()

    def removeAll(self, paths: list[Path]):
        for path in paths:
            p = str(path)
            fileId = self._getFileId(path)
            if fileId is not None:
                self.db.execute("DELETE FROM files where path = ?", (p,))
        self.db.commit()

    def removeFile(self, path: Path):
        p = str(path)
        fileId = self._getFileId(path)
        if fileId is not None:
            self.db.execute("DELETE FROM files where path = ?", (p,))
            self.db.commit()

    def _insertFile(
        self,
        path: Path,
        time: str,
    ):
        self.db.execute(
            """INSERT INTO files (path, time_updated)
            VALUES (?, ?)""",
            (
                path,
                time,
            ),
        )

    def _getFileId(self, path: Path) -> int:
        p = str(path)
        row = self.db.execute("SELECT id FROM files WHERE path = ?", (p,)).fetchone()
        if row is None:
            return row
        return row[0]

    def getFileTime(self, path: Path):
        p = str(path)
        row = self.db.execute(
            "SELECT time_updated FROM files where path = ?", (p,)
        ).fetchone()
        if row is None:
            return row
        return row[0]

    def _insertChunk(
        self,
        file_id: int,
        start_line: int,
        end_line: int,
        raw_text: str,
        embedding: np.ndarray,
    ):
        self.db.execute(
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
