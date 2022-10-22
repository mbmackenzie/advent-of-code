"""Tools for solving and submitting Advent of Code puzzles."""
import argparse
import datetime
import os
from collections import namedtuple
from typing import Optional
from typing import Sequence

import requests

from tools.caching import _cache_data
from tools.caching import _data_is_cached
from tools.caching import _make_cache_dir
from tools.runner import _run_solution
from tools.tester import _run_test_cases

Day = namedtuple("Day", ["year", "day"])


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
        day, year = map(int, day_year.split("-"))

    if day is None and current.day == -1:
        raise ValueError("It's not December yet! Please specify a day.")

    if year is not None and year // 10 < 10:
        year += 2000

    day = day if day is not None else current.day
    year = year if year is not None else current.year

    return Day(year, day)


def _get_parser(description: Optional[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-d", "--day", type=int, help="The day")
    parser.add_argument("-y", "--year", type=int, help="The year")
    parser.add_argument("day_year", help="The day and year")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Parse command line arguments and dispatch to subcommands."""

    parser = argparse.ArgumentParser(description=main.__doc__)
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand", required=True)

    _make_cache_dir()
    funcs = {"new": new_day, "pull": pull_data, "run": run_solution, "submit": submit_answer}

    for name, func in funcs.items():
        subparsers.add_parser(name, help=func.__doc__, add_help=False)

    args, unknown = parser.parse_known_args(argv)

    if args.subcommand in ("new", "pull", "submit"):
        _ensure_token()

    return funcs[args.subcommand](unknown)


def new_day(argv: Optional[Sequence[str]] = None) -> int:
    """Create a new day's file and pull its data."""

    parser = _get_parser(description=new_day.__doc__)
    args = parser.parse_args(argv)

    year, day = _get_day(args.year, args.day, args.day_year)
    pull_data(["--year", str(year), "--day", str(day)])

    print(f"AOC day {day:02d}, {year} - creating files...")

    if not os.path.exists(str(year)):
        os.mkdir(str(year))

    filename = f"{year}/day{day:02d}.py"
    if os.path.exists(filename):
        print(f"File {filename} already exists, skipping.")

    with open(f"{year}/day{day:02d}.py", "w") as file:
        file.write(f'"""Day {day} of Advent of Code {year}"""')

    return 0


def pull_data(argv: Optional[Sequence[str]] = None) -> int:
    """Pull puzzle data from Advent of Code."""

    parser = _get_parser(description=pull_data.__doc__)
    parser.add_argument("--force", action="store_true", help="Force data download")
    args = parser.parse_args(argv)

    year, day = _get_day(args.year, args.day, args.day_year)

    if not args.force and _data_is_cached(year, day):
        print(f"AOC day {day:02d}, {year} - data is already cached.")
        return 0

    print(f"AOC day {day:02d}, {year} - downloading data...")
    session_header = {"Cookie": f"session={_read_cookie()}"}
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, headers=session_header)

    if response.status_code != 200:
        print("Could not download data.")
        return 1

    _cache_data(year, day, response.text)
    return 0


def run_solution(argv: Optional[Sequence[str]] = None) -> int:
    """Run a solution to a puzzle using the days's data."""

    parser = _get_parser(description=run_solution.__doc__)
    parser.add_argument("-T", "--test", action="store_true", help="Use test data")
    args, unknown = parser.parse_known_args(argv)

    year, day = _get_day(args.year, args.day, args.day_year)
    print(f"AOC day {day:02d}, {year} - running solution...")

    parts = [1]

    if args.test:
        _run_test_cases(year, day, unknown)
        return 0

    _run_solution(year, day, parts)

    return 0


def submit_answer(argv: Optional[Sequence[str]] = None) -> int:
    """Submit a puzzle answer to Advent of Code."""

    parser = argparse.ArgumentParser(description=submit_answer.__doc__)
    args = parser.parse_args(argv)

    print("Submitting answer...", args)

    return 0
