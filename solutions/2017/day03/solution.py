import pathlib
from collections import defaultdict
from typing import Sequence

from tools.common import Point
from tools.runnner import aoc_runner
from tools.runnner import TestCases


def manhattan(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


moves = [
    (1, 0),  # right
    (0, 1),  # up
    (-1, 0),  # left
    (0, -1),  # down
]


def print_grid(grid: dict[Point, int]) -> None:
    min_x = min(grid.keys(), key=lambda x: x[0])[0]
    max_x = max(grid.keys(), key=lambda x: x[0])[0]

    min_y = min(grid.keys(), key=lambda x: x[1])[1]
    max_y = max(grid.keys(), key=lambda x: x[1])[1]

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            print(f"{grid[(x, y)]:>4}", end=" ")
        print()


def part1(input_str: str) -> int:
    if input_str == "1":
        return 0

    grid = defaultdict(int)
    origin = (0, 0)

    target = int(input_str)

    position = origin

    move_count = 0
    steps = 0
    steps_to_move = 1
    current_move = 0

    grid[origin] = 1

    for i in range(2, target + 1):
        steps += 1
        move = moves[current_move]
        position = (position[0] + move[0], position[1] + move[1])
        grid[position] = i

        if steps == steps_to_move:
            steps = 0
            move_count += 1
            current_move = (current_move + 1) % 4

            if move_count == 2:
                steps_to_move += 1
                move_count = 0

    return manhattan(origin, position)


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


def part2(input_str: str) -> int:
    if input_str == "1":
        return 1

    grid = defaultdict(int)
    origin = (0, 0)

    target = int(input_str)

    position = origin

    i = 0
    move_count = 0
    steps = 0
    steps_to_move = 1
    current_move = 0
    largest = 1
    target = int(input_str)

    grid[origin] = 1

    while True:
        if largest > target:
            return largest

        if i >= 1000:
            return -1

        steps += 1
        move = moves[current_move]
        position = (position[0] + move[0], position[1] + move[1])
        grid[position] = 0
        for dx, dy in ADJACENT:
            neighbour = (position[0] + dx, position[1] + dy)
            grid[position] += grid[neighbour]

        if grid[position] > largest:
            largest = grid[position]

        if steps == steps_to_move:
            steps = 0
            move_count += 1
            current_move = (current_move + 1) % 4

            if move_count == 2:
                steps_to_move += 1
                move_count = 0

        i += 1


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_CASES: TestCases = (
    [
        ("1", 0),
        ("12", 3),
        ("23", 2),
        ("1024", 31),
    ],
    [
        ("1", 1),
        ("2", 4),
        ("3", 4),
        ("4", 5),
        ("5", 10),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
