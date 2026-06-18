import typer
from pathlib import Path
from typing import Annotated
import os

app = typer.Typer(no_args_is_help=True)


@app.command()
def init(debug: Annotated[bool, typer.Option(help="Print debug logs")] = False):
    from .setup import setup

    """Initialize engine into current directory."""
    initialized = False
    cwd = Path.cwd()
    for item in cwd.iterdir():
        if item.suffix == ".db" and item.name == "corpusEngine":
            initialized = True
            print("Corpus Engine already initialized")

    if not initialized:
        setup(cwd, debug)


@app.command()
def update():
    pass


@app.command()
def remove():
    if os.path.exists("corpusEngine.db"):
        os.remove("corpusEngine.db")
        print("[INFO] Removed Corpus Engine")
    else:
        print("[INFO] Corpus Engine not initialized")
