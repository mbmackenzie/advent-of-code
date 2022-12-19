"""Day 15 of Advent of Code 2022"""
import re
from collections import defaultdict
from typing import Iterator

from tools import AOC_TESTING

TEST_DATA = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

TEST_CASES = ((TEST_DATA, 26, 56000011),)

REGEX = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

Point = tuple[int, int]


def draw_grids(
    *grids: dict[Point, int | str | None],
    constraints: tuple[int, ...] | None = None,
) -> None:

    big_grid: dict[Point, int | str | None] = defaultdict(lambda: None)

    for grid in grids:
        big_grid.update(grid)

    if constraints:
        min_x, max_x, min_y, max_y = constraints
    else:
        max_x = max(x for x, _ in big_grid.keys())
        min_x = min(x for x, _ in big_grid.keys())
        max_y = max(y for _, y in big_grid.keys())
        min_y = min(y for _, y in big_grid.keys())

    print(min_x, max_x, min_y, max_y)

    print(f"{' ':>10}", end="  ")
    for x in range(min_x, max_x + 1):
        if x % 5 == 0:
            print(x, end=" ")
        else:
            print(" ", end=" ")

    print()
    for y in range(min_y, max_y + 1):
        print(f"{y:>10}", end="  ")
        for x in range(min_x, max_x + 1):

            if (val := big_grid[(x, y)]) in ("", 0, None):
                print(".", end=" ")
            elif isinstance(val, int) and val >= 1:
                print("#", end=" ")
            else:
                print(val, end=" ")
        print()


def get_perimeter(x: int, y: int, dist: int, fillin: bool = False) -> Iterator[tuple[int, int]]:

    perimeter = set()
    for i in range(dist):
        perimeter.add((x + i, y + dist - i))
        perimeter.add((x - i, y - dist + i))
        perimeter.add((x + dist - i, y - i))
        perimeter.add((x - dist + i, y + i))

    if not fillin:
        yield from perimeter

    else:

        max_x = max(x for x, _ in perimeter)
        min_x = min(x for x, _ in perimeter)
        max_y = max(y for _, y in perimeter)
        min_y = min(y for _, y in perimeter)

        for ix in range(min_x, max_x + 1):
            for iy in range(min_y, max_y + 1):
                if abs(ix - x) + abs(iy - y) <= dist:
                    yield (ix, iy)


def parse_input(input_str: str) -> tuple[dict[Point, str], dict[Point, int]]:
    grid = dict()
    sensor_dist = defaultdict(int)

    for line in input_str.splitlines():
        coords = REGEX.findall(line)[0]
        x1, y1 = map(int, coords[:2])
        x2, y2 = map(int, coords[2:])

        grid[(x1, y1)] = "S"
        grid[(x2, y2)] = "B"

        sensor_dist[(x1, y1)] = abs(x1 - x2) + abs(y1 - y2)

    return grid, sensor_dist


def get_xintercepts(sensor: Point, radius: int, row: int) -> Point | None:
    """Solve this system:

    1) y = row
    2) abs(x1 - sensor[0]) + abs(y1 - sensor[1]) = radius
    """
    right_side = radius - abs(row - sensor[1])

    pos_case = sensor[0] + right_side
    neg_case = sensor[0] - right_side

    if abs(pos_case - sensor[0]) == abs(neg_case - sensor[0]) == right_side:
        return (neg_case, pos_case)

    return None


def part1(input_str: str) -> int:
    """Part 1 solution"""

    grid, sensor_dist = parse_input(input_str)

    row = 10 if AOC_TESTING else 2000000
    row_intersections: set[int] = set()

    for (x, y), dist in sensor_dist.items():

        if (xintercepts := get_xintercepts((x, y), dist, row)) is not None:
            row_intersections.update(range(xintercepts[0], xintercepts[1] + 1))

    row_spaces_filled = {x for x, y in grid.keys() if y == row}
    return len(row_intersections - row_spaces_filled)


def part2(input_str: str) -> int:
    """Part 2 solution"""
    grid, sensor_dist = parse_input(input_str)

    lower_limit = 0
    upper_limit = 20 if AOC_TESTING else 4000000

    for (x, y), dist in sensor_dist.items():

        for (px, py) in get_perimeter(x, y, dist + 1):

            if px < lower_limit or px > upper_limit or py < lower_limit or py > upper_limit:
                continue

            if (px, py) in grid:
                continue

            for (sx, sy), sdist in sensor_dist.items():
                if abs(px - sx) + abs(py - sy) <= sdist:
                    break
            else:
                return px * 4000000 + py

    raise ValueError("No solution found!")


if __name__ == "__main__":

    AOC_TESTING = True

    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
