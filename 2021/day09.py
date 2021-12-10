"""Day 9"""
from functools import reduce
from typing import Generator

from aoc.solution import Solution


TEST_DATA = """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()

Grid = dict[tuple[int, int], int]
Point = tuple[int, int]


def get_neighbors(point: Point) -> Generator[Point, None, None]:
    """Get the neighbors of a cell"""
    i, j = point
    yield i + 1, j
    yield i - 1, j
    yield i, j + 1
    yield i, j - 1


def find_low_points(grid: Grid) -> list[Point]:
    """Find the low points"""
    low_points = []
    for point, value in grid.items():
        if all([value < grid.get(n, 9) for n in get_neighbors(point)]):
            low_points.append(point)

    return low_points


def find_basin(grid: Grid, point: Point) -> set[Point]:
    """Find the basin"""
    basin: set[Point] = {point}

    def traverse_basin(point: Point) -> None:
        value = grid[point]
        for neighbor in get_neighbors(point):
            n_value = grid.get(neighbor, 9)
            if n_value == 9:
                continue
            elif n_value > value and neighbor not in basin:
                basin.add(neighbor)
                traverse_basin(neighbor)

    traverse_basin(point)
    return basin


class Day09(Solution):
    """Solution to day 9 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 9, "")

    def _part_one(self) -> int:
        """
        What is the sum of the risk levels of all low points
        on your heightmap?
        """
        low_points = find_low_points(self.data)
        return sum(self.data[p] + 1 for p in low_points)

    def _part_two(self) -> int:
        """
        What do you get if you multiply together the sizes of the
        three largest basins?
        """
        basin_lens = []
        low_points = find_low_points(self.data)
        for low_point in low_points:
            basin = find_basin(self.data, low_point)
            basin_lens.append(len(basin))

        return reduce(lambda x, y: x * y, sorted(basin_lens)[-3:])

    def _get_data(self) -> Grid:
        data = self.input.as_list(lambda line: [int(x) for x in line])

        grid: Grid = dict()
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                grid[(i, j)] = value

        return grid


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day09()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 15
    assert solution.part_two() == 1134


if __name__ == "__main__":
    test_solution(TEST_DATA)
