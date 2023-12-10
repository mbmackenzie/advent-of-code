"""Day 9 of Advent of Code 2023"""

from typing import Iterator


TEST_DATA = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

TEST_CASES = ((TEST_DATA, None, None),)


def iter_numbers(input_str: str, reverse: bool = False) -> Iterator[list[int]]:
    """Iterate over the numbers in the input"""

    for line in input_str.splitlines():
        if reverse:
            yield list(reversed([int(i) for i in line.split()]))
        else:
            yield [int(i) for i in line.split()]


def find_next_number(numbers: list[int]) -> int:
    all_diffs: list[list[int]] = [numbers]
    step = 1

    while True:
        diffs = all_diffs[step - 1]
        diffs = [i - j for i, j in zip(diffs[1:], diffs[:-1])]
        all_diffs.append(diffs)

        if all(d == 0 for d in diffs):
            break

        step += 1

    d = 0
    for diff in reversed(all_diffs):
        diff.append(diff[-1] + d)
        d = diff[-1]

    return all_diffs[0][-1]


def part1(input_str: str) -> int:
    """Part 1 solution"""
    return sum(find_next_number(numbers) for numbers in iter_numbers(input_str))


def part2(input_str: str) -> int:
    """Part 2 solution"""
    return sum(find_next_number(numbers) for numbers in iter_numbers(input_str, True))


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
