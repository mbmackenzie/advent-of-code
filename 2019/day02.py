"""Day 2 of Advent of Code 2019"""
from tools.parsing import comma_separated_ints

TEST_CASES = (
    ("1,0,0,0,99", 2, None),
    ("2,3,0,3,99", 2, None),
    ("2,4,4,5,99,0", 2, None),
    ("1,1,1,4,99,5,6,0,99", 30, None),
)


@comma_separated_ints
def part1(data: list[int], testing: bool = False) -> int:
    """Part 1 solution"""

    if testing is False:
        data[1] = 12
        data[2] = 2

    for i in range(0, len(data), 4):
        d = data[i]
        if d == 1:
            data[data[i + 3]] = data[data[i + 1]] + data[data[i + 2]]
        elif d == 2:
            data[data[i + 3]] = data[data[i + 1]] * data[data[i + 2]]
        elif d == 99:
            break

    return data[0]


def part2(input_str: str, testing: bool = False) -> int:
    """Part 2 solution"""
    raise NotImplementedError
