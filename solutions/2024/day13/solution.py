import pathlib
import re
from typing import Iterator
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases

XY = tuple[int, int]


button_regex = re.compile(r"^Button [AB]: X\+(\d+), Y\+(\d+)$")
prize_regex = re.compile(r"^Prize: X=(\d+), Y=(\d+)$")


def parse(input_str: str) -> Iterator[tuple[XY, XY, XY]]:
    for group in input_str.split("\n\n"):
        lines = group.split("\n")
        a = tuple(int(x) for x in button_regex.match(lines[0]).groups())
        b = tuple(int(x) for x in button_regex.match(lines[1]).groups())
        target = tuple(int(x) for x in prize_regex.match(lines[2]).groups())
        yield (a, b, target)


def part1(input_str: str) -> int:
    cost = 0
    for (x1, y1), (x2, y2), (X, Y) in parse(input_str):
        b = (Y * x1 - X * y1) / (y2 * x1 - x2 * y1)
        a = (X - b * x2) / x1

        if int(a) == a and int(b) == b:
            cost += int(3 * a + b)

    return cost


def part2(input_str: str) -> int:
    ADD = 10000000000000

    cost = 0
    for (x1, y1), (x2, y2), (X, Y) in parse(input_str):
        X = X + ADD
        Y = Y + ADD

        b = (Y * x1 - X * y1) / (y2 * x1 - x2 * y1)
        a = (X - b * x2) / x1

        if int(a) == a and int(b) == b:
            cost += int(3 * a + b)

    return cost


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 480),
    ],
    [
        (TEST_DATA, 875318608908),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
