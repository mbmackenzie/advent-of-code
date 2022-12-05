"""Day 3"""
from aoc import Solution


def parse_input(data: str) -> list[int]:
    """Gets a list of indicies of all trees in the input"""
    return [i for i, v in enumerate(data) if v == "#"]


def generic_solution(
    data: list[list[int]],
    slope: tuple[int, int],
    spaces_per_row: int,
    init_xy: tuple[int, int] = (0, 0),
) -> int:
    """Gets the number of trees hit by a slope"""
    x, y = init_xy
    dx, dy = slope
    trees_hit = 0

    while y < len(data):

        if x % spaces_per_row in data[y]:
            trees_hit += 1

        x, y = x + dx, y + dy

    return trees_hit


class Day03(Solution):
    """Solution to day 3 of the 2020 Advent of Code"""

    data: list[list[int]]
    spaces_per_row: int

    def __init__(self) -> None:
        super().__init__(2020, 3, "")

    def _part_one(self) -> int:
        """How many trees do you hit moving down 1 and right 3?"""
        return generic_solution(self.data, (3, 1), self.spaces_per_row)

    def _part_two(self) -> int:
        """Return the product of the generic_solution for mutliple slopes"""
        slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

        ret = 1
        for slope in slopes:
            ret *= generic_solution(self.data, slope, self.spaces_per_row)

        return ret

    def _get_data(self) -> list[list[int]]:
        self.spaces_per_row = len(self.input.as_list()[0])
        return self.input.as_list(parse_input)
