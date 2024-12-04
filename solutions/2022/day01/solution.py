import pathlib
from typing import Iterator
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def parse_elves(input_str: str) -> Iterator[list[int]]:
    for elf in input_str.split("\n\n"):
        yield [int(s) for s in elf.splitlines() if s.isdigit()]


def part1(input_str: str) -> int:
    scores = [sum(elf) for elf in parse_elves(input_str)]
    return max(scores)


def part2(input_str: str) -> int:
    scores = [sum(elf) for elf in parse_elves(input_str)]
    return sum(c for c in sorted(scores)[-3:])


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 24000),
    ],
    [
        (TEST_DATA, 45000),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
