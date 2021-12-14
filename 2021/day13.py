"""Day 13: Transparent Origami"""
from typing import Optional

from aoc.solution import Solution


TEST_DATA = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".strip()


Point = tuple[int, int]
Grid = set[Point]

Fold = tuple[str, int]
Folds = list[Fold]


def fold_point(point: Point, axis: str, value: int) -> Point:
    """Fold a point along a direction"""
    x, y = point
    if axis == "x":
        new_x = x if x < value else value - (x - value)
        return new_x, y
    elif axis == "y":
        new_y = y if y < value else value - (y - value)
        return x, new_y
    else:
        raise ValueError(f"Invalid axis: {axis}")


def run_instructions(grid: Grid, folds: Folds, n_folds: Optional[int] = None) -> Grid:

    showing_points = grid
    for i, (axis, value) in enumerate(folds):

        new_points = set()
        for point in showing_points:
            new_points.add(fold_point(point, axis, value))

        showing_points = new_points

        if n_folds and i == n_folds - 1:
            break

    return showing_points


def show_grid(grid: Grid) -> None:
    """Show the grid"""
    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in grid:
                print("#", end="")
            else:
                print(" ", end="")
        print()


class Day13(Solution):
    """Solution to day 13 of the 2021 Advent of Code"""

    folds: Folds

    def __init__(self) -> None:
        super().__init__(2021, 13, "Transparent Origami")

    def _part_one(self) -> int:
        """
        How many dots are visible after completing just the first fold
        instruction on your transparent paper?
        """
        return len(run_instructions(self.data, self.folds, 1))

    def _part_two(self) -> str:
        """
        What code do you use to activate the infrared thermal imaging camera system?
        The manual says the code is always eight capital letters.
        """
        show_grid(run_instructions(self.data, self.folds))
        return "See printed output"

    def _get_data(self) -> Grid:
        data = "\n".join(self.input.as_list())
        coords_str, folds_str = data.split("\n\n")

        self.folds = list()
        for fold in folds_str.split("\n"):
            axis, value = fold.replace("fold along ", "").split("=")
            self.folds.append((axis, int(value)))

        points: Grid = set()
        for coord in coords_str.split("\n"):
            x, y = coord.split(",")
            points.add((int(x), int(y)))

        return points


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day13()
    solution.set_input_data(data.split("\n"))

    part_one = solution.part_one()
    assert part_one == 17, f"Part one failed, got {part_one}"

    solution.part_two()


if __name__ == "__main__":
    test_solution(TEST_DATA)
