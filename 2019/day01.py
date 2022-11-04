"""Day 1 of Advent of Code 2019"""
from typing import Sequence


TEST_CASES = (
    ("12", 2, 2),
    ("14", 2, None),
    ("1969", 654, 966),
    ("100756", 33583, 50346),
)


def parse_data(input_str: str) -> Sequence[int]:
    """Parse data"""
    return [int(x) for x in input_str.splitlines()]


def calc_fuel(x: int) -> int:
    """Calculate fuel"""
    return x // 3 - 2


def part1(input_str: str, testing: bool = False) -> int:
    """Part 1 solution"""
    return sum(map(calc_fuel, parse_data(input_str)))


def part2(input_str: str, testing: bool = False) -> int:
    """Part 2 solution"""
    data = parse_data(input_str)

    total = 0
    for x in data:
        while (x := calc_fuel(x)) > 0:
            total += x

    return total
