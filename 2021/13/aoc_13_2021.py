"""Day 13: Transparent Origami"""
from typing import Optional


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

TEST_CASES = ((TEST_DATA, 17, "See printed output"),)


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


def _get_data(input_str: str) -> tuple[Folds, Grid]:
    coords_str, folds_str = input_str.split("\n\n")

    folds: Folds = list()
    for fold in folds_str.strip().split("\n"):
        axis, value = fold.replace("fold along ", "").split("=")
        folds.append((axis, int(value)))

    points: Grid = set()
    for coord in coords_str.strip().split("\n"):
        x, y = coord.split(",")
        points.add((int(x), int(y)))

    return folds, points


def part1(input_str: str) -> int:
    """
    How many dots are visible after completing just the first fold
    instruction on your transparent paper?
    """

    folds, data = _get_data(input_str)
    return len(run_instructions(data, folds, 1))


def part2(input_str: str) -> str:
    """
    What code do you use to activate the infrared thermal imaging camera system?
    The manual says the code is always eight capital letters.
    """
    folds, data = _get_data(input_str)
    show_grid(run_instructions(data, folds))
    return "See printed output"


if __name__ == "__main__":

    with open(".aoc_cache/2021_13.txt", "r") as f:
        input_str = f.read().strip()

    print(part1(input_str))
    print(part2(input_str))
