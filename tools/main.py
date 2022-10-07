"""Tools for solving and submitting Advent of Code puzzles."""
import argparse
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Parse command line arguments and dispatch to subcommands."""

    parser = argparse.ArgumentParser(description=main.__doc__)
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand", required=True)

    funcs = {"pull": pull_data, "run": run_solution, "submit": submit_answer}

    for name, func in funcs.items():
        subparsers.add_parser(name, help=func.__doc__, add_help=False)

    args, unknown = parser.parse_known_args(argv)
    return funcs[args.subcommand](unknown)


def pull_data(argv: Optional[Sequence[str]] = None) -> int:
    """Pull puzzle data from Advent of Code."""

    parser = argparse.ArgumentParser(description=pull_data.__doc__)
    args = parser.parse_args(argv)

    print("Pulling data...", args)
    return 0


def run_solution(argv: Optional[Sequence[str]] = None) -> int:
    """Run a solution to a puzzle using the days's data."""

    parser = argparse.ArgumentParser(description=run_solution.__doc__)
    parser.add_argument(
        "-T",
        "--test",
        action="store_true",
        help="Use test data instead",
    )
    args = parser.parse_args(argv)

    print("Testing solution...", args)
    return 0


def submit_answer(argv: Optional[Sequence[str]] = None) -> int:
    """Submit a puzzle answer to Advent of Code."""

    parser = argparse.ArgumentParser(description=submit_answer.__doc__)
    args = parser.parse_args(argv)

    print("Submitting answer...", args)
    return 0
