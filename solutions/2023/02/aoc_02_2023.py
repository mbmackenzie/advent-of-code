"""Day 2 of Advent of Code 2023"""
from __future__ import annotations

import re
from collections import defaultdict
from typing import Iterator
from typing import NamedTuple

TEST_DATA = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

TEST_CASES = ((TEST_DATA, 8, 2286),)
PULL_REGEX = re.compile(r"(?P<count>\d+) (?P<cube>red|green|blue)")


class CubePull(NamedTuple):
    red: int = 0
    green: int = 0
    blue: int = 0

    @property
    def power(self) -> int:
        return self.red * self.green * self.blue

    def __le__(self, o: CubePull) -> bool:
        return self.red <= o.red and self.green <= o.green and self.blue <= o.blue


def iter_max_cube_counts(input_str: str) -> Iterator[tuple[int, CubePull]]:
    for game_id, pull_str in enumerate(input_str.splitlines(), 1):
        pull_dict = defaultdict(int)

        for pull in pull_str.split("; "):
            for count_str, cube in PULL_REGEX.findall(pull):
                count = int(count_str)

                if count > pull_dict[cube]:
                    pull_dict[cube] = count

        yield game_id, CubePull(**pull_dict)


def part1(input_str: str) -> int:
    """Part 1 solution"""
    limits = CubePull(red=12, green=13, blue=14)

    max_counts = iter_max_cube_counts(input_str)
    return sum(game_id for game_id, counts in max_counts if counts <= limits)


def part2(input_str: str) -> int:
    """Part 2 solution"""
    max_counts = iter_max_cube_counts(input_str)
    return sum(counts.power for _, counts in max_counts)


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
