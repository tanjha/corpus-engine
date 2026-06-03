from langchain_text_splitters import RecursiveCharacterTextSplitter
import sqlite3
from pathlib import Path
from datetime import datetime
from .embed import embed_engine
from .entryObj import entry
from .dbManager import initSQL, insertAll

acceptedFiles = ["py", "txt"]
config = {"chunk_size": 256, "overlap": 26}


def setup():
    db = sqlite3.connect("index.db")
    initSQL(db)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunk_size"], overlap=config["overlap"]
    )
    embedder = embed_engine([])
    cwd = Path.cwd()
    _lookDir(splitter, cwd, db, embedder)


def _lookDir(
    splitter: RecursiveCharacterTextSplitter,
    path: Path,
    db: sqlite3.Connection,
    embedder: embed_engine,
):
    for item in path.iterdir():
        if item.is_dir():
            _lookDir(splitter, path)
        else:
            if item.suffix in acceptedFiles:
                _splitFile(item, splitter, db, embedder)


def _splitFile(
    file: Path,
    splitter: RecursiveCharacterTextSplitter,
    db: sqlite3.Connection,
    embedder: embed_engine,
):
    time = datetime.fromtimestamp(file.stat().st_mtime)
    with open(file, "r") as f:
        raw_full = f.read()
    chunks = splitter.split_text(raw_full)
    to_embed = [str]
    entries = [entry]
    for i, chunk in enumerate(chunks):
        start_line, end_line = _generateLines(file, i)
        to_embed.append(chunk)
        ent = entry(
            path=file,
            start_line=start_line,
            end_line=end_line,
            time=time,
            raw_text=chunk,
        )
        entries.append(ent)
    embedded = embedder.embedAll(to_embed)
    for chunk, ent in zip(embedded, entries):
        ent.embedding = chunk
    insertAll(db, entries)


def _generateLines(file_path: Path, chunk_index: int) -> tuple[int, int]:
    total_lines = sum(1 for _ in file_path.open())
    start_line = chunk_index * (config["chunk_size"] - config["overlap"])
    end_line = min(start_line + config["chunk_size"], total_lines)
    return start_line, end_line
