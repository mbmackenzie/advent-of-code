"""Day 8 of Advent of Code 2022"""
from collections import defaultdict
from typing import Iterator


TEST_DATA = """\
30373
25512
65332
33549
35390
"""

TEST_CASES = ((TEST_DATA, 21, 8),)


Point = tuple[int, int]
Grid = dict[Point, int]

directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "R": (0, 1),
    "L": (0, -1),
}


def parse_grid(input_str: str) -> tuple[Grid, int]:
    grid = defaultdict(lambda: -1)
    lines = input_str.splitlines()

    for i, row in enumerate(lines):
        for j, val in enumerate(row):
            grid[(i, j)] = int(val)

    return grid, len(lines)


def in_perimeter(i: int, j: int, shape: int) -> bool:
    return i in (0, shape - 1) or j in (0, shape - 1)


def in_corner(i: int, j: int, shape: int) -> bool:
    return (i, j) in ((0, 0), (0, shape - 1), (shape - 1, 0), (shape - 1, shape - 1))


def get_tree_line(
    grid: Grid,
    shape: int,
    i: int,
    j: int,
    dx: int = 0,
    dy: int = 0,
) -> Iterator[Point]:

    if (dx == 0 and dy == 0) or (dx != 0 and dy != 0):
        raise ValueError("one of dx and dy must be zero and the other non-zero")

    current_max = grid[(i, j)]

    for k in range(1, shape):

        c = (i + k * dy, j) if dx == 0 else (i, j + k * dx)

        if grid[c] < 0:
            break

        if grid[c] > current_max:
            current_max = grid[c]
            yield c


def part1(input_str: str) -> int:
    """Part 1 solution"""

    grid, shape = parse_grid(input_str)

    visible = set()
    keys = list(grid.keys())
    for i, j in keys:

        if not in_perimeter(i, j, shape):
            continue

        # tree on perimeter is always visible
        visible.add((i, j))

        if in_corner(i, j, shape):
            continue

        # in top row so look down
        if i == 0:
            visible.update(get_tree_line(grid, shape, i, j, dy=1))

        # in bottom row so look up
        if i == shape - 1:
            visible.update(get_tree_line(grid, shape, i, j, dy=-1))

        # in left column so look right
        if j == 0:
            visible.update(get_tree_line(grid, shape, i, j, dx=1))

        # in right column so look left
        if j == shape - 1:
            visible.update(get_tree_line(grid, shape, i, j, dx=-1))

    return len(visible)


def part2(input_str: str) -> int:
    """Part 2 solution"""

    grid, shape = parse_grid(input_str)
    scores = defaultdict(int)

    keys = list(grid.keys())
    for i, j in keys:

        if in_perimeter(i, j, shape):
            continue

        score = 1
        for _, (dx, dy) in directions.items():

            dir_total = 0
            x, y = i, j

            while True:
                x += dx
                y += dy

                # Out of bounds!
                if grid[(x, y)] < 0:
                    break

                dir_total += 1

                # Blocked!
                if grid[(x, y)] >= grid[(i, j)]:
                    break

            score *= dir_total

        scores[(i, j)] = score

    return max(scores.values())


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
