"""Day {day} of Advent of Code {year}"""
import re
from collections import defaultdict
from collections import namedtuple
from typing import Iterator


TEST_DATA = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


TEST_CASES = ((TEST_DATA, "CMZ", "MCD"),)


Stacks = dict[int, list[str]]
Move = namedtuple("Move", ["n", "from_", "to_"])
Moves = Iterator[Move]


move_regex = re.compile(r"move (\d+) from (\d+) to (\d+)")
stack_regex = re.compile(r"(\s{3}|\[([A-Z])\])\s?")


def parse_and_get_initial_state(input_str: str) -> tuple[Stacks, Moves]:
    stacks_str, moves_str = input_str.split("\n\n")

    stacks: Stacks = defaultdict(list)
    for stack_level in stacks_str.splitlines():
        print(stack_regex.findall(stack_level))
        for i, crate in enumerate(stack_regex.findall(stack_level)):
            if crate[0].strip():
                stacks[i + 1].append(crate[1])

    moves = (Move(*map(int, move)) for move in move_regex.findall(moves_str))
    return stacks, moves


def get_solution(stacks: Stacks) -> str:
    return "".join(stacks[s][0] for s in range(1, len(stacks) + 1))


def part1(input_str: str) -> str:
    """Part 1 solution"""

    stacks, moves = parse_and_get_initial_state(input_str)

    for move in moves:
        for _ in range(move.n):
            move_crate = stacks[move.from_].pop(0)
            stacks[move.to_].insert(0, move_crate)

    return get_solution(stacks)


def part2(input_str: str) -> str:
    """Part 2 solution"""
    stacks, moves = parse_and_get_initial_state(input_str)

    for move in moves:
        if move.n == 1:
            move_crate = stacks[move.from_].pop(0)
            stacks[move.to_].insert(0, move_crate)
        else:

            tmp = []
            for _ in range(move.n):
                tmp.append(stacks[move.from_].pop(0))

            for _ in range(move.n):
                stacks[move.to_].insert(0, tmp.pop())

    return get_solution(stacks)


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
