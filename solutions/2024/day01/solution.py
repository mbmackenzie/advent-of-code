import pathlib
from collections import Counter
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def parse(input_str: str):
    left, right = [], []

    for line in input_str.splitlines():
        l, r = map(int, line.split())
        left.append(l)
        right.append(r)

    return left, right


def part1(input_str: str) -> int:
    left, right = parse(input_str)

    left_s = sorted(left)
    right_s = sorted(right)

    return sum(abs(l - r) for l, r in zip(left_s, right_s))


def part2(input_str: str) -> int:
    left, right = parse(input_str)
    right_counts = Counter(right)

    return sum(l * right_counts[l] for l in left)


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 11),
    ],
    [
        (TEST_DATA, 31),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
