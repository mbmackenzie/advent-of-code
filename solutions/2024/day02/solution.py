import pathlib
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def parse(input_str: str) -> list[list[int]]:
    return [[int(x) for x in line.split()] for line in input_str.splitlines()]


def sign(x: int) -> int:
    return 1 if x > 0 else -1


def run_line(line: list[int]) -> int:
    signs: set[int] = set()

    for i, j in zip(line, line[1:]):
        d, s = abs(i - j), sign(i - j)

        signs.add(s)
        if d < 1 or d > 3:
            return 0

    if len(set(signs)) == 1:
        return 1

    return 0


def part1(input_str: str) -> int:
    lines = parse(input_str)
    return sum(run_line(line) for line in lines)


def part2(input_str: str) -> int:
    lines = parse(input_str)

    tot = 0
    for line in lines:
        if run_line(line):
            tot += 1
            continue

        for r in range(len(line)):
            if run_line(line[:r] + line[r + 1 :]):
                tot += 1
                break

    return tot


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 2),
    ],
    [
        (TEST_DATA, 4),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
