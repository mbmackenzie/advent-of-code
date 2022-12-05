"""Day 3 of Advent of Code 2022"""
from tools.parsing import split_lines

TEST_DATA = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

TEST_CASES = ((TEST_DATA, 2, 4),)


def get_range(s: str) -> range:
    """Return a range from a string"""
    start, end = s.split("-")
    return range(int(start), int(end) + 1)


@split_lines
def part1(data: list[str]) -> int:
    """Part 1 solution"""

    tot = 0
    for pair in data:
        elf1, elf2 = pair.split(",")

        if set(get_range(elf1)) <= set(get_range(elf2)) or set(get_range(elf2)) <= set(
            get_range(elf1),
        ):
            tot += 1

    return tot


@split_lines
def part2(data: list[str]) -> int:
    """Part 2 solution"""
    tot = 0
    for pair in data:
        elf1, elf2 = pair.split(",")

        if set(get_range(elf1)) & set(get_range(elf2)):
            tot += 1

    return tot


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
