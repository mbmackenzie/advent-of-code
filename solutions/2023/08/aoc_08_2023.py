"""Day 8 of Advent of Code 2023"""
from __future__ import annotations

import math
from typing import Callable
from typing import NamedTuple


TEST_DATA = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

TEST_2 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

TEST_CASES = ((TEST_DATA, None, None),)


class Node(NamedTuple):
    start: str
    left: str
    right: str


def parse_input(input_str: str) -> tuple[str, dict[str, Node]]:
    lines = input_str.splitlines()
    instructions = lines.pop(0)
    lines.pop(0)

    nodes = {}
    for line in lines:
        start, _, where_to = line.partition(" = ")
        where_to = where_to[1:-1]
        left, _, right = where_to.partition(", ")

        nodes[start] = Node(start, left, right)

    return instructions, nodes


def get_path_length(
    instructions: str,
    start: str,
    nodes: dict[str, Node],
    is_end: Callable[[str], bool],
) -> int:
    idx = 0
    current = nodes[start]

    while True:
        to_move = instructions[idx % len(instructions)]

        if to_move == "R":
            next_node = current.right
        elif to_move == "L":
            next_node = current.left

        if is_end(next_node):
            return idx + 1

        current = nodes[next_node]
        idx += 1


def part1(input_str: str) -> int:
    """Part 1 solution"""

    instructions, nodes = parse_input(input_str)

    start = "AAA"
    end = "ZZZ"

    return get_path_length(instructions, start, nodes, lambda x: x == end)


def part2(input_str: str) -> int:
    """Part 2 solution"""

    instructions, nodes = parse_input(input_str)

    start_nodes = [node for node in nodes if node.endswith("A")]
    end_nodes = [node for node in nodes if node.endswith("Z")]

    lengths = [
        get_path_length(instructions, start, nodes, lambda x: x in end_nodes)
        for start in start_nodes
    ]

    return math.lcm(*lengths)


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_2))
