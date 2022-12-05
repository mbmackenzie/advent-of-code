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

    def check_pair(pair: str) -> bool:
        elf1, elf2 = map(get_range, pair.split(","))
        return set(elf1).issubset(elf2) or set(elf2).issubset(elf1)

    return sum(map(check_pair, data))


@split_lines
def part2(data: list[str]) -> int:
    """Part 2 solution"""

    def check_pair(pair: str) -> bool:
        elf1, elf2 = map(get_range, pair.split(","))
        return bool(set(elf1) & set(elf2))

    return sum(map(check_pair, data))


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
