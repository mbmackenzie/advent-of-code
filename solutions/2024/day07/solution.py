import pathlib
from itertools import product
from typing import Iterator
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def parse(input_str: str) -> Iterator[tuple[int, list[int]]]:
    for line in input_str.splitlines():
        res, nums = line.split(": ")
        yield int(res.strip()), [int(n) for n in nums.strip().split()]


def brute1(res: int, nums: list[int]) -> bool:
    OPERATORS = "*+"

    num_to_choose = len(nums) - 1
    for operators in product(OPERATORS, repeat=num_to_choose):
        left = nums[0]
        for i in range(len(operators)):
            right = nums[i + 1]
            op = operators[i]

            if op == "*":
                left *= right

            if op == "+":
                left += right

        if left == res:
            return res

    return 0


def part1(input_str: str) -> int:
    return sum(brute1(*parsed) for parsed in parse(input_str))


def brute2(res: int, nums: list[int]) -> bool:
    OPERATORS = "*+|"

    num_to_choose = len(nums) - 1
    for operators in product(OPERATORS, repeat=num_to_choose):
        left = nums[0]
        for i in range(len(operators)):
            right = nums[i + 1]
            op = operators[i]

            if op == "*":
                left *= right

            if op == "+":
                left += right

            if op == "|":
                left = int(f"{left}{right}")

        if left == res:
            return res

    return 0


def part2(input_str: str) -> int:
    return sum(brute2(*parsed) for parsed in parse(input_str))


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


TEST_CASES: TestCases = (
    [
        (TEST_DATA, 3749),
    ],
    [
        (TEST_DATA, 11387),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
