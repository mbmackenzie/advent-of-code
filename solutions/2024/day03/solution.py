import pathlib
import re
from typing import Iterator
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


regex = re.compile(r"mul\((\d+),(\d+)\)")


def part1(input_str: str) -> int:
    findall = regex.findall(input_str)
    return sum(int(a) * int(b) for a, b in findall)


# def part2(input_str: str) -> int:
#     """
#     Benchmark with `hyperfine` ::
#
#         Time (mean ± σ):     588.0 ms ±  18.4 ms    [User: 520.6 ms, System: 54.4 ms]
#         Range (min … max):   570.7 ms … 627.3 ms    10 runs
#     """
#     matches = regex.findall(input_str)
#     starts = [input_str.index(f"mul({a},{b})") for a, b in matches]

#     tot = 0
#     on = True
#     for i in range(len(input_str)):
#         curr = input_str[i:]
#         if curr.startswith("don't()"):
#             on = False

#         if curr.startswith("do()"):
#             on = True

#         for s in starts:
#             if i == s and on:
#                 tot += int(matches[starts.index(s)][0]) * int(matches[starts.index(s)][1])

#     return tot


do_dont_regex = re.compile(r"do\(\)|don't\(\)")


def get_products(input_str: str) -> Iterator[tuple[str, int, int]]:
    for m in regex.finditer(input_str):
        a = int(m.group(1))
        b = int(m.group(2))
        yield "product", m.start(), a * b


def get_toggles(input_str: str) -> Iterator[tuple[str, int, bool]]:
    for m in do_dont_regex.finditer(input_str):
        yield "toggle", m.start(), m.group() == "do()"


def part2(input_str: str) -> int:
    """
    Benchmark with `hyperfine` ::

        Time (mean ± σ):     369.3 ms ±  15.9 ms    [User: 300.4 ms, System: 59.0 ms]
        Range (min … max):   341.5 ms … 396.0 ms    10 runs
    """
    products = list(get_products(input_str))
    toggles = list(get_toggles(input_str))

    total = 0
    toggle = True

    for kind, _, val in sorted(products + toggles, key=lambda x: x[1]):
        if kind == "toggle":
            toggle = val
        elif toggle:
            total += val

    return total


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

TEST_DATA2 = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 161),
    ],
    [
        (TEST_DATA2, 48),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
