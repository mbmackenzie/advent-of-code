"""Day 17 of Advent of Code 2022"""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable
from typing import Iterator
from typing import NamedTuple


TEST_DATA = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""

"""\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

TEST_CASES = ((TEST_DATA, None, None),)

Point = tuple[int, int]


class Grid(NamedTuple):
    resting: set[Point] = set()

    @property
    def highest_y(self) -> int:
        if len(self.resting) == 0:
            return -1

        return max(y for _, y in self.resting)

    @property
    def highest_points(self) -> set[Point]:

        high_y = self.highest_y
        if len(self.resting) == 0:
            return {(x, high_y) for x in range(-3, 4)}

        return {(x, y) for x, y in self.resting if y == high_y}


class Shape(NamedTuple):

    points: set[Point]

    @property
    def lowest_x(self) -> int:
        if len(self.points) == 0:
            return -1
        return min(x for x, _ in self.points)

    @property
    def highest_x(self) -> int:
        if len(self.points) == 0:
            return -1
        return max(x for x, _ in self.points)

    @property
    def lowest_y(self) -> int:
        if len(self.points) == 0:
            return -1
        return min(y for _, y in self.points)

    @property
    def highest_y(self) -> int:
        if len(self.points) == 0:
            return -1
        return max(y for _, y in self.points)

    @property
    def leftmost_points(self) -> set[Point]:
        return {(x, y) for x, y in self.points if x == self.lowest_x}

    @property
    def rightmost_points(self) -> set[Point]:
        return {(x, y) for x, y in self.points if x == self.highest_x}

    @property
    def lowest_points(self) -> set[Point]:
        return {(x, y) for x, y in self.points if y == self.lowest_y}

    def translate(self, dx: int, dy: int) -> Shape:
        return Shape({(x + dx, y + dy) for x, y in self.points})

    def push(self, dx: int, dy: int, resting_points: set[Point]) -> Shape:

        new_shape = self.translate(dx, dy)

        if new_shape.points & resting_points:
            return self

        if new_shape.lowest_y < 0 or new_shape.lowest_x < -3 or new_shape.highest_x > 3:
            return self

        return new_shape

    def push_left(self, resting_points: set[Point]) -> Shape:
        return self.push(-1, 0, resting_points)

    def push_right(self, resting_points: set[Point]) -> Shape:
        return self.push(1, 0, resting_points)

    def move_down(self, resting_points: set[Point]) -> Shape:
        return self.push(0, -1, resting_points)


def draw(grid: Grid, shape: Shape | None = None) -> None:

    if shape is None:
        shape = Shape(set())

    max_y = max(grid.highest_y, shape.highest_y)

    for y in range(max_y, -1, -1):
        print("|", end="")

        for x in range(-3, 4):

            if (x, y) in grid.resting:
                print("#", end="")
            elif (x, y) in shape.points:
                print("@", end="")
            else:
                print(".", end="")

        print("|", end="")
        print()

    print("+", end="")

    for _ in range(7):
        print("-", end="")

    print("+", end="")

    print()
    print()


class Rocks:
    """Rocks with left most corner centered at 0, 0"""

    @property
    def minus(self) -> Shape:
        return Shape({(0, 0), (1, 0), (2, 0), (3, 0)})

    @property
    def plus(self) -> Shape:
        return Shape({(0, 0), (1, 0), (2, 0), (1, 1), (1, -1)})

    @property
    def backwards_L(self) -> Shape:
        return Shape({(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)})

    @property
    def line(self) -> Shape:
        return Shape({(0, 0), (0, 1), (0, 2), (0, 3)})

    @property
    def square(self) -> Shape:
        return Shape({(0, 0), (1, 0), (0, 1), (1, 1)})

    def __iter__(self) -> Iterator[Shape]:
        seq = [self.minus, self.plus, self.backwards_L, self.line, self.square]

        i = 0
        while True:
            yield seq[i % len(seq)]
            i += 1


def part1(input_str: str) -> int:
    """Part 1 solution"""

    sequence = input_str.strip()

    grid = Grid()

    seq_pos = -1
    num_rocks_stopped = 0

    for rock in Rocks():

        shape = rock.translate(-1, grid.highest_y - rock.lowest_y + 4)

        while True:
            seq_pos += 1
            move = sequence[seq_pos % len(sequence)]

            if move == "<":
                pushed_shape = shape.push_left(grid.resting)
            elif move == ">":
                pushed_shape = shape.push_right(grid.resting)
            else:
                raise ValueError(f"Unknown move {move}")

            new_shape = pushed_shape.move_down(grid.resting)

            if pushed_shape == new_shape:
                grid.resting.update(new_shape.points)
                num_rocks_stopped += 1
                break

            shape = new_shape

        # draw(grid, new_shape)
        if num_rocks_stopped == 2022:
            break

    return grid.highest_y + 1


def part2(input_str: str) -> int:
    """Part 2 solution"""

    MAX_ROCKS = 1_000_000_000_000

    raise NotImplementedError


if __name__ == "__main__":
    # print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
