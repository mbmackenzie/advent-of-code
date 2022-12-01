"""Day 1 of Advent of Code 2022"""
from typing import Iterator

TEST_DATA = """
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

TEST_CASES = ((TEST_DATA.strip(), 24000, 45000),)


def parse_elves(input_str: str) -> Iterator[list[int]]:
    """Parse the elves"""

    for elf in input_str.split("\n\n"):
        yield [int(s) for s in elf.splitlines() if s.isdigit()]


def part1(input_str: str, testing: bool = False) -> int:
    """Part 1 solution"""

    scores = [sum(elf) for elf in parse_elves(input_str)]
    return max(scores)


def part2(input_str: str, testing: bool = False) -> int:
    """Part 2 solution"""

    scores = [sum(elf) for elf in parse_elves(input_str)]
    return sum(c for c in sorted(scores)[-3:])


if __name__ == "__main__":
    # part1()
    # part2()
    pass
