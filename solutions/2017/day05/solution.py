import pathlib
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def part1(input_str: str) -> int:
    instructions = [int(c.strip()) for c in input_str.splitlines()]

    steps = 0
    current = 0

    while 0 <= current < len(instructions):
        instruction = instructions[current]
        instructions[current] += 1
        current += instruction

        steps += 1

    return steps


def part2(input_str: str) -> int:
    instructions = [int(c.strip()) for c in input_str.splitlines()]

    steps = 0
    current = 0

    while 0 <= current < len(instructions):
        if steps >= 50_000_000:
            print("LOOP OVERFLOW")
            raise StopIteration()

        instruction = instructions[current]

        if instruction >= 3:
            instructions[current] -= 1
        else:
            instructions[current] += 1

        current += instruction
        steps += 1

        if current >= len(instructions):
            break

    return steps


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
0
3
0
1
-3
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 5),
    ],
    [
        (TEST_DATA, 10),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
