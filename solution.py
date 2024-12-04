import pathlib
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def part1(input_str: str) -> int:
    return -1


def part2(input_str: str) -> int:
    return -1


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\

"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 1),
    ],
    [
        (TEST_DATA, 2),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
