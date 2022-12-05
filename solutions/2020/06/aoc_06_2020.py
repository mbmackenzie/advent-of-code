"""Day 6: Custom Customs"""
from functools import reduce

from aoc import Solution
from aoc.reformaters import combine_nonblank_lines


class Day06(Solution):
    """Solution to day 6 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 6, "Custom Customs")

    def _part_one(self) -> int:
        """Sum of the number of unique questions each group answered"""
        return sum(map(len, self.data))

    def _part_two(self) -> int:
        """TODO"""

        def mutli_intersect(sets: list[set[str]]) -> set[str]:
            return reduce(lambda x, y: x & y, sets)

        intersections = [mutli_intersect(groups) for groups in self.data]
        return sum(map(len, intersections))

    def _reformat_data(self) -> None:
        self.input.reformat(combine_nonblank_lines)

    def _get_data_for_part_one(self) -> list[set[str]]:
        return self.input.as_list(lambda x: set(x.replace(" ", "")))

    def _get_data_for_part_two(self) -> list[list[set[str]]]:
        return self.input.as_list(lambda x: [set(g) for g in x.split(" ")])


if __name__ == "__main__":
    sol = Day06()
    print(sol())
