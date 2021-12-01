"""Day 5: Binary Boarding"""
from functools import reduce
from typing import Callable

from aoc import Solution


def parse_boarding_pass(raw_input: str) -> int:
    """Parse input into two strings"""

    def reduce_with(replace: str) -> Callable[[str, str], str]:
        def inner(x: str, y: str) -> str:
            return x.replace(y, replace)

        return inner

    value = reduce(reduce_with("0"), "FL", raw_input)
    value = reduce(reduce_with("1"), "BR", value)

    return int(value, 2)


class Day05(Solution):
    """Solution to day 5 of the 2020 Advent of Code"""

    data: list[int]

    def __init__(self) -> None:
        super().__init__(2020, 5, "Binary Boarding")

    def _part_one(self) -> int:
        """Returns the max row * column"""
        return max(self.data)

    def _part_two(self) -> int:
        """What seat is your seat?"""
        sorted_seat_ids = sorted(self.data)
        diffs = [x - y for x, y in zip(sorted_seat_ids[1:], sorted_seat_ids[:-1])]
        return sorted_seat_ids[diffs.index(2)] + 1

    def _get_data(self) -> list[int]:
        return self.input.as_list(parse_boarding_pass)
