"""Day 9 of Advent of Code 2022"""
from __future__ import annotations

from collections import OrderedDict
from typing import Iterator
from typing import NamedTuple


TEST_DATA = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

TEST_DATA2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

TEST_CASES = (
    (TEST_DATA, 13, 1),
    (TEST_DATA2, None, 36),
)

DIRECTIONS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, __o: object) -> Point:
        if isinstance(__o, Point):
            return Point(self.x + __o.x, self.y + __o.y)

        return NotImplemented

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Point):
            return self.x == __o.x and self.y == __o.y

        return NotImplemented

    def is_touching(self, other: Point) -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def is_in_line_with(self, other: Point) -> bool:
        return self.x == other.x or self.y == other.y

    def jump_towards(self, other: Point, known_inline_move: Point | None = None) -> Point:

        if self.is_in_line_with(other):

            if known_inline_move is not None:
                return known_inline_move

            if self.x == other.x:
                return Point(0, 1 if other.y > self.y else -1)

            if self.y == other.y:
                return Point(1 if other.x > self.x else -1, 0)

        return Point(*map(lambda x: 1 if x[0] > x[1] else -1, zip(other, self)))


def parse_head_moves(input_str: str) -> Iterator[tuple[Point, int]]:
    for line in input_str.splitlines():
        direction, steps_str = line.split()
        yield Point(*DIRECTIONS[direction]), int(steps_str)


def part1(input_str: str) -> int:
    """Part 1 solution"""

    head = Point(0, 0)
    tail = Point(0, 0)
    visited: set[Point] = {tail}

    for (dhead, steps) in parse_head_moves(input_str):

        for _ in range(steps):

            head = head + dhead

            if head.is_touching(tail):
                continue

            tail = tail + tail.jump_towards(head, known_inline_move=dhead)
            visited.add(tail)

            assert head.is_touching(tail)

    return len(visited)


def part2(input_str: str) -> int:
    """Part 2 solution"""

    initial = Point(0, 0)

    knot_names = ["head", "1", "2", "3", "4", "5", "6", "7", "8", "tail"]
    knots = OrderedDict({k: initial for k in knot_names})
    move_order = list(zip(knot_names, knot_names[1:]))

    visited: set[Point] = {initial}

    for dhead, steps in parse_head_moves(input_str):
        for _ in range(steps):
            for k1, k2 in move_order:
                knot1 = knots[k1]
                knot2 = knots[k2]

                if k1 == "head":
                    knot1 = knot1 + dhead
                    knots[k1] = knot1

                if knot1.is_touching(knot2):
                    continue

                knot2 = knot2 + knot2.jump_towards(knot1)
                knots[k2] = knot2

                if k2 == "tail":
                    visited.add(knot2)

                assert knot1.is_touching(knot2)

    return len(visited)


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    print(part2(TEST_DATA2))

    pass
