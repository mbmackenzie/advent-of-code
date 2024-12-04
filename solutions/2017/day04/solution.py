import pathlib
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def part1(input_str: str) -> int:
    lines = input_str.strip().split("\n")

    return sum(1 for line in lines if len(line.split()) == len(set(line.split())))


def check_valid(line: str) -> bool:
    words = line.split()
    sorted_words = {"".join(sorted(word)) for word in words}

    if len(words) != len(sorted_words):
        return False

    return True


def part2(input_str: str) -> int:
    return sum(check_valid(line) for line in input_str.strip().split("\n"))


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa
"""

TEST_DATA2 = """\
abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 2),
    ],
    [
        (TEST_DATA2, 3),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
