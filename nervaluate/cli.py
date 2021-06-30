import typer

from nervaluate.nervaluate_cli import nervaluate

app = typer.Typer()
app.command()(nervaluate)

if __name__ == "__main__":
    app()
