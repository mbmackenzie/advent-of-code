"""Day 12 of Advent of Code 2022"""
from __future__ import annotations

from collections import defaultdict
from collections import deque
from typing import Iterator
from typing import NamedTuple

TEST_DATA = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

TEST_CASES = ((TEST_DATA, 31, 29),)


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


MOVES = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]


def parse_grid(input_str: str) -> tuple[Point, Point, dict[Point, int]]:
    grid = defaultdict(int)

    for y, line in enumerate(input_str.splitlines()):
        for x, char in enumerate(line):

            if char == "S":
                char = "a"
                start = Point(x, y)
            elif char == "E":
                char = "z"
                end = Point(x, y)

            grid[Point(x, y)] = ord(char) - ord("a") + 1

    if start is None or end is None:
        raise ValueError("Start or end not found")

    return start, end, grid


def get_neighbors(point: Point) -> Iterator[Point]:
    for move in MOVES:
        yield point + move


def get_shortest_paths_from(grid: dict[Point, int], start: Point) -> dict[Point, float]:
    visited = set()
    queue = deque([start])

    shortest_paths: dict[Point, float] = defaultdict(lambda: float("inf"))
    shortest_paths[start] = 0

    while queue:
        point = queue.popleft()

        if point in visited:
            continue

        visited.add(point)

        for new_point in get_neighbors(point):
            if new_point in grid and grid[point] - grid[new_point] <= 1:
                if (dist := shortest_paths[point] + 1) <= shortest_paths[new_point]:
                    shortest_paths[new_point] = dist
                queue.append(new_point)

    return shortest_paths


def part1(input_str: str) -> float:
    """Part 1 solution"""
    start, end, grid = parse_grid(input_str)
    paths = get_shortest_paths_from(grid, end)

    return paths[start]


def part2(input_str: str) -> float:
    """Part 2 solution"""
    _, end, grid = parse_grid(input_str)
    paths = get_shortest_paths_from(grid, end)

    low_points = [point for point, value in grid.items() if value == 1]
    return int(min(paths[point] for point in low_points))


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
