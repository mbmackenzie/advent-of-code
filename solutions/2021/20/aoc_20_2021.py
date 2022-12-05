"""Day 20: Trench Map"""
from collections import defaultdict
from typing import Generator

from aoc.solution import Solution


TEST_DATA = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".strip()

Point = tuple[int, int]
Grid = dict[Point, int]


def get_neighbors(i: int, j: int) -> Generator[Point, None, None]:
    for i_ in range(i - 1, i + 2):
        for j_ in range(j - 1, j + 2):
            yield i_, j_


def get_algorithm_idx(grid: Grid, i: int, j: int) -> int:
    bin_str = ""
    for neighbor in get_neighbors(i, j):
        bin_str += str(grid[neighbor])

    return int(bin_str, 2)


def update_grid(grid: Grid, algorithm_string: str, num_steps: int) -> Grid:
    to_update: Grid = grid.copy()
    outer_toggle = algorithm_string[0] == "#" and algorithm_string[-1] == "."

    for step in range(num_steps):

        min_x = min(x for x, _ in to_update)
        min_y = min(y for _, y in to_update)
        max_x = max(x for x, _ in to_update)
        max_y = max(y for _, y in to_update)

        if outer_toggle and step % 2 == 0:
            updated: Grid
            updated = defaultdict(lambda: 1)
        else:
            updated = defaultdict(int)

        for i in range(min_x - 1, max_x + 2):
            for j in range(min_y - 1, max_y + 2):
                output_idx = get_algorithm_idx(to_update, i, j)
                output_char = algorithm_string[output_idx]
                updated[(i, j)] = 1 if output_char == "#" else 0

        to_update = updated

    return to_update


class Day20(Solution):
    """Solution to day 20 of the 2021 Advent of Code"""

    algorithm_string: str

    def __init__(self) -> None:
        super().__init__(2021, 20, "Trench Map")

    def _part_one(self) -> int:
        """After 2 iterations, how many pixels are lit in the resulting image?"""
        updated_grid = update_grid(self.data, self.algorithm_string, 2)
        return sum(updated_grid.values())

    def _part_two(self) -> int:
        """After 50 iterations, how many pixels are lit in the resulting image?"""
        updated_grid = update_grid(self.data, self.algorithm_string, 50)
        return sum(updated_grid.values())

    def _pop_lines(self) -> None:
        self.algorithm_string = self.input.pop_line()

    def _get_data(self) -> Grid:
        data = self.input.as_list()
        grid = defaultdict(int)
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if val == "#":
                    grid[(i, j)] = 1
        return grid


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day20()
    solution.set_input_data(data.split("\n"))

    part_one = solution.part_one()
    assert part_one == 35, f"Part one failed, got {part_one}"

    part_two = solution.part_two()
    assert part_two == 3351, f"Part two failed, got {part_two}"


if __name__ == "__main__":
    test_solution(TEST_DATA)
