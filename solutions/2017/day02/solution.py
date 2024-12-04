import pathlib
from itertools import combinations
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def parse(input_str: str) -> list[list[int]]:
    lines = []
    for line in input_str.splitlines():
        lines.append([int(d) for d in line.split()])

    return lines


def part1(input_str: str) -> int:
    lines = parse(input_str)
    return sum(max(l) - min(l) for l in lines)


def find_val(line: list[int]):
    for l1, l2 in combinations(line, 2):
        little, big = (l1, l2) if l1 < l2 else (l2, l1)
        value, mod = divmod(big, little)

        if mod == 0:
            return value

    raise ValueError("No value found")


def part2(input_str: str) -> int:
    return sum(find_val(line) for line in parse(input_str))


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
5 1 9 5
7 5 3
2 4 6 8
"""

TEST_DATA2 = """\
5 9 2 8
9 4 7 3
3 8 6 5
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 18),
    ],
    [
        (TEST_DATA2, 9),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
