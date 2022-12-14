"""Day 14 of Advent of Code 2022"""
from collections import defaultdict
from typing import Optional

TEST_DATA = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

TEST_CASES = ((TEST_DATA, None, None),)


def get_coords(line: str) -> list[tuple[int, int]]:

    coords = []
    for coord in line.split(" -> "):
        x, y = map(int, coord.split(","))
        coords.append((x, y))
    return coords


def draw_grid(grid: dict[tuple[int, int], int], sand_pos: Optional[tuple[int, int]]) -> None:

    max_x = max(x for x, _ in grid.keys())
    min_x = min(x for x, _ in grid.keys())

    max_y = max(y for _, y in grid.keys())
    min_y = min(y for _, y in grid.keys())

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) == sand_pos:
                print("o", end="")
            elif grid[(x, y)] == 0:
                print(".", end="")
            elif grid[(x, y)] == 1:
                print("#", end="")
            elif grid[(x, y)] == 2:
                print("+", end="")
            elif grid[(x, y)] == 3:
                print("o", end="")
        print()


def part1(input_str: str) -> int:
    """Part 1 solution"""

    grid = defaultdict(int)
    grid[(500, 0)] = 2

    for line in input_str.splitlines():
        coords = get_coords(line)

        for c1, c2 in zip(coords, coords[1:]):
            x1, y1 = c1
            x2, y2 = c2

            min_x = min(x1, x2)
            max_x = max(x1, x2)

            min_y = min(y1, y2)
            max_y = max(y1, y2)

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    grid[(x, y)] = 1

    min_x = min(x for x, _ in grid.keys())
    max_x = max(x for x, _ in grid.keys())
    max_y = max(y for _, y in grid.keys())

    num_sands = 0

    while True:
        sand_pos = (500, 0)

        dropping = True
        while dropping:

            if sand_pos[0] > max_x or sand_pos[0] < min_x or sand_pos[1] > max_y:
                return num_sands

            for move in ((0, 1), (-1, 1), (1, 1)):
                x, y = sand_pos
                dx, dy = move
                if grid[(x + dx, y + dy)] == 0:
                    sand_pos = (x + dx, y + dy)
                    break
            else:
                dropping = False
                grid[sand_pos] = 3

        num_sands += 1


def part2(input_str: str) -> int:
    """Part 2 solution"""
    grid = defaultdict(int)
    grid[(500, 0)] = 2

    for line in input_str.splitlines():
        coords = get_coords(line)

        for c1, c2 in zip(coords, coords[1:]):
            x1, y1 = c1
            x2, y2 = c2

            min_x = min(x1, x2)
            max_x = max(x1, x2)

            min_y = min(y1, y2)
            max_y = max(y1, y2)

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    grid[(x, y)] = 1

    max_y = 2 + max(y for _, y in grid.keys())

    min_x = 500 - (max_y + 1)
    max_x = 500 + (max_y + 1)

    for x in range(min_x, max_x + 1):
        grid[(x, max_y)] = 1

    num_sands = 0
    while True:

        # draw_grid(grid)

        sand_pos = (500, 0)

        dropping = True
        while dropping:

            for move in ((0, 1), (-1, 1), (1, 1)):
                x, y = sand_pos
                dx, dy = move
                if grid[(x + dx, y + dy)] == 0:
                    sand_pos = (x + dx, y + dy)
                    break
            else:
                dropping = False
                grid[sand_pos] = 3

                if sand_pos == (500, 0):
                    # draw_grid(grid)
                    return num_sands + 1

        num_sands += 1


if __name__ == "__main__":
    # print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
