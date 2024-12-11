import functools
import pathlib
from collections import Counter
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def parse(s: str) -> list[int]:
    return [int(c) for c in s.strip().split()]


@functools.lru_cache(maxsize=None)
def process_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    stone_string = str(stone)
    stone_length = len(stone_string)
    if stone_length % 2 == 0:
        m = stone_length // 2
        left = int(stone_string[:m])
        right = int(stone_string[m:])

        return [left, right]

    return [stone * 2024]


def part1(input_str: str) -> int:
    stones = parse(input_str)
    new_stones = []

    for _ in range(25):
        for stone in stones:
            new_stones.extend(process_stone(stone))

        stones = new_stones
        new_stones = []

    return len(stones)


def part2(input_str: str) -> int:
    stones = parse(input_str)
    current = Counter(stones)

    for _ in range(75):
        new = Counter()
        for stone, count in current.items():
            new_stones = process_stone(stone)

            for new_stone in new_stones:
                new[new_stone] += count

        current = new

    return sum(current.values())


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
125 17
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 55312),
    ],
    [
        (TEST_DATA, 65601038650482),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
