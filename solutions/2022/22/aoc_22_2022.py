"""Day 22 of Advent of Code 2022"""
import re
from collections import defaultdict

from tools import AOC_TESTING


TEST_DATA = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

TEST_CASES = ((TEST_DATA, 6032, 5031),)


Point = tuple[int, int]

PATH_REGEX = re.compile(r"\d+|[RL]")

DIRECTIONS = ["RIGHT", "DOWN", "LEFT", "UP"]
DIRECTION_STR = {"RIGHT": ">", "DOWN": "v", "LEFT": "<", "UP": "^"}
REVERSE_DIRECTION_STR = {"<": "LEFT", "^": "UP", ">": "RIGHT", "v": "DOWN"}


def parse_board(board_str: str) -> dict[Point, int]:
    """Parse the board"""
    max_len = max(len(line) for line in board_str.splitlines())

    board = defaultdict(lambda: -1)
    for y, line in enumerate(board_str.splitlines()):
        if len(line) < max_len:
            line += " " * (max_len - len(line))

        for x, char in enumerate(line):
            if char == "#":
                board[(x, y)] = 1
            elif char == ".":
                board[(x, y)] = 0

    return board


def show(grid, path):

    min_x = min(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in path:
                print(path[(x, y)], end="")
            elif grid[(x, y)] == 1:
                print("#", end="")
            elif grid[(x, y)] == 0:
                print(".", end="")
            else:
                print(" ", end="")
        print()


def show_faces(faces):

    min_x = min(x for x, y in faces)
    min_y = min(y for x, y in faces)
    max_x = max(x for x, y in faces)
    max_y = max(y for x, y in faces)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):

            if (x, y) not in faces:
                print(" ", end="")
            else:
                print(faces[(x, y)], end="")
        print()


def get_2d_extremes(board: dict[Point, int]) -> tuple[Point, Point]:
    """Get the 2D extremes of the board"""

    x_min = min(x for x, y in board if board[(x, y)] >= 0)
    y_min = min(y for x, y in board if board[(x, y)] >= 0)

    x_max = max(x for x, y in board if board[(x, y)] >= 0)
    y_max = max(y for x, y in board if board[(x, y)] >= 0)

    return (x_min, y_min), (x_max, y_max)


def get_2d_loop_arounds(board: dict[Point, int]) -> dict[Point, tuple[int, int]]:
    loop_arounds = dict()

    _, (board_x_max, board_y_max) = get_2d_extremes(board)

    for loop_y in range(board_y_max + 1):

        leftmost = min(x for x, y in board if y == loop_y)
        rightmost = max(x for x, y in board if y == loop_y)
        loop_arounds[(-1, loop_y)] = (leftmost, rightmost)

    for loop_x in range(board_x_max + 1):

        topmost = min(y for x, y in board if x == loop_x)
        bottommost = max(y for x, y in board if x == loop_x)
        loop_arounds[(loop_x, -1)] = (topmost, bottommost)

    return loop_arounds


def part1(input_str: str) -> int:
    """Part 1 solution"""

    board_str, path = input_str.split("\n\n")
    board = parse_board(board_str)

    loop_arounds = get_2d_loop_arounds(board)
    curr_x, curr_y = loop_arounds[(-1, 0)][0], 0

    path_taken = {}
    direction = "RIGHT"

    for instruction in PATH_REGEX.findall(path):

        if instruction == "R":
            direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]
            continue

        if instruction == "L":
            direction = DIRECTIONS[(DIRECTIONS.index(direction) - 1) % len(DIRECTIONS)]
            continue

        num_steps = int(instruction)

        for _ in range(num_steps):

            path_taken[(curr_x, curr_y)] = DIRECTION_STR[direction]

            if direction == "UP":
                new_x = curr_x
                new_y = curr_y - 1

                if new_y < loop_arounds[(new_x, -1)][0]:
                    new_y = loop_arounds[(new_x, -1)][1]

            elif direction == "DOWN":
                new_x = curr_x
                new_y = curr_y + 1

                if new_y > loop_arounds[(new_x, -1)][1]:
                    new_y = loop_arounds[(new_x, -1)][0]

            elif direction == "LEFT":
                new_y = curr_y
                new_x = curr_x - 1

                if new_x < loop_arounds[(-1, new_y)][0]:
                    new_x = loop_arounds[(-1, new_y)][1]

            elif direction == "RIGHT":
                new_y = curr_y
                new_x = curr_x + 1

                if new_x > loop_arounds[(-1, new_y)][1]:
                    new_x = loop_arounds[(-1, new_y)][0]

            if board[(new_x, new_y)] == 1:
                break

            curr_x, curr_y = new_x, new_y

    # show(board, path_taken)
    # print(curr_x, curr_y, direction)
    return (1000 * (curr_y + 1)) + (4 * (curr_x + 1)) + DIRECTIONS.index(direction)


