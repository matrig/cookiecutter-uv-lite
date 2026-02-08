"""Command-line interface for {{cookiecutter.project_name}}."""

from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(
    name="{{cookiecutter.project_name}}",
    help="{{cookiecutter.project_description}}",
    add_completion=False,
)
console = Console()


@app.command()
def hello(name: str = typer.Option("World", help="Name to greet")) -> None:
    """Say hello to someone."""
    console.print(f"[bold green]Hello, {name}![/bold green]")


@app.command()
def version() -> None:
    """Show the application version."""
    console.print("[bold blue]{{cookiecutter.project_name}}[/bold blue] version 0.0.1")


if __name__ == "__main__":
    app()
