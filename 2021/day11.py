"""Day 11: Dumbo Octopus"""
from collections import defaultdict
from typing import Generator
from typing import NamedTuple

from aoc.solution import Solution

TEST_DATA = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip()

Point = tuple[int, int]
Grid = dict[Point, int]


def get_neighbors(point: Point) -> Generator[Point, None, None]:
    """Get the neighbors of a point"""
    for i in range(point[0] - 1, point[0] + 2):
        for j in range(point[1] - 1, point[1] + 2):
            if (i, j) == point or i < 0 or j < 0 or i > 9 or j > 9:
                continue
            yield (i, j)


class OctopusGrid(NamedTuple):
    """Octopus Grid"""

    grid: Grid

    def increment_energy_levels(self) -> None:
        for point in self.grid:
            self.grid[point] += 1

    def reset_overly_energenic(self) -> None:
        for point, value in self.grid.items():
            if value > 9:
                self.grid[point] = 0

    def run_step(self) -> int:
        """Run a step of the simulation

        Returns
        -------
        total_flashed : int
            The number of flashes during this step
        """
        total_flashed = 0
        flashed: set[Point] = set()
        to_flash: list[Point] = []

        self.increment_energy_levels()

        for point, value in self.grid.items():
            if value <= 9:
                continue

            to_flash.append(point)

            while to_flash:
                point = to_flash.pop()
                if point in flashed:
                    continue

                flashed.add(point)
                total_flashed += 1

                for neighbor in get_neighbors(point):
                    self.grid[neighbor] += 1
                    if self.grid[neighbor] > 9:
                        to_flash.append(neighbor)

        self.reset_overly_energenic()
        return total_flashed


class Day11(Solution):
    """Solution to day 11 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 11, "Dumbo Octopus")

    def _part_one(self) -> int:
        """How many total flashes are there after 100 steps?"""

        total_flashed = 0
        octopi = OctopusGrid(self.data)

        for _ in range(100):
            total_flashed += octopi.run_step()

        return total_flashed

    def _part_two(self) -> int:
        """What is the first step during which all octopuses flash?"""
        step = 0
        octopi = OctopusGrid(self.data)

        while True:
            total_flashed = octopi.run_step()
            if total_flashed == 100:
                return step + 1

            step += 1

            if step > 1000:
                break

        raise RuntimeError("Unreachable within 1000 steps")

    def _get_data(self) -> Grid:
        data = self.input.as_list(lambda row: [int(x) for x in row])

        grid = defaultdict(int)
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                grid[(i, j)] = value

        return grid


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day11()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 1656
    assert solution.part_two() == 195


if __name__ == "__main__":
    test_solution(TEST_DATA)
