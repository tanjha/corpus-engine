from langchain_text_splitters import RecursiveCharacterTextSplitter
import sqlite3
from pathlib import Path
from datetime import datetime
from .embed import embed_engine
from .entryObj import entry
from .dbManager import initSQL, insertFull, getEmbeddings, removeFile
from .vectorCheck import is_vectorizable

scale = 2
config = {"chunk_size": 256 * scale, "overlap": 26 * scale}
debug = False


def setup(cwd: Path, dbg: bool = False):
    debug = dbg
    print("[INFO] Initializing Corpus Engine...")
    db = _initDB("corpusEngine.db")
    initSQL(db)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunk_size"],
        chunk_overlap=config["overlap"],
        separators=[""],
        strip_whitespace=False,
    )
    embedder = embed_engine([])

    _lookDir(splitter=splitter, path=cwd, db=db, embedder=embedder)
    print("[INFO] Finished initialization.")


def updateEmbed(cwd: Path, dbg: bool = False):
    db = _initDB("corpusEngine.db")
    embedder = embed_engine([])

    walked_dir = _listAll(cwd)
    paths = {str(p.absolute()) for p in walked_dir}
    db_rows = {
        row[0]: row[1] for row in db.execute("SELECT path, time_updated FROM files")
    }
    for path in paths:
        time = datetime.fromtimestamp(path.stat().st_mtime)
        if path not in db_rows:
            _splitFile(path=Path(path), db=db, embedder=embedder)
        elif time != db_rows[path]:
            removeFile()
            _splitFile(path=Path(path), db=db, embedder=embedder)
    for removed in db_rows.keys() - paths:
        removeFile(db, path(removed))


def query(debug: bool = False):
    print("Querying")
    db = _initDB("corpusEngine.db")
    embeddings = getEmbeddings(db)
    embedder = embed_engine(embeddings)
    query = _getQuery(embedder)
    sim_embeddings = embedder.similarityFull(query, embeddings)
    similarities = sorted(sim_embeddings, key=lambda x: x["similarity"], reverse=True)[
        :5
    ]

    for sim in similarities:
        similarity = sim["similarity"]
        path = sim["path"]
        start_line = sim["start_line"]
        end_line = sim["end_line"]

        text = sim["raw_text"]
        print(f"Similarity: {similarity.item():.4f}")
        print(f"File:       {path}")
        if int(start_line) == int(end_line):
            print(f"Line:       {start_line}")
        else:
            print(f"Lines:      {start_line}-{end_line}")
        print(f"Text:       {text}")
        print("-------------------------------------------------------------")


def _getQuery(embedder: embed_engine) -> str:
    print("Query:")
    raw = input("> ")
    return embedder._embedQuery(raw)


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
    pathlist = []
    for item in path.iterdir():
        pathlist.append(item)
        if item.is_dir():
            _lookDir(splitter, item, db, embedder, _seen)
        elif is_vectorizable(item):
            _splitFile(item, splitter, db, embedder)


def _listAll(
    path: Path,
    _seen=None,
) -> list[Path]:
    _seen = _seen if _seen is not None else set()
    real = path.resolve()
    if real in _seen:
        return []
    _seen.add(real)

    paths = []
    for item in path.iterdir():
        if item.is_dir():
            paths += _listAll(item, _seen)
        elif is_vectorizable(item):
            paths.append(item)
    return paths


def _initDB(connection: str) -> sqlite3.Connection:
    db = sqlite3.connect(connection)
    db.execute("PRAGMA foreign_keys = ON")
    return db


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
    to_embed = []
    entries = []
    line = 0
    for i, chunk in enumerate(chunks):
        start_line = line
        line += chunk.count("\n")
        end_line = line

        to_embed.append(chunk)
        ent = entry(
            path=file,
            start_line=start_line,
            end_line=end_line,
            time=time,
            raw_text=chunk,
        )
        # ent.printAll()
        entries.append(ent)
    embedded = embedder.embedAll(to_embed)
    for chunk, ent in zip(embedded, entries):
        ent.embedding = chunk
    insertFull(db, entries)
    print(f"[DEBUG] inserted all chunks of {file.name}")
