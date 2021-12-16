"""Day 15: Chiton"""
import heapq
from collections import defaultdict
from typing import Generator

from aoc.solution import Solution

TEST_DATA = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".strip()

Point = tuple[int, int]
Grid = defaultdict[Point, int]
ShortestPaths = dict[Point, int]


def get_neighbors(i: int, j: int) -> Generator[tuple[int, int], None, None]:
    yield i + 1, j
    yield i - 1, j
    yield i, j + 1
    yield i, j - 1


def get_grid_size(grid: Grid) -> tuple[int, int]:
    last_row, last_col = max(grid)
    return last_row + 1, last_col + 1


def find_lowest_risk(grid: Grid) -> int:
    n, m = get_grid_size(grid)

    starting_point = (0, 0)
    end_point = (n - 1, m - 1)

    stack = [(starting_point, 0)]
    lowest_risk: ShortestPaths = {}

    while stack:
        current_point, risk = heapq.heappop(stack)

        if current_point in lowest_risk and risk >= lowest_risk[current_point]:
            continue

        lowest_risk[current_point] = risk

        if current_point == end_point:
            return risk

        for next_point in get_neighbors(*current_point):
            if grid[next_point] < 1:
                continue

            heapq.heappush(stack, (next_point, risk + grid[next_point]))

    raise RuntimeError("Failed to reach endpoint")


class Day15(Solution):
    """Solution to day 15 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 15, "Chiton")

    def _part_one(self) -> int:
        """
        What is the lowest total risk of any path from the top
        left to the bottom right?
        """
        return find_lowest_risk(self.data)

    def _part_two(self) -> int:
        """
        What is the lowest total risk of any path from the top
        left to the bottom right?
        """
        n, m = get_grid_size(self.data)
        expanded_grid: Grid = defaultdict(int)

        for (i, j), value in self.data.items():
            for di in range(5):
                for dj in range(5):
                    new_value = value + di + dj
                    while new_value > 9:
                        new_value = new_value - 9
                    expanded_grid[(i + di * n, j + dj * m)] = new_value

        return find_lowest_risk(expanded_grid)

    def _get_data(self) -> Grid:
        lines = self.input.as_list()
        grid: Grid = defaultdict(int)
        for i, row in enumerate(lines):
            for j, value in enumerate(row):
                grid[(i, j)] = int(value)

        return grid


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day15()
    solution.set_input_data(data.split("\n"))

    part_one = solution.part_one()
    assert part_one == 40, f"Part one failed, got {part_one}"

    part_two = solution.part_two()
    assert part_two == 315, f"Part two failed, got {part_two}"


if __name__ == "__main__":
    test_solution(TEST_DATA)
