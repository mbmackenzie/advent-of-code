import pathlib
from collections import defaultdict
from typing import NamedTuple
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


deltas = {"^": (0, -1), "<": (-1, 0), ">": (1, 0), "v": (0, 1)}

Point = tuple[int, int]
Delta = tuple[int, int]
Grid = dict[Point, int]


class ParsedInput(NamedTuple):
    grid: Grid
    max_x: int
    max_y: int
    loc: Point
    delta: Delta


def parse_grid(input_str: str) -> ParsedInput:
    lines = input_str.splitlines()

    grid = defaultdict(int)
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1

    guard_loc: Point
    guard_delta: Delta

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ".":
                continue

            if delta := deltas.get(c):
                guard_loc = (x, y)
                guard_delta = delta

                continue

            grid[(x, y)] = 1

    return ParsedInput(grid, max_x, max_y, guard_loc, guard_delta)


def rotate(x, y):
    m = [[0, -1], [1, 0]]

    new_x = m[0][0] * x + m[0][1] * y
    new_y = m[1][0] * x + m[1][1] * y

    return new_x, new_y


def move(loc: Point, delta: Delta, grid: Grid, block: Point = (-1, -1)) -> tuple[Point, Delta]:
    next_loc: Point = loc[0] + delta[0], loc[1] + delta[1]

    if grid[next_loc] == 1 or next_loc == block:
        return loc, rotate(*delta)
    else:
        return next_loc, delta


def in_grid(loc: Point, max_x, max_y, min_x=0, min_y=0) -> bool:
    return min_x <= loc[0] <= max_x and min_y <= loc[1] <= max_y


def part1(input_str: str) -> int:
    grid, mx, my, loc, delta = parse_grid(input_str)

    moves = set()

    while in_grid(loc, mx, my):
        moves.add(loc)
        loc, delta = move(loc, delta, grid)

    return len(moves)


def part2(input_str: str) -> int:
    grid, mx, my, loc, delta = parse_grid(input_str)

    starting_loc = loc
    starting_delta = delta

    obstructions = set(grid.keys())

    moves: set[Point] = set()
    while in_grid(loc, mx, my):
        moves.add(loc)
        loc, delta = move(loc, delta, grid)

    to_check = moves - obstructions - {starting_loc}

    tot_loops = 0
    for block in to_check:
        loc = starting_loc
        delta = starting_delta

        visited = set()

        for _ in range(10_000):
            if not in_grid(loc, mx, my):
                break

            visited.add((loc, delta))
            loc, delta = move(loc, delta, grid, block)

            if (loc, delta) in visited:
                tot_loops += 1
                break
        else:
            print("Max iterations reached")

    return tot_loops


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 41),
    ],
    [
        (TEST_DATA, 6),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
