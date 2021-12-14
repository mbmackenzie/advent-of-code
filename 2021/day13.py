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


Grid = set[tuple[int, int]]
Instructions = list[tuple[str, int]]


def fold_point(point: tuple[int, int], axis: str, value: int) -> tuple[int, int]:
    """Fold a point along a direction"""
    x, y = point

    if axis == "x":
        if x < value:
            return x, y

        diff = x - value
        return value - diff, y

    if axis == "y":
        if y < value:
            return x, y

        diff = y - value
        return x, value - diff

    raise ValueError(f"Invalid axis: {axis}")


def run_instructions(
    grid: Grid, fold_instructions: Instructions, num_instructions: Optional[int] = None
) -> Grid:

    if not num_instructions:
        use_instructions = fold_instructions
    else:
        use_instructions = fold_instructions[:num_instructions]

    showing_points = grid.copy()
    for axis, value in use_instructions:
        new_points = set()
        for point in showing_points:
            new_points.add(fold_point(point, axis, value))

        showing_points = new_points.copy()

    return showing_points


class Day13(Solution):
    """Solution to day 13 of the 2021 Advent of Code"""

    fold_instructions: list[tuple[str, int]]

    def __init__(self) -> None:
        super().__init__(2021, 13, "Transparent Origami")

    def _part_one(self) -> int:
        """
        How many dots are visible after completing just the first fold
        instruction on your transparent paper?
        """
        return len(run_instructions(self.data, self.fold_instructions, 1))

    def _part_two(self) -> str:
        """
        What code do you use to activate the infrared thermal imaging camera system?

        The manual says the code is always eight capital letters.
        """
        final_grid = run_instructions(self.data, self.fold_instructions)

        max_x = max(x for x, _ in final_grid)
        max_y = max(y for _, y in final_grid)
        min_x = min(x for x, _ in final_grid)
        min_y = min(y for _, y in final_grid)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in final_grid:
                    print("#", end="")
                else:
                    print(" ", end="")
            print()

        return "See printed output"

    def _get_data(self) -> set[tuple[int, int]]:
        data = self.input.as_list()

        where_to_split = data.index("")
        coords_list: list[str] = data[:where_to_split]
        folds_list: list[str] = data[where_to_split + 1 :]

        self.fold_instructions = list()
        for fold in folds_list:
            axis, value = fold.replace("fold along ", "").split("=")
            self.fold_instructions.append((axis, int(value)))

        points: set[tuple[int, int]] = set()
        for coord in coords_list:
            x, y = coord.split(",")
            points.add((int(x), int(y)))

        return points


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day13()
    solution.set_input_data(data.split("\n"))

    part_one = solution.part_one()
    solution.part_two()
    assert part_one == 17, f"Part one failed, got {part_one}"
    # assert part_two == NotImplemented, f"Part two failed, got {part_two}"


if __name__ == "__main__":
    test_solution(TEST_DATA)
