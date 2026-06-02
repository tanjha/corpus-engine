import typer
from typing_extensions import Annotated
from pathlib import Path
from .setup import setup


def do(
    command: Annotated[
        str,
        typer.Argument(
            help="Example Commands: \ninit (initialize engine into current directory) \nupdate (updates vector listings)"
        ),
    ] = "",
):
    match command.tolower():
        case "init":
            pass
        case "update":
            pass


def init():
    """ """
    initialized = False
    cwd = Path.cwd()
    for item in cwd.iterdir():
        if item.suffix == ".toml" and item.name == "corpusEngine":
            initialized = True

    if not initialized:
        setup(cwd)


def update():
    """ """
    pass
