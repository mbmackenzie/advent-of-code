"""Day 3 of Advent of Code 2022"""
from functools import reduce
from typing import Iterable

from tools.parsing import group_lines
from tools.parsing import split_lines

TEST_DATA = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

TEST_CASES = ((TEST_DATA, 157, 70),)


def priority(item_type: str) -> int:
    """Return the priority of an item type"""

    if item_type.islower():
        return 1 + (ord(item_type) - ord("a"))

    return 27 + (ord(item_type) - ord("A"))


def get_shared_item(items: Iterable[str]) -> str:
    return reduce(set.intersection, map(lambda x: set(x), items)).pop()


@split_lines
def part1(data: list[str]) -> int:
    """Part 1 solution"""

    def half_string(s: str) -> tuple[str, str]:
        midpoint = len(s) // 2
        return s[:midpoint], s[midpoint:]

    return sum(priority(get_shared_item(half_string(rs))) for rs in data)


@group_lines(lines_per_group=3, split_groups=True)
def part2(data: list[list[str]]) -> int:
    """Part 2 solution"""

    return sum(priority(get_shared_item(blocks)) for blocks in data)


if __name__ == "__main__":
    # print(part1(TEST_DATA))
    # print(part2(TEST_DATA))
    pass
