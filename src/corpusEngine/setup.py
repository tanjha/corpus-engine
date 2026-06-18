from langchain_text_splitters import RecursiveCharacterTextSplitter
import sqlite3
from pathlib import Path
from datetime import datetime
from .embed import embed_engine
from .entryObj import entry
from .dbManager import initSQL, insertAll
from .vectorCheck import is_vectorizable

config = {"chunk_size": 256, "overlap": 26}


def setup(cwd: Path, debug: bool):
    print("[INFO] Initializing Corpus Engine...")
    db = sqlite3.connect("corpusEngine.db")
    initSQL(db)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunk_size"], chunk_overlap=config["overlap"]
    )
    embedder = embed_engine([])
    _lookDir(splitter=splitter, path=cwd, db=db, embedder=embedder)
    print("[INFO] Finished initialization.")


def _lookDir(
    splitter: RecursiveCharacterTextSplitter,
    path: Path,
    db: sqlite3.Connection,
    embedder: embed_engine,
    _seen=None,
):
    _seen = _seen if _seen is not None else set()
    real = path.resolve()
    if real in _seen:
        return
    _seen.add(real)
    for item in path.iterdir():
        if item.is_dir():
            _lookDir(splitter, item, db, embedder, _seen)
        elif is_vectorizable(item.suffix):
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
