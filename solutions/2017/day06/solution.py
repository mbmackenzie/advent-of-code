import pathlib
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def stringify(x: list[int]):
    return "|".join(str(v) for v in x)


def part1(input_str: str) -> int:
    numbers = [int(c.strip()) for c in input_str.split()]

    states = set()

    steps = 0
    while stringify(numbers) not in states:
        states.add(stringify(numbers))

        if steps >= 1_000_000:
            print("STEP OVERFLOW")
            raise StopIteration()

        states.add(stringify(numbers))

        m = max(numbers)
        idxmax = numbers.index(m)

        i = (idxmax + 1) % len(numbers)
        numbers[idxmax] = 0

        for _ in range(m):
            numbers[i] += 1
            i = (i + 1) % len(numbers)

        steps += 1
    return steps


def part2(input_str: str) -> int:
    numbers = [int(c.strip()) for c in input_str.split()]

    states = {}

    steps = 0
    num_string = stringify(numbers)

    while num_string not in states:
        states[num_string] = steps

        if steps >= 1_000_000:
            print("STEP OVERFLOW")
            raise StopIteration()

        m = max(numbers)
        idxmax = numbers.index(m)

        i = (idxmax + 1) % len(numbers)
        numbers[idxmax] = 0

        for _ in range(m):
            numbers[i] += 1
            i = (i + 1) % len(numbers)

        steps += 1
        num_string = stringify(numbers)

    prev_found = states[num_string]

    return steps - prev_found


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
0   2   7   0
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 5),
    ],
    [
        (TEST_DATA, 4),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
