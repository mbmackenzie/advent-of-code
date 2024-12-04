import pathlib
import subprocess
from typing import Annotated

import typer
from rich import print
from rich.prompt import Confirm
from rich.prompt import Prompt

from tools.utils import fetch_input
from tools.utils import get_puzzle
from tools.utils import Puzzle
from tools.utils import submit_answer
from tools.utils import try_fetch_input

app = typer.Typer()


@app.command()
def create_token(token: Annotated[str | None, typer.Argument()] = None) -> None:
    """Create a new token file."""
    token_path = pathlib.Path(".token")

    if token_path.exists():
        print("[yellow]Token already exists")
        if not Confirm.ask("Do you want to overwrite it?"):
            print("[red]Exiting.")
            return

    if token:
        token_path.write_text(token)
        print("[green]Token created!")
        return

    new_token = Prompt.ask("Enter token value")
    token_path.write_text(new_token)
    print("[green]Token created!")


Day = Annotated[int | None, typer.Option("--day", "-d", help="The day")]
Year = Annotated[int | None, typer.Option("--year", "-y", help="The year")]
Part = Annotated[int | None, typer.Option("--part", "-p", help="The part of the solution")]
Next = Annotated[bool, typer.Option(help="Use next day")]


@app.command("set")
def set_puzzle(day: Day = None, year: Year = None, next: Next = False, part: Part = None):
    """Set the current puzzle."""
    puzzle = get_puzzle(None, day, year, part, next)
    print(
        f"[bright_cyan]Setting current puzzle to Day {puzzle.day}, {puzzle.year}, part {puzzle.part}..."
    )

    puzzle.save()


@app.command("part1")
def set_part1() -> None:
    """Set the current puzzle to part 1."""
    current_puzzle = Puzzle.load()
    if not current_puzzle:
        print("[red]No current puzzle set!")
        raise typer.Exit()

    print("[bright_cyan]Setting current puzzle to part 1...")
    current_puzzle.part = 1
    current_puzzle.save()


@app.command("part2")
def set_part2() -> None:
    """Set the current puzzle to part 2."""
    current_puzzle = Puzzle.load()
    if not current_puzzle:
        print("[red]No current puzzle set!")
        raise typer.Exit()

    print("[bright_cyan]Setting current puzzle to part 2...")
    current_puzzle.part = 2
    current_puzzle.save()


@app.command("clear")
def clear_puzzle() -> None:
    """Clear the current puzzle."""
    print("[bright_cyan]Clearing current puzzle...")
    if current_puzzle := Puzzle.load():
        current_puzzle.delete()


@app.command()
def preview(day: Day = None, year: Year = None, part: Part = None, next: Next = False) -> None:
    """Preview the current puzzle."""
    puzzle = get_puzzle(Puzzle.load(), day, year, part, next)
    print(
        f"[bold bright_green]Advent of Code: Day {puzzle.day}, {puzzle.year}! (Part {puzzle.part})"
    )


def _read_token() -> str:
    token_path = pathlib.Path(".token")

    if not token_path.exists():
        print("[red]Token not found!")
        raise typer.Exit()

    return token_path.read_text().strip()


@app.command("pull")
def pull_data(day: Day = None, year: Year = None) -> None:
    """Pull data for the current puzzle"""
    puzzle = get_puzzle(Puzzle.load(), day, year)
    solution_folder = pathlib.Path(f"solutions/{year}/day{puzzle.day:02d}")
    if not solution_folder.exists():
        print(
            f"[red]Solution folder [not bold underline]{solution_folder}[/] not found!",
        )
        raise typer.Exit()

    input_file = solution_folder / "input.txt"
    if input_file.exists() and not Confirm.ask("Do you want to overwrite it?"):
        print("[red]Exiting.")
        return

    print(
        f"[bright_cyan]Pulling data for [bold]Day {puzzle.day}, {puzzle.year}[/bold]...",
    )

    input_data = fetch_input(puzzle.day, puzzle.year, _read_token())
    input_file.write_text(input_data)

    print("[green]Data pulled!")


@app.command("new")
def new_day(day: Day = None, year: Year = None, next: Next = False) -> None:
    """Create a new day folder and pull data."""
    puzzle = get_puzzle(None, day, year, next=next)
    puzzle.save()

    solution_folder = pathlib.Path(f"solutions/{puzzle.year}/day{puzzle.day:02d}")

    if solution_folder.exists():
        print(
            f"[red]Solution folder [not bold underline]{solution_folder}[/] already exists!",
        )
        raise typer.Exit()

    print(
        f"[bright_cyan]Creating solution folder [not bold underline]{solution_folder}[/]...",
    )
    solution_folder.mkdir(parents=True)

    print("[bright_cyan]Pulling data...")
    input_file = solution_folder / "input.txt"
    input_data = try_fetch_input(puzzle.day, puzzle.year, _read_token())
    input_file.write_text(input_data)

    print("[bright_cyan]Creating solution file...")
    solution_template = pathlib.Path("solution.py")
    solution_file = solution_folder / "solution.py"
    solution_file.write_text(solution_template.read_text())

    print(f"[bold green]Day {puzzle.day}, {puzzle.year} created!")


@app.command("run")
def run_day(
    day: Day = None,
    year: Year = None,
    part: Part = None,
    test: Annotated[bool, typer.Option("-t", "--test")] = False,
    submit: Annotated[bool, typer.Option()] = False,
) -> None:
    """Run the current puzzle."""
    puzzle = get_puzzle(Puzzle.load(), day, year, part)
    print(f"[bright_cyan not bold]Running Day {puzzle.day}, {puzzle.year}, part {puzzle.part}...")

    solution_folder = pathlib.Path(f"solutions/{puzzle.year}/day{puzzle.day:02d}")
    solution_file = solution_folder / "solution.py"

    if not solution_file.exists():
        print(f"[red]Solution file [not bold underline]{solution_file}[/] not found!")
        raise typer.Exit()

    command = f"uv run {solution_file.absolute()} --part {puzzle.part}"

    if test:
        command = f"{command} --test"
        print(f"[bright_black not bold]{command}[/]\n")
        subprocess.run(command, shell=True)
        return

    print(f"[bright_black not bold]{command}[/]\n")
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    answer = process.stdout.strip()
    print(f"Result: {answer}")

    if submit:
        status = submit_answer(puzzle.day, puzzle.year, _read_token(), puzzle.part, answer)

        if status == "Correct":
            print("[bold green]Correct!")
        elif status == "Already completed":
            print("[bold yellow]Already completed!")
        else:
            print(f"[bold red]{status}[/]")


@app.command("dev")
def dev() -> None:
    """Continuously run tests for the current puzzle."""

    file_watcher = "watchexec"
    cmd = f"{file_watcher} -w solutions/ -w .current_puzzle -- aoc run --test"
    print(f"[bright_black not bold]{cmd}[/]\n")

    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    app()