def part2(input_str: str) -> int:
    """Part 2 solution"""

    FACE_SHAPE = 50 if AOC_TESTING is False else 4

    board_str, path = input_str.split("\n\n")

    board = parse_board(board_str)
    board_x_max, board_y_max = get_2d_extremes(board)[1]

    # first find faces
    loop_arounds_2d = get_2d_loop_arounds(board)
    curr_x, curr_y = loop_arounds_2d[(-1, 0)][0], 0

    face = 1
    faces = defaultdict(int)

    while True:

        if curr_x + FACE_SHAPE > loop_arounds_2d[(-1, curr_y)][1] + 1:
            curr_y += FACE_SHAPE
            if curr_y > board_y_max:
                break

            curr_x = loop_arounds_2d[(-1, curr_y)][0]

        for y in range(curr_y, curr_y + FACE_SHAPE):
            for x in range(curr_x, curr_x + FACE_SHAPE):
                faces[(x, y)] = face

        curr_x += FACE_SHAPE
        face += 1

    face_extremes: dict[int, tuple[Point, Point]] = dict()
    for face in set(faces.values()):
        face_min_x = min(x for (x, y), f in faces.items() if f == face)
        face_min_y = min(y for (x, y), f in faces.items() if f == face)
        face_max_x = max(x for (x, y), f in faces.items() if f == face)
        face_max_y = max(y for (x, y), f in faces.items() if f == face)

        face_extremes[face] = ((face_min_x, face_min_y), (face_max_x, face_max_y))

    # TODO: Make this work for any board!
    if AOC_TESTING:
        BOUNDARIES = {
            1: {">": ("R", 6), "v": ("U", 4), "<": ("U", 3), "^": ("U", 2)},
            2: {">": ("L", 3), "v": ("D", 5), "<": ("D", 6), "^": ("U", 1)},
            3: {">": ("L", 4), "v": ("L", 5), "<": ("R", 2), "^": ("L", 1)},
            4: {">": ("U", 6), "v": ("U", 5), "<": ("R", 3), "^": ("D", 1)},
            5: {">": ("L", 6), "v": ("D", 2), "<": ("D", 3), "^": ("D", 4)},
            6: {">": ("R", 1), "v": ("L", 2), "<": ("R", 5), "^": ("R", 4)},
        }
    else:
        BOUNDARIES = {
            1: {">": ("L", 2), "v": ("U", 3), "<": ("L", 4), "^": ("L", 6)},
            2: {">": ("R", 5), "v": ("R", 3), "<": ("R", 1), "^": ("D", 6)},
            3: {">": ("D", 2), "v": ("U", 5), "<": ("U", 4), "^": ("D", 1)},
            4: {">": ("L", 5), "v": ("U", 6), "<": ("L", 1), "^": ("L", 3)},
            5: {">": ("R", 2), "v": ("R", 6), "<": ("R", 4), "^": ("D", 3)},
            6: {">": ("D", 5), "v": ("U", 2), "<": ("U", 1), "^": ("D", 4)},
        }

    all_moves: set[tuple[str, int]] = set()
    for _, moves in BOUNDARIES.items():
        for _, (side, face) in moves.items():
            all_moves.add((side, face))

    for side in ("L", "R", "U", "D"):
        for face in (1, 2, 3, 4, 5, 6):
            assert (side, face) in all_moves, f"Missing {side} side of face {face}."

    loop_arounds_3d: dict[tuple[int, int, int, str], tuple[Point, str]] = dict()
    NEW_DIRECTION = {"R": "<", "L": ">", "U": "v", "D": "^"}

    for loop_y in range(board_y_max + 1):

        pos_in_face = loop_y % FACE_SHAPE
        faces_in_row = {face for (_, y), face in faces.items() if y == loop_y}

        for face in faces_in_row:

            for move in "<>":

                entry_side, entry_face = BOUNDARIES[face][move]
                (face_min_x, face_min_y), (face_max_x, face_max_y) = face_extremes[entry_face]

                if move == ">" and entry_side == "L":
                    entry_x = face_min_x
                    entry_y = face_min_y + pos_in_face

                elif move == ">" and entry_side == "R":
                    entry_x = face_max_x
                    entry_y = face_max_y - pos_in_face

                elif move == ">" and entry_side == "U":
                    entry_x = face_max_x - pos_in_face
                    entry_y = face_min_y

                elif move == ">" and entry_side == "D":
                    entry_x = face_min_x + pos_in_face
                    entry_y = face_max_y

                elif move == "<" and entry_side == "L":
                    entry_x = face_min_x
                    entry_y = face_max_y - pos_in_face

                elif move == "<" and entry_side == "R":
                    entry_x = face_max_x
                    entry_y = face_min_y + pos_in_face

                elif move == "<" and entry_side == "U":
                    entry_x = face_min_x + pos_in_face
                    entry_y = face_min_y

                elif move == "<" and entry_side == "D":
                    entry_x = face_max_x - pos_in_face
                    entry_y = face_max_y

                new_direction = NEW_DIRECTION[entry_side]
                loop_arounds_3d[(-1, loop_y, face, move)] = ((entry_x, entry_y), new_direction)

    for loop_x in range(board_x_max + 1):

        pos_in_face = loop_x % FACE_SHAPE
        faces_in_col = {face for (x, _), face in faces.items() if x == loop_x}

        for face in faces_in_col:
            for move in "v^":

                entry_side, entry_face = BOUNDARIES[face][move]
                (face_min_x, face_min_y), (face_max_x, face_max_y) = face_extremes[entry_face]

                if move == "v" and entry_side == "L":
                    entry_x = face_min_x
                    entry_y = face_max_y - pos_in_face

                elif move == "v" and entry_side == "R":
                    entry_x = face_max_x
                    entry_y = face_min_y + pos_in_face

                elif move == "v" and entry_side == "U":
                    entry_x = face_min_x + pos_in_face
                    entry_y = face_min_y

                elif move == "v" and entry_side == "D":
                    entry_x = face_max_x - pos_in_face
                    entry_y = face_max_y

                elif move == "^" and entry_side == "L":
                    entry_x = face_min_x
                    entry_y = face_min_y + pos_in_face

                elif move == "^" and entry_side == "R":
                    entry_x = face_max_x
                    entry_y = face_max_y - pos_in_face

                elif move == "^" and entry_side == "U":
                    entry_x = face_max_x - pos_in_face
                    entry_y = face_min_y

                elif move == "^" and entry_side == "D":
                    entry_x = face_min_x + pos_in_face
                    entry_y = face_max_y

                new_direction = NEW_DIRECTION[entry_side]
                loop_arounds_3d[(loop_x, -1, face, move)] = ((entry_x, entry_y), new_direction)

    path_taken = {}
    direction = "RIGHT"
    curr_x, curr_y = loop_arounds_2d[(-1, 0)][0], 0

    for instruction in PATH_REGEX.findall(path):

        if instruction == "R":
            direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]
            continue

        if instruction == "L":
            direction = DIRECTIONS[(DIRECTIONS.index(direction) - 1) % len(DIRECTIONS)]
            continue

        num_steps = int(instruction)

        for _ in range(num_steps):

            path_taken[(curr_x, curr_y)] = DIRECTION_STR[direction]
            current_face = faces[(curr_x, curr_y)]

            (face_min_x, face_min_y), (face_max_x, face_max_y) = face_extremes[current_face]

            new_direction = direction

            if direction == "UP":
                new_x = curr_x
                new_y = curr_y - 1

                if new_y < face_min_y:
                    (new_x, new_y), new_direction = loop_arounds_3d[(new_x, -1, current_face, "^")]

            elif direction == "DOWN":
                new_x = curr_x
                new_y = curr_y + 1

                if new_y > face_max_y:
                    (new_x, new_y), new_direction = loop_arounds_3d[(new_x, -1, current_face, "v")]

            elif direction == "LEFT":
                new_y = curr_y
                new_x = curr_x - 1

                if new_x < face_min_x:
                    (new_x, new_y), new_direction = loop_arounds_3d[(-1, new_y, current_face, "<")]

            elif direction == "RIGHT":
                new_y = curr_y
                new_x = curr_x + 1

                if new_x > face_max_x:
                    (new_x, new_y), new_direction = loop_arounds_3d[(-1, new_y, current_face, ">")]

            if board[(new_x, new_y)] == 1:
                break

            curr_x, curr_y = new_x, new_y
            direction = REVERSE_DIRECTION_STR.get(new_direction, new_direction)

    # show(board, path_taken)
    # print(curr_x, curr_y, direction)
    return (1000 * (curr_y + 1)) + (4 * (curr_x + 1)) + DIRECTIONS.index(direction)


if __name__ == "__main__":

    AOC_TESTING = True

    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
