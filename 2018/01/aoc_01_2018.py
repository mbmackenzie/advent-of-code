"""Day 1 of Advent of Code 2018"""
from collections import defaultdict

from tools.parsing import line_separated_ints


_TEST_CASES = (
    ("+1, +1, +1", 3, None),
    ("+1, +1, -2", 0, None),
    ("-1, -2, -3", -6, None),
    ("+1, -1", None, 0),
    ("+3, +3, +4, -2, -4", None, 10),
    ("-6, +3, +8, +5, -6", None, 5),
    ("+7, +7, -2, -7, -4", None, 14),
)

TEST_CASES = tuple((i.replace(", ", "\n"), *j) for i, *j in _TEST_CASES)


@line_separated_ints
def part1(data: list[int]) -> int:
    """Part 1 solution"""
    return sum(data)


@line_separated_ints
def part2(data: list[int]) -> int:
    """Part 2 solution"""

    counter: dict[int, int] = defaultdict(int)

    tot, i = 0, 0

    while True:

        counter[tot] += 1

        if counter[tot] == 2:
            return tot

        tot += data[i % len(data)]
        i += 1
