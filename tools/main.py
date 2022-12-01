"""Tools for solving and submitting Advent of Code puzzles."""
import argparse
import datetime
import os
import sys
from collections import namedtuple
from typing import NoReturn
from typing import Optional
from typing import Sequence

import requests

from tools import caching
from tools import running

Day = namedtuple("Day", ["year", "day"])

_SUBCOMMANDS = ["new", "pull", "test", "run", "submit", "preview"]


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        self.print_help()
        sys.exit(2)


def _ensure_token() -> None:
    """Create the session token file."""

    if os.path.exists(".token"):
        return

    print("A session token is required to use this tool.")
    print("Please visit https://adventofcode.com/ and log in.")
    print("Next, copy the value of the session cookie from your browser.")
    print("Paste it below:")
    token = input("> ")
    with open(".token", "w") as file:
        file.write(token)


def _read_cookie() -> str:
    """Read the session token from the .env file."""
    with open(".token", "r") as file:
        return file.read().strip()


def _get_current_day() -> Day:
    today = datetime.date.today()
    if today.month != 12:
        return Day(today.year - 1, -1)

    return Day(today.year, today.day)


def _get_day(year: Optional[int], day: Optional[int], day_year: Optional[str]) -> Day:
    current = _get_current_day()

    if day_year is not None:
        if "-" in day_year:
            day, year = map(int, day_year.split("-"))
        elif len(day_year) == 4:
            day = int(day_year[:2])
            year = int(day_year[2:])
        else:
            raise ValueError(f"Invalid day-year format: {day_year}")

    if day is None and current.day == -1:
        raise ValueError("It's not December yet! Please specify a day.")

    if year is not None and year // 10 < 10:
        year += 2000

    day = day if day is not None else current.day
    year = year if year is not None else current.year

    return Day(year, day)


def _get_parser(description: Optional[str] = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-d", "--day", type=int, help="The day")
    parser.add_argument("-y", "--year", type=int, help="The year")
    parser.add_argument("day_year", nargs="?", help="The day and year (i.e., 01-22)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Utility for creating, testing, and submitting Advent of Code solutions."""

    parser = DefaultHelpParser(description=main.__doc__)
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand", required=True)

    caching.make_cache_dir()

    for name in _SUBCOMMANDS:
        func = globals()[name]
        subparsers.add_parser(name, help=func.__doc__, add_help=False)

    args, unknown = parser.parse_known_args(argv)

    if args.subcommand in ("new", "pull", "submit"):
        _ensure_token()

    return globals()[args.subcommand](unknown)


def new(argv: Sequence[str] | None = None) -> int:
    """Create a new day's file and pull its data."""
    parser = _get_parser(description=new.__doc__)
    args = parser.parse_args(argv)

    year, day = _get_day(args.year, args.day, args.day_year)
    pull(["--year", str(year), "--day", str(day)])

    print(f"AOC day {day:02d}, {year} - creating files...")

    if not os.path.exists(str(year)):
        os.mkdir(str(year))

    filename = f"{year}/day{day:02d}.py"
    if os.path.exists(filename):
        print(f"File {filename} already exists, skipping.")

    with open("tools/_assets/new_day.txt", "r") as file:
        template = file.read()

    with open(f"{year}/day{day:02d}.py", "w") as file:
        file.write(template.format(year=year, day=day))

    return 0


def pull(argv: Sequence[str] | None = None) -> int:
    """Pull puzzle data from Advent of Code."""

    parser = _get_parser(description=pull.__doc__)
    parser.add_argument("--force", action="store_true", help="Force data download")
    args = parser.parse_args(argv)

    year, day = _get_day(args.year, args.day, args.day_year)

    if not args.force and caching.data_is_cached(year, day):
        print(f"AOC day {day:02d}, {year} - data is already cached.")
        return 0

    print(f"AOC day {day:02d}, {year} - downloading data...")
    session_header = {"Cookie": f"session={_read_cookie()}"}
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, headers=session_header)

    if response.status_code != 200:
        print("Could not download data.")
        return 1

    caching.cache_data(year, day, response.text)
    return 0


def test(argv: Sequence[str] | None = None) -> int:
    """Test a solution against the cached data."""
    parser = _get_parser(description=test.__doc__)
    args, pytest_args = parser.parse_known_args(argv)

    year, day = _get_day(args.year, args.day, args.day_year)

    print(f"AOC day {day:02d}, {year} - testing solution...")
    running.run_test_cases(year, day, pytest_args)
    return 0


def run(argv: Sequence[str] | None = None) -> int:
    """Run a solution to a puzzle using the days's data."""
    parser = _get_parser(description=run.__doc__)
    parser.add_argument("-E", "--raise-errors", action="store_true", help="Raise exceptions")
    args = parser.parse_args(argv)

    year, day = _get_day(args.year, args.day, args.day_year)

    print(f"AOC day {day:02d}, {year} - running solution...")
    running.preview_solution(year, day, raise_errors=args.raise_errors)
    return 0


def submit(argv: Sequence[str] | None = None) -> int:
    """Submit a puzzle answer to Advent of Code."""

    parser = _get_parser(description=submit.__doc__)
    parser.add_argument("-p", "--part", type=int, required=True, help="The part")
    args = parser.parse_args(argv)

    year, day = _get_day(args.year, args.day, args.day_year)
    result = running.run_solution_part(year, day, args.part)

    print(f"AOC day {day:02d}, {year}")
    print(f"Submitting part {args.part} answer: {result} ...")

    response = requests.post(
        f"https://adventofcode.com/{year}/day/{day}/answer",
        headers={"Cookie": f"session={_read_cookie()}"},
        data={"level": args.part, "answer": result},
    )

    return 0


def preview(argv: Sequence[str] | None = None) -> None:
    """Print the cached data for a day."""

    parser = _get_parser(description=preview.__doc__)
    parser.add_argument("-l", "--lines", type=int, help="The number of lines to print")
    args = parser.parse_args(argv)

    year, day = _get_day(args.year, args.day, args.day_year)

    if not caching.data_is_cached(year, day):
        print(f"AOC day {day:02d}, {year} - data is not cached.")
        return

    print(f"AOC day {day:02d}, {year} - previewing data...")
    with open(caching.cache_filename(year, day), "r") as file:
        lines = args.lines if args.lines else 10
        for _ in range(lines):
            print(file.readline(), end="")
