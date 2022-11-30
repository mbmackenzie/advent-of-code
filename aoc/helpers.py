import importlib.machinery
import importlib.resources as pkg_resources
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Type

import click

from aoc import assets
from aoc.solution import Solution
from aoc.solution import SolutionResult


def read_asset(asset_name: str) -> str:
    """Read an asset file"""
    return pkg_resources.read_text(assets, asset_name)


def get_latest_year() -> int:
    """
    Returns the last year if we are not in december yet otherwise
    returns the current year.
    """
    today = datetime.now()
    if today.month < 12:
        return today.year - 1
    return today.year


def get_solution_class(solution_file: Path) -> Type[Solution]:
    """Import the correct solution"""

    if not solution_file.exists():
        raise FileNotFoundError(f"Solution file {solution_file} not found!")

    module_name = f"solutions_{solution_file.name[:-3]}"
    cls_name = solution_file.name[:-3].title()

    spec = importlib.util.spec_from_file_location(module_name, solution_file.resolve())

    if not spec:
        raise ImportError(f"Could not import {solution_file}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    return getattr(module, cls_name)


def get_input_data(input_file: Path) -> list[str]:
    """Get the input data from the file"""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file {input_file} not found!")

    with open(input_file, "r") as f:
        return f.readlines()


def instantiate_solution(solution_file: Path, input_file: Path) -> Solution:
    """Import the correct solution and return an instance of it"""

    solution_cls = get_solution_class(solution_file)
    input_data = get_input_data(input_file)

    solution = solution_cls()  # type: ignore
    solution.set_input_data(input_data)
    return solution


def display_solution(solution: Solution, timeit: bool, number: int) -> None:
    """Display the first and second parts of the solution"""
    part_one, part_two = solution(timeit, number)

    def part_name(part: int) -> str:
        color = "green" if part == 1 else "red"
        return click.style(f"Part {part}:", fg=color)

    def display_part(part: int, result: SolutionResult) -> None:
        time_res = f" ({result.avg_time:.05f} sec)" if timeit else ""
        click.echo(f"{part_name(part)} {result.result}{time_res}")

    click.secho(solution, bold=True)

    display_part(1, part_one)
    display_part(2, part_two)

    if timeit:
        click.secho(f"Times represent average of {number:,d} runs", fg="yellow")
