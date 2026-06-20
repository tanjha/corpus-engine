import typer
from pathlib import Path
from typing import Annotated
import os

app = typer.Typer(no_args_is_help=True)


@app.command()
def init(debug: Annotated[bool, typer.Option(help="Print debug logs")] = False):
    """Initialize engine into current directory."""
    doInit(debug)


def doInit(debug: bool = False):
    initialized = False
    cwd = Path.cwd()
    # print(cwd)
    for item in cwd.iterdir():
        if item.name == "corpusEngine.db":
            initialized = True
            print("[INFO] Corpus Engine already initialized")
    if not initialized:
        from .worker import setup

        setup(cwd, debug)


@app.command()
def query(debug: Annotated[bool, typer.Option(help="Print debug logs")] = False):
    initialized = False
    cwd = Path.cwd()
    # print(cwd)
    for item in cwd.iterdir():
        if item.name == "corpusEngine.db":
            initialized = True

    if initialized:
        from .worker import query

        query(debug)
    else:
        print("[INFO] Corpus Engine not initialized")


@app.command()
def update():
    initialized = False
    cwd = Path.cwd()
    # print(cwd)
    for item in cwd.iterdir():
        if item.name == "corpusEngine.db":
            initialized = True

    if initialized:
        from .worker import updateEmbed

        updateEmbed(cwd)
    else:
        print("[INFO] Corpus Engine not initialized")


@app.command()
def reset(debug: Annotated[bool, typer.Option(help="Print debug logs")] = False):
    """Remove Corpus Engine and reinitialize it."""
    doRemove()
    doInit(debug)


@app.command()
def remove():
    doRemove()


def doRemove():
    if os.path.exists("corpusEngine.db"):
        os.remove("corpusEngine.db")
        print("[INFO] Removed Corpus Engine")
    else:
        print("[INFO] Corpus Engine not initialized")
