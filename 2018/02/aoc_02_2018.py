"""Day 2 of Advent of Code 2018"""
from collections import Counter

PART1_TEST = """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"""

PART2_TEST = """
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"""

TEST_CASES = (
    (PART1_TEST, 12, None),
    (PART2_TEST, None, "fgij"),
)


def part1(input_str: str) -> int:
    """Part 1 solution"""

    num_twos = 0
    num_threes = 0
    for line in input_str.splitlines():
        counter = Counter(line)
        for count in counter.values():
            if count == 2:
                num_twos += 1
                break

        for count in counter.values():
            if count == 3:
                num_threes += 1
                break

    return num_twos * num_threes


def part2(input_str: str) -> str:
    """Part 2 solution"""

    lines = input_str.strip().splitlines()

    best_diff = len(lines[0]) + 1
    best_pair: tuple[str, str] = ("", "")

    for i, l1 in enumerate(lines):
        for j, l2 in enumerate(lines):
            if l1 == l2:
                continue

            diff = 0
            for c1, c2 in zip(l1, l2):
                if c1 != c2:
                    diff += 1

                if diff >= best_diff:
                    break

            if diff > 0 and diff < best_diff:
                best_diff = diff
                best_pair = (l1, l2)

    return "".join(c1 for c1, c2 in zip(*best_pair) if c1 == c2)


if __name__ == "__main__":
    print(part2(PART2_TEST))
