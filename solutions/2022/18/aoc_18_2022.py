"""Day 18 of Advent of Code 2022"""
from __future__ import annotations

import itertools
from typing import Iterator
from typing import NamedTuple

SIMPLE_DATA = """\
1,1,1
2,1,1
"""

TEST_DATA = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""


MY_EXAMPLE = ""
for x in range(5):
    for y in range(5):
        for z in range(5):

            if abs(x - 2) <= 1 and abs(y - 2) <= 1 and abs(z - 2) <= 1:
                continue

            MY_EXAMPLE += f"{x},{y},{z}\n"


TEST_CASES = ((TEST_DATA, 64, 58), (MY_EXAMPLE, 204, 150))

Array3D = list[list[list[int]]]


class Point(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def from_str(input: str) -> Point:
        x, y, z = input.split(",")
        return Point(int(x), int(y), int(z))


def get_neighbors_xyz(x: int, y: int, z: int) -> Iterator[tuple[int, int, int]]:

    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1


def get_neighbors(point: Point) -> Iterator[Point]:
    yield from (Point(*n) for n in get_neighbors_xyz(point.x, point.y, point.z))


def draw(arr3d: Array3D) -> None:
    print("\n\nAfter filling")
    for arr2d in arr3d:
        for arr1d in arr2d:
            for v in arr1d:
                if v == 2:
                    print("O", end="")
                elif v == 1:
                    print("#", end="")
                else:
                    print(".", end="")

            print()
        print()


def get_arr3d(coords: set[Point]) -> tuple[Array3D, int, int, int]:
    max_x = max([p.x for p in coords])
    max_y = max([p.y for p in coords])
    max_z = max([p.z for p in coords])

    arr3d: Array3D = []
    for x in range(max_x + 1):
        arr2d = []
        for y in range(max_y + 1):
            arr1d = [0] * (max_z + 1)
            arr2d.append(arr1d)
        arr3d.append(arr2d)

    for p in coords:
        arr3d[p.x][p.y][p.z] = 1

    return arr3d, max_x, max_y, max_z


def iter_arr3d(max_x: int, max_y: int, max_z: int) -> Iterator[tuple[int, int, int]]:
    for x, y, z in itertools.product(range(max_x + 1), range(max_y + 1), range(max_z + 1)):
        yield x, y, z


def run_from_seed(arr3d: Array3D, seed: Point, max_x: int, max_y: int, max_z: int) -> bool:

    success = True
    stack = [(seed.x, seed.y, seed.z)]

    while stack:

        x, y, z = stack.pop()
        arr3d[x][y][z] = -1

        for xn, yn, zn in get_neighbors_xyz(x, y, z):
            if xn > max_x or yn > max_y or zn > max_z or xn < 0 or yn < 0 or zn < 0:
                success = False
                continue

            if arr3d[xn][yn][zn] == 0:
                stack.append((xn, yn, zn))

    for x, y, z in iter_arr3d(max_x, max_y, max_z):
        if arr3d[x][y][z] == -1:
            arr3d[x][y][z] = 2 if success else -2

    return success


def part1(input_str: str) -> int:
    """Part 1 solution"""

    coords = {Point.from_str(line) for line in input_str.splitlines()}

    sides_exposed = {}
    for p in coords:
        num_sides_exposed = 0
        for pn in get_neighbors(p):
            if pn not in coords:
                num_sides_exposed += 1

        sides_exposed[p] = num_sides_exposed

    return sum(sides_exposed.values())


def part2(input_str: str) -> int:
    """Part 2 solution"""

    coords = {Point.from_str(line) for line in input_str.splitlines()}
    arr3d, max_x, max_y, max_z = get_arr3d(coords)

    good_seeds = set()
    for x, y, z in iter_arr3d(max_x, max_y, max_z):

        if arr3d[x][y][z] != 0:
            continue

        p = Point(x, y, z)
        if run_from_seed(arr3d, p, max_x, max_y, max_z):
            good_seeds.add(p)

    # print(f"Good seeds: {good_seeds}")

    filled_points = set()
    for x, y, z in iter_arr3d(max_x, max_y, max_z):
        if arr3d[x][y][z] == 2:
            filled_points.add(Point(x, y, z))

    sides_exposed = {}
    for p in coords:
        num_sides_exposed = 0
        for pn in get_neighbors(p):
            if pn not in coords and pn not in filled_points:
                num_sides_exposed += 1

        sides_exposed[p] = num_sides_exposed

    return sum(sides_exposed.values())


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
