from langchain_text_splitters import RecursiveCharacterTextSplitter
import sqlite3
import numpy as np
from pathlib import Path

acceptedFiles = ["py", "txt"]


def setup():
    db = sqlite3.connect("index.db")
    _initSQL(db)
    splitter = RecursiveCharacterTextSplitter(chunk_size=256, overlap=26)

    cwd = Path.cwd()
    lookDir(splitter, cwd)


def lookDir(splitter: RecursiveCharacterTextSplitter, path: Path, db: sqlite3):
    for item in path.iterdir():
        if item.is_dir():
            lookDir(splitter, path)
        else:
            if item.suffix in acceptedFiles:
                _splitFile(item, splitter, db)


def _splitFile(file: Path, splitter: RecursiveCharacterTextSplitter, db: sqlite3):
    embedding = ""  # embed here
    
    _insert(db=db, file=f"{file.name}")


def _initSQL(db: sqlite3):
    db.execute("""  CREATE TABLE chunks (
                        id          INTEGER PRIMARY KEY,
                        file        TEXT NOT NULL,
                        start_line  INTEGER,
                        end_line    INTEGER,
                        raw_text    TEXT NOT NULL,
                        embedding   BLOB NOT NULL
                    ) """)
    db.commit()


def _insert(
    db: sqlite3,
    file: str,
    start_line: int,
    end_line: int,
    raw_text: str,
    embedding: np.ndarray,
):
    db.execute("""
    INSERT INTO chunks 
""")
