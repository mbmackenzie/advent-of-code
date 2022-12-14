"""Day 13 of Advent of Code 2022"""
from __future__ import annotations

import re
from functools import cmp_to_key
from math import prod
from typing import Iterator
from typing import Literal
from typing import overload
from typing import Union

TEST_DATA = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

TEST_CASES = ((TEST_DATA, 13, 140),)

Packet = list[Union[int, list[int], "Packet"]]
PacketItem = Union[int, list[int], Packet]

INPUT_CHECK = re.compile(r"^[\[\]\,\d\s]+$")
TOKENS = re.compile(r"(\[|\]|\d+)")


def parse_nested_list(packet_str: str) -> Packet:

    if not INPUT_CHECK.match(packet_str):
        raise ValueError("Illegal input!")

    current: Packet = []
    stack: list[Packet] = [current]

    for token in TOKENS.findall(packet_str[1:-1]):

        if token in "[]":
            if token == "[":
                stack.append([])

            elif token == "]":
                stack.pop()
                stack[-1].append(current)

            current = stack[-1]
            continue

        current.append(int(token))

    return stack[0]


def in_correct_order(left: Packet | PacketItem, right: Packet | PacketItem) -> int:

    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0

        return -1 if left < right else 1

    if isinstance(left, list) and isinstance(right, list):
        for left_item, right_item in zip(left, right):
            order_check = in_correct_order(left_item, right_item)
            if order_check != 0:
                return order_check

        return in_correct_order(len(left), len(right))

    return in_correct_order(
        [left] if isinstance(left, int) else left,
        [right] if isinstance(right, int) else right,
    )


@overload
def get_packets(input_str: str, pairs: Literal[True]) -> Iterator[tuple[Packet, Packet]]:
    ...


@overload
def get_packets(input_str: str, pairs: Literal[False]) -> Iterator[Packet]:
    ...


def get_packets(input_str: str, pairs: bool = True) -> Iterator[Packet | tuple[Packet, Packet]]:
    """Get packets from input string"""

    to_yield: list[Packet] = []
    for line in input_str.split("\n"):
        if not line.strip():
            continue

        to_yield.append(parse_nested_list(line.strip()))

        if not pairs:
            yield to_yield.pop()

        if len(to_yield) == 2:
            yield (to_yield[0], to_yield[1])
            to_yield = []


def part1(input_str: str) -> int:
    """Part 1 solution"""

    pairs = get_packets(input_str, pairs=True)
    return sum(i for i, pair in enumerate(pairs, 1) if in_correct_order(*pair) <= 0)


def part2(input_str: str) -> int:
    """Part 2 solution"""

    dividers: list[Packet] = [[[2]], [[6]]]
    all_packets: list[Packet] = [*dividers, *get_packets(input_str, pairs=False)]

    all_packets.sort(key=cmp_to_key(in_correct_order))
    return prod(map(lambda x: x + 1, map(all_packets.index, dividers)))


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
