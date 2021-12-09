"""Day 9"""
from functools import reduce
from typing import NamedTuple

from aoc.solution import Solution


TEST_DATA = """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()

Grid = list[list[int]]


class Point(NamedTuple):
    row: int
    col: int
    value: int


def get_neighbors(grid: Grid, row: int, column: int) -> list[Point]:
    """Get the neighbors of a cell"""
    neighbors = []
    for i in range(row - 1, row + 2):
        if i == row or i < 0 or i >= len(grid):
            continue
        neighbors.append(Point(i, column, grid[i][column]))

    for j in range(column - 1, column + 2):
        if j == column or j < 0 or j >= len(grid[0]):
            continue
        neighbors.append(Point(row, j, grid[row][j]))

    return neighbors


def find_low_points(grid: Grid) -> list[Point]:
    """Find the low points"""
    low_points = []
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            neighbors = get_neighbors(grid, i, j)
            if value < min([n.value for n in neighbors]):
                low_points.append(Point(i, j, value))

    return low_points


def find_basin(grid: Grid, low_point: Point) -> set[Point]:
    """Find the basin"""
    basin: set[Point] = {low_point}

    def traverse_basin(current: Point) -> None:
        neighbors = get_neighbors(grid, current.row, current.col)
        for neighbor in neighbors:
            if neighbor.value == 9:
                continue
            elif neighbor.value > current.value and neighbor not in basin:
                basin.add(neighbor)
                traverse_basin(neighbor)

    traverse_basin(low_point)
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
        return sum(p.value + 1 for p in low_points)

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
        def parse_line(line: str) -> list[int]:
            return [int(x) for x in line]

        return self.input.as_list(parse_line)


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day09()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 15
    assert solution.part_two() == 1134


if __name__ == "__main__":
    test_solution(TEST_DATA)
