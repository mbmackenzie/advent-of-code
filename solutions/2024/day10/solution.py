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

    grid = defaultdict(lambda: -1)

    max_x = len(lines[0])
    max_y = len(lines)

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ".":
                continue

            grid[(x, y)] = int(c)

    return ParsedInput(grid, max_x, max_y)


STEPS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
]


def print_grid(grid: Grid, max_x: int, max_y: int, curr: Point) -> None:
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) == curr:
                print("@", end="")
            elif grid[(x, y)] == -1:
                print(".", end="")
            else:
                print(grid[(x, y)], end="")
        print()


def part1(input_str: str) -> int:
    grid, max_x, max_y = parse_grid(input_str)

    trail_heads = {k for k, v in grid.items() if v == 0}

    tot_nines = 0

    for start in trail_heads:
        nines = set()
        to_visit = {start}

        while to_visit:
            x, y = to_visit.pop()
            curr = grid[(x, y)]

            if grid[(x, y)] == 9:
                nines.add((x, y))
                continue

            for dx, dy in STEPS:
                new_x, new_y = x + dx, y + dy

                if new_x < 0 or new_x >= max_x or new_y < 0 or new_y >= max_y:
                    continue

                if (new_x, new_y) not in grid:
                    continue

                if grid[(new_x, new_y)] != curr + 1:
                    continue

                to_visit.add((new_x, new_y))

        tot_nines += len(nines)

    return tot_nines


def part2(input_str: str) -> int:
    grid, max_x, max_y = parse_grid(input_str)

    trail_heads = {k for k, v in grid.items() if v == 0}

    paths = []

    for start in trail_heads:
        to_visit = [(start, [start])]

        while to_visit:
            (x, y), path = to_visit.pop()

            curr = grid[(x, y)]

            if grid[(x, y)] == 9:
                paths.append(path)
                continue

            for dx, dy in STEPS:
                new_x, new_y = x + dx, y + dy
                new_path = path + [(new_x, new_y)]

                if new_x < 0 or new_x >= max_x or new_y < 0 or new_y >= max_y:
                    continue

                if (new_x, new_y) not in grid:
                    continue

                if grid[(new_x, new_y)] != curr + 1:
                    continue

                to_visit.append(((new_x, new_y), new_path))

    return len(paths)


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
0123
1234
8765
9876
"""

T2 = """\
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
"""

T3 = """\
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
"""

T4 = """\
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
"""

T5 = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

T6 = """\
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
"""

T7 = """\
012345
123456
234567
345678
4.6789
56789.
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 1),
        (T2, 2),
        (T3, 4),
        (T4, 3),
        (T5, 36),
    ],
    [
        (T6, 3),
        (T3, 13),
        (T7, 227),
        (T5, 81),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
