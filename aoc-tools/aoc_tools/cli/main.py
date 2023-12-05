from typing import Annotated
from typing import Optional

import pendulum
import typer
from aoc_tools import plugins
from rich import print
from rich.table import Table

app = typer.Typer()


def get_current_puzzle_date(date: pendulum.DateTime) -> pendulum.Date:
    if date.month != 12:
        raise ValueError("It is not December. Please specify a puzzle date.")

    return pendulum.Date(date.year, 12, date.day)


def get_puzzle_date(day: int | None, year: int | None) -> pendulum.Date:
    today = pendulum.today()

    if day is None:
        return get_current_puzzle_date(today)

    return pendulum.date(year if year else today.year, 12, day)


@app.command()
def discover():
    """Discover available plugins."""
    print("Discovering plugins.")

    plugins.discover()

    table = Table("Plugin", "--name", "--lang")

    for plugin in plugins.plugins:
        table.add_row(
            plugin.config.title,
            plugin.config.name,
            plugin.config.lang,
        )

    print(table)


@app.command()
def new(
    day: Annotated[int, typer.Argument()] = None,
    year: Optional[int] = None,
    lang: Optional[str] = "python",
    plugin: Optional[str] = None,
):
    """Create a new day's solution file and pull its data."""

    puzzle_date = get_puzzle_date(day, year)

    print(
        f"NEW PUZZLE | [bold green]Day {puzzle_date.day} "
        f"of Advent of Code {puzzle_date.year}[/bold green]",
    )

    solution_generator = find_solution_generator(lang, plugin)


@app.command()
def pull(day: Annotated[int, typer.Argument()] = None, year: Optional[int] = None):
    """Pull puzzle data"""
    puzzle_date = get_puzzle_date(day, year)
