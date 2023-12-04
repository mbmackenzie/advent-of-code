"""Day 1 of Advent of Code 2023"""

P1_TEST_DATA = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

P2_TEST_DATA = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

TEST_CASES = (
    (P1_TEST_DATA, 142, None),
    (P2_TEST_DATA, None, 281),
)

num_strings = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part1(input_str: str) -> int:
    """Part 1 solution"""

    cal_values = []

    for line in input_str.splitlines():
        nums = [c for c in line if c.isdigit()]

        cal_values.append(int(f"{nums[0]}{nums[-1]}"))

    return sum(cal_values)


def part2(input_str: str) -> int:
    """Part 2 solution"""
    cal_values = []

    for line in input_str.splitlines():
        nums = []

        for i in range(len(line)):
            if line[i].isdigit():
                nums.append(line[i])

            for key in num_strings:
                if line[i:].startswith(key):
                    nums.append(num_strings[key])

        cal_values.append(int(f"{nums[0]}{nums[-1]}"))

    return sum(cal_values)


if __name__ == "__main__":
    print(part1(P1_TEST_DATA))
    print(part2(P2_TEST_DATA))
