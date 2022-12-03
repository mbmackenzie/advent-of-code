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

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def priority(item_type: str) -> int:
    """Return the priority of an item type"""

    if item_type not in LETTERS + LETTERS.upper():
        raise ValueError(f"Invalid item type: {item_type}")

    if item_type in LETTERS:
        return LETTERS.index(item_type) + 1

    return 26 + LETTERS.index(item_type.lower()) + 1


def get_shared_items(rucksacks: Iterable[str]) -> str:
    common: set[str] = reduce(set.intersection, map(lambda x: set(x), rucksacks))

    if len(common) != 1:
        raise ValueError("There is no single shared item")

    return common.pop()


@split_lines
def part1(data: list[str], testing: bool = False) -> int:
    """Part 1 solution"""

    def half_string(s: str) -> tuple[str, str]:
        midpoint = len(s) // 2
        return s[:midpoint], s[midpoint:]

    return sum(priority(get_shared_items(half_string(rs))) for rs in data)


@group_lines(lines_per_group=3, split_groups=True)
def part2(data: list[list[str]], testing: bool = False) -> int:
    """Part 2 solution"""

    return sum(priority(get_shared_items(blocks)) for blocks in data)


if __name__ == "__main__":
    # part1(TEST_DATA)
    # part2(TEST_DATA)
    pass
