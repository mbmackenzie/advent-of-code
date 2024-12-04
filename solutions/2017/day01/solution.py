import pathlib
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def part1(input_str: str) -> int:
    digits = [c1 for c1, c2 in zip(input_str, input_str[1:] + input_str[0]) if c1 == c2]
    return sum(int(d) for d in digits)


def part2(input_str: str) -> int:
    mid = int(len(input_str) / 2)
    digits = [c1 for c1, c2 in zip(input_str[:mid], input_str[mid:] + input_str[0]) if c1 == c2]

    return sum(int(d) * 2 for d in digits)


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_CASES: TestCases = (
    [
        ("1122", 3),
        ("1111", 4),
        ("1234", 0),
        ("91212129", 9),
    ],
    [
        ("1212", 6),
        ("1221", 0),
        ("123425", 4),
        ("123123", 12),
        ("12131415", 4),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
