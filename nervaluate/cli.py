import typer

from nervaluate.evaluate import evaluate

app = typer.Typer()

app.command()(evaluate)

if __name__ == "__main__":
    app()
