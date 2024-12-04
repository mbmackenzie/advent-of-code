import pathlib
from typing import Sequence

from tools.common import Point
from tools.runnner import aoc_runner
from tools.runnner import TestCases


def manhattan(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def get_points(wire: list[str]) -> list[Point]:
    x, y = 0, 0
    points = []

    for move in wire:
        direction = move[0]
        distance = int(move[1:])

        for _ in range(distance):
            if direction == "U":
                y += 1
            elif direction == "D":
                y -= 1
            elif direction == "L":
                x -= 1
            elif direction == "R":
                x += 1
            else:
                raise ValueError(f"Invalid direction: {direction}")

            points.append((x, y))

    return points


def part1(input_str: str) -> int:
    wire1, wire2 = input_str.strip().splitlines()
    wire1_points = get_points(wire1.split(","))
    wire2_points = get_points(wire2.split(","))

    intersections = set(wire1_points) & set(wire2_points)

    return min(manhattan(0, 0, x, y) for x, y in intersections)


def steps_to_intersection(wire: list[Point], intersections: set[Point]) -> dict[Point, int]:
    points: dict[Point, int] = {}
    for point in intersections:
        points[point] = wire.index(point) + 1

    return points


def part2(input_str: str) -> int:
    wire1, wire2 = input_str.strip().splitlines()
    wire1_points = get_points(wire1.split(","))
    wire2_points = get_points(wire2.split(","))

    intersections = set(wire1_points) & set(wire2_points)

    wire1_steps = steps_to_intersection(wire1_points, intersections)
    wire2_steps = steps_to_intersection(wire2_points, intersections)

    return min(wire1_steps[point] + wire2_steps[point] for point in intersections)


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_1 = """\
R8,U5,L5,D3
U7,R6,D4,L4
"""

TEST_2 = """\
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
"""

TEST_3 = """\
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
"""

TEST_CASES: TestCases = (
    [
        (TEST_1, 6),
        (TEST_2, 159),
        (TEST_3, 135),
    ],
    [
        (TEST_2, 610),
        (TEST_3, 410),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
