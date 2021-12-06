"""Day 5"""
from collections import defaultdict
from fractions import Fraction
from typing import NamedTuple

from aoc.solution import Solution

TEST_DATA = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip()


Point = tuple[int, int]


class Line(NamedTuple):
    """Line made with two points, (x1, y1) and (x2, y2)"""

    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def hor_or_vert(self) -> bool:
        """Is the line horizontal or vertical?"""
        return self.x1 == self.x2 or self.y1 == self.y2

    @property
    def slope(self) -> tuple[int, int]:
        """Slope of the line, (dx, dy)"""
        if self.x1 == self.x2:
            return 0, 1 if self.y2 > self.y1 else -1
        if self.y1 == self.y2:
            return 1 if self.x2 > self.x1 else -1, 0

        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        sign_dx = 1 if dx > 0 else -1
        sign_dy = 1 if dy > 0 else -1

        slope = Fraction(abs(dx), abs(dy))
        return sign_dx * slope.numerator, sign_dy * slope.denominator

    @property
    def points(self) -> list[Point]:
        """All the points on this line"""
        dx, dy = self.slope
        x, y = self.x1, self.y1
        points = []

        while x != self.x2 or y != self.y2:
            points.append((x, y))
            x += dx
            y += dy

        points.append((self.x2, self.y2))
        return points


def find_points(lines: list[Line]) -> dict[Point, int]:
    """Find all the points, and how many lines pass through them"""
    points: dict[Point, int] = defaultdict(int)
    for line in lines:
        for point in line.points:
            points[point] += 1

    return points


class Day05(Solution):
    """Solution to day 5 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 5, "")

    def _part_one(self) -> int:
        """
        At how many points do at least two vertical or horizontal
        lines overlap?
        """
        to_consider = [line for line in self.data if line.hor_or_vert]
        points = find_points(to_consider)
        return sum(1 for point in points.values() if point >= 2)

    def _part_two(self) -> int:
        """At how many points do at least two lines overlap?"""
        points = find_points(self.data)
        return sum(1 for point in points.values() if point >= 2)

    def _get_data(self) -> list[Line]:
        def parse_line(line: str) -> Line:
            coord1, coord2 = line.split(" -> ")
            x1, y1 = [int(x) for x in coord1.split(",")]
            x2, y2 = [int(x) for x in coord2.split(",")]
            return Line(x1, y1, x2, y2)

        return self.input.as_list(parse_line)


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day05()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 5
    assert solution.part_two() == 12


if __name__ == "__main__":
    test_solution(TEST_DATA)
