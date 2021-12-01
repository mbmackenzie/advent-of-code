"""Day 10: Adapter Array"""
from collections import Counter
from collections import defaultdict

from aoc import Solution


class Day10(Solution):
    """Solution to day 10 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 10, "Adapter Array")

    @property
    def max_joltage(self) -> int:
        """The last element in the data plus 3"""
        return self.data[-1] + 3

    def _part_one(self) -> int:
        counts = Counter(
            val - prev for val, prev in zip(self.data, [0, *self.data[:-1]])
        )

        return counts[1] * (counts[3] + 1)

    def _part_two(self) -> int:
        counts = defaultdict(int, {0: 1})

        for value in self.data:
            counts[value] = counts[value - 1] + counts[value - 2] + counts[value - 3]

        return counts[self.max_joltage - 3]

    def _get_data(self) -> list[int]:
        return sorted(self.input.as_list(int))
