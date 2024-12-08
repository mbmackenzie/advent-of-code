import pathlib
from collections import defaultdict
from itertools import combinations
from typing import NamedTuple
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


Point = tuple[int, int]
Grid = dict[Point, str]


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
            if c == ".":
                continue

            grid[(x, y)] = c

    return ParsedInput(grid, max_x, max_y)


def draw_grid(grid: Grid, max_x: int, max_y: int, nodes: set[Point]) -> None:
    out = ""
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in nodes:
                out += "#"
            else:
                out += grid.get((x, y), ".")

        out += "\n"

    print(out)


def part1(input_str: str) -> int:
    grid, max_x, max_y = parse_grid(input_str)

    pos = set()
    nodes = set(grid.values())

    for node in nodes:
        points = {k for k, v in grid.items() if v == node}
        for p1, p2 in combinations(points, 2):
            p1, p2 = sorted([p1, p2], key=lambda x: x[0])

            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            new1 = p1[0] - dx, p1[1] - dy
            new2 = p2[0] + dx, p2[1] + dy

            if 0 <= new1[0] < max_x and 0 <= new1[1] < max_y:
                pos.add(new1)

            if 0 <= new2[0] < max_x and 0 <= new2[1] < max_y:
                pos.add(new2)

    return len(pos)


def part2(input_str: str) -> int:
    grid, max_x, max_y = parse_grid(input_str)

    pos = set()
    nodes = set(grid.values())

    for node in nodes:
        points = {k for k, v in grid.items() if v == node}
        for p1, p2 in combinations(points, 2):
            p1, p2 = sorted([p1, p2], key=lambda x: x[0])

            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            new1 = p1[0], p1[1]
            new2 = p2[0], p2[1]

            while 0 <= new1[0] < max_x and 0 <= new1[1] < max_y:
                pos.add(new1)
                new1 = new1[0] - dx, new1[1] - dy

            while 0 <= new2[0] < max_x and 0 <= new2[1] < max_y:
                pos.add(new2)
                new2 = new2[0] + dx, new2[1] + dy

    return len(pos)


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 14),
    ],
    [
        (TEST_DATA, 34),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
