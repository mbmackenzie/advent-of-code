import pathlib
from collections import defaultdict
from typing import NamedTuple
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


Point = tuple[int, int]
Grid = dict[Point, int]


class ParsedInput(NamedTuple):
    grid: Grid
    max_x: int
    max_y: int


def parse_grid(input_str: str) -> ParsedInput:
    lines = input_str.splitlines()

    grid = defaultdict(str)

    max_x = len(lines[0])
    max_y = len(lines)

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x, y)] = c

    return ParsedInput(grid, max_x, max_y)


STEPS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
]


def find_regions(grid: Grid, start: Point, placed: set[Point], regions: dict[str, set[str]]):
    if start in placed:
        return

    i = len(regions) + 1
    plant = grid[start]
    to_visit = {start}

    while to_visit:
        x, y = to_visit.pop()
        regions[f"{plant}_{i}"].add((x, y))
        placed.add((x, y))

        for dx, dy in STEPS:
            new = x + dx, y + dy

            if new not in grid:
                continue

            if grid[new] != plant:
                continue

            if new in placed:
                continue

            to_visit.add(new)


def area(region: set[Point]) -> int:
    return len(region)


def perimeter(region: set[Point]) -> int:
    sides_touching = 0
    for x, y in region:
        for dx, dy in STEPS:
            nx = x + dx
            ny = y + dy

            if (nx, ny) in region:
                sides_touching += 1

    return 4 * len(region) - sides_touching


def part1(input_str: str) -> int:
    grid, mx, my = parse_grid(input_str)

    placed = set()
    regions = defaultdict(set)

    for point in grid:
        find_regions(grid, point, placed, regions)

    # print(regions)
    # [print(k, area(region), perimeter(region)) for k, region in regions.items()]
    return sum(area(region) * perimeter(region) for region in regions.values())


def print_grid(grid: Grid, curr: Point) -> None:
    max_x = max(p[0] for p in grid.keys()) + 1
    max_y = max(p[1] for p in grid.keys()) + 1

    for y in range(max_y):
        for x in range(max_x):
            if (x, y) == curr:
                print("@", end="")
            elif grid[(x, y)] == -1:
                print(".", end="")
            else:
                print(grid[(x, y)], end="")
        print()


def bulk_perimeter(region: set[Point]) -> int:
    min_x = min(p[0] for p in region)
    max_x = max(p[0] for p in region) + 1
    min_y = min(p[1] for p in region)
    max_y = max(p[1] for p in region) + 1

    left = []
    right = []
    top = []
    bottom = []

    # scan each column for points with no neighbors to left or right
    for x_ in range(min_x, max_x):
        for x, y in region:
            if x != x_:
                continue

            if (x - 1, y) not in region:
                left.append((x, y))

            if (x + 1, y) not in region:
                right.append((x, y))

    # scan each row for points with no neighbors to top or bottom
    for y_ in range(min_y, max_y):
        for x, y in region:
            if y != y_:
                continue

            if (x, y - 1) not in region:
                top.append((x, y))

            if (x, y + 1) not in region:
                bottom.append((x, y))

    # sort lefts, look up from bottom for adjecent points - if so
    # they share an edge. Remove current point.
    left = sorted(left, key=lambda x: x[1])
    for i in range(len(left) - 1, -1, -1):
        (x, y) = left[i]

        if (x, y - 1) in left:
            left.pop()

    # similar for right
    right = sorted(right, key=lambda x: x[1])
    for i in range(len(right) - 1, -1, -1):
        (x, y) = right[i]

        if (x, y - 1) in right:
            right.pop()

    # similar but look left from right
    top = sorted(top, key=lambda x: x[0])
    for i in range(len(top) - 1, -1, -1):
        (x, y) = top[i]

        if (x - 1, y) in top:
            top.pop()

    # similar
    bottom = sorted(bottom, key=lambda x: x[0])
    for i in range(len(bottom) - 1, -1, -1):
        (x, y) = bottom[i]

        if (x - 1, y) in bottom:
            bottom.pop()

    # remaining points should be 1 per unique edge
    return len(left) + len(right) + len(top) + len(bottom)


def part2(input_str: str) -> int:
    grid, mx, my = parse_grid(input_str)

    placed = set()
    regions = defaultdict(set)

    for point in grid:
        find_regions(grid, point, placed, regions)

    return sum(area(region) * bulk_perimeter(region) for region in regions.values())


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
AAAA
BBCD
BBCC
EEEC
"""

TD2 = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

TD3 = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

TD4 = """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

TD5 = """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 140),
        (TD2, 772),
        (TD3, 1930),
    ],
    [
        (TEST_DATA, 80),
        (TD2, 436),
        (TD4, 236),
        (TD5, 368),
        (TD3, 1206),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
