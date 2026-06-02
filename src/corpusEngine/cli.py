import typer

from .engine import do

app = typer.Typer()
app.command()(do)

if __name__ == "__main__":
    app()
