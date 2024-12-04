import pathlib
from collections import defaultdict
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


ADJACENT = [
    (1, 0),  # right
    (1, 1),  # up right
    (0, 1),  # up
    (-1, 1),  # up left
    (-1, 0),  # left
    (-1, -1),  # down left
    (0, -1),  # down
    (1, -1),  # down right
]

DIAGS = [
    (1, 1),  # up right
    (-1, 1),  # up left
    (-1, -1),  # down left
    (1, -1),  # down right
]


def parse_grid(input_str: str) -> dict[tuple[int, int], str]:
    grid = defaultdict(str)

    for y, line in enumerate(input_str.splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = c

    return grid


def part1(input_str: str) -> int:
    grid = parse_grid(input_str)

    tot = 0
    xs = [k for k, v in grid.items() if v == "X"]

    for x, y in xs:
        for dx, dy in ADJACENT:
            if grid[(x + dx, y + dy)] != "M":
                continue

            if grid[x + dx * 2, y + dy * 2] != "A":
                continue

            if grid[x + dx * 3, y + dy * 3] != "S":
                continue

            tot += 1

    return tot


def part2(input_str: str) -> int:
    grid = parse_grid(input_str)

    ms = [k for k, v in grid.items() if v == "M"]
    a_pts = defaultdict(int)

    for x, y in ms:
        for dx, dy in DIAGS:
            if grid[(x + dx, y + dy)] != "A":
                continue

            if grid[x + dx * 2, y + dy * 2] != "S":
                continue

            a_pts[(x + dx, y + dy)] += 1

    return sum(v == 2 for v in a_pts.values())


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"


TEST_DATA_SMALL = """\
..X...
.SAMX.
.A..A.
XMAS.S
.X....
"""

TEST_DATA = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


TEST_CASES: TestCases = (
    [
        (TEST_DATA_SMALL, 4),
        (TEST_DATA, 18),
    ],
    [
        (TEST_DATA, 9),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
