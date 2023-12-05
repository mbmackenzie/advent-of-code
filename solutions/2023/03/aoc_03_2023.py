"""Day 3 of Advent of Code 2023"""
from collections import defaultdict
from functools import reduce
from typing import NamedTuple


TEST_DATA = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

TEST_CASES = ((TEST_DATA, None, None),)


Point = tuple[int, int]
Grid = dict[Point, str]
SymbolToPoints = dict[str, list[Point]]


class Number(NamedTuple):
    starting_point: Point
    value: int


class DiscoveredNumber(NamedTuple):
    original_point: Point
    number: Number


def parse_grid(input_str: str) -> Grid:
    grid = defaultdict(lambda x: ".")

    for y, line in enumerate(input_str.splitlines()):
        for x, c in enumerate(line):
            if c != ".":
                grid[(x, y)] = c

    return grid


def discover_symbol_neighbours(symbols: SymbolToPoints, grid: Grid, point: Point) -> list[Point]:
    x, y = point

    # orthogonals
    orthogonals = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    diagonals = [(1, 1), (-1, -1), (-1, 1), (1, -1)]

    for dx, dy in orthogonals + diagonals:
        new_point = (x + dx, y + dy)
        if new_point in grid and not grid[new_point].isdigit():
            symbols[new_point].append(point)

    return symbols


def get_symbol_neighbours(grid: Grid) -> SymbolToPoints:
    symbol_lookup = defaultdict(list)
    for point, value in grid.items():
        if not value.isdigit():
            continue

        discover_symbol_neighbours(symbol_lookup, grid, point)

    return symbol_lookup


def discover_number(grid: Grid, point: Point) -> DiscoveredNumber:
    digits = []

    x, y = point
    while True:
        x -= 1
        if (x, y) not in grid or not grid[(x, y)].isdigit():
            break

    starting_point = (x, y)

    while True:
        x += 1
        if (x, y) not in grid or not grid[(x, y)].isdigit():
            break

        digits.append(grid[(x, y)])

    value = int("".join(digits))
    number = Number(starting_point, value)
    return DiscoveredNumber(point, number)


def part1(input_str: str) -> int:
    """Part 1 solution"""

    grid = parse_grid(input_str)
    sym_to_points = get_symbol_neighbours(grid)

    to_discover = reduce(lambda x, y: x.union(y), sym_to_points.values(), set())
    discovered = [discover_number(grid, point) for point in to_discover]

    numbers = set(num.number for num in discovered)
    return sum(num.value for num in numbers)


def part2(input_str: str) -> int:
    """Part 2 solution"""
    grid = parse_grid(input_str)
    symbals = get_symbol_neighbours(grid)

    next_to_symbol = list(reduce(lambda x, y: x.union(y), symbals.values(), set()))

    point_to_num_map = {}
    starting_point_to_num_map = {}
    nums = []
    for x, y in next_to_symbol:
        original_point = (x, y)
        right_digits = []

        while True:
            x -= 1
            if (x, y) not in grid or not grid[(x, y)].isdigit():
                break

        starting_point = (x, y)

        while True:
            x += 1
            if (x, y) not in grid or not grid[(x, y)].isdigit():
                break

            right_digits.append(grid[(x, y)])

        point_to_num_map[original_point] = starting_point
        starting_point_to_num_map[starting_point] = int("".join(right_digits))

    symbals_to_starting_points = {}
    for sym, points in symbals.items():
        symbals_to_starting_points[sym] = set([point_to_num_map[point] for point in points])

    print(symbals_to_starting_points)

    tot = 0
    for sym, starting_points in symbals_to_starting_points.items():
        if len(starting_points) == 2:
            num1 = starting_point_to_num_map[starting_points.pop()]
            num2 = starting_point_to_num_map[starting_points.pop()]
            gr = num1 * num2
            tot += gr

    return tot


if __name__ == "__main__":
    # print(part1(TEST_DATA))
    print(part2(TEST_DATA))
