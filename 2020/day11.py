"""Day 11"""
from typing import Any

from aoc import Solution

Grid = list[str]


def get_num_occupied(x: int, y: int, grid: Grid, acceptable: str) -> int:
    """Get the number of empty and occupied seats amongh neighbors"""

    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    ]

    def update_pos(x: int, y: int, direction: tuple[int, int]) -> tuple[int, int]:
        """Update the position"""
        return x + direction[0], y + direction[1]

    def in_grid(x: int, y: int) -> bool:
        """Check if the coordinates are in the grid"""
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    neighbors = ""

    for direction in directions:
        new_x, new_y = update_pos(x, y, direction)

        while True:

            if not in_grid(new_x, new_y):
                break

            if grid[new_x][new_y] in acceptable:
                neighbors += grid[new_x][new_y]
                break

            new_x, new_y = update_pos(new_x, new_y, direction)

    return neighbors.count("#")


def update_grid(
    old_grid: Grid, acceptable: str = ".L#", min_occupied_to_switch: int = 4
) -> Grid:
    """Update the grid"""
    new_grid = [""] * len(old_grid)
    for i, row in enumerate(old_grid):
        for j, seat in enumerate(row):
            occupied = get_num_occupied(i, j, old_grid, acceptable)

            if seat == "L" and occupied == 0:
                new_grid[i] += "#"
            elif seat == "#" and occupied >= min_occupied_to_switch:
                new_grid[i] += "L"
            else:
                new_grid[i] += seat

    return new_grid


def update_until_stable(initial_grid: Grid, **kwargs: Any) -> Grid:
    prev_grid = None
    current_grid = initial_grid

    while current_grid != prev_grid:
        prev_grid = current_grid
        current_grid = update_grid(current_grid, **kwargs)

    return current_grid


class Day11(Solution):
    """Solution to day 11 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 11, "")

    def _part_one(self) -> int:
        """How many occupied seats when the arrangment is stable?"""
        stable_grid = update_until_stable(self.data)
        return sum(seat == "#" for row in stable_grid for seat in row)

    def _part_two(self) -> int:
        """How many occupied seats when the arrangment is stable?

        - people ignore empty space
        - people need 5 or more occupied seats to leave
        """
        stable_grid = update_until_stable(
            self.data, acceptable="L#", min_occupied_to_switch=5
        )
        return sum(seat == "#" for row in stable_grid for seat in row)

    def _get_data(self) -> Grid:
        return self.input.as_list()
