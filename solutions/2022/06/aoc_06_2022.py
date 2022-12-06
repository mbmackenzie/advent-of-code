"""Day 6 of Advent of Code 2022"""

TEST_CASES = (
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
)


def get_first_non_repeating_set_idx(input_str: str, window: int) -> int:
    for i in range(window, len(input_str)):
        if len(set(input_str[i - window : i])) == window:
            return i

    raise ValueError("No non-repeating set found")


def part1(input_str: str) -> int:
    """Part 1 solution"""
    return get_first_non_repeating_set_idx(input_str, 4)


def part2(input_str: str) -> int:
    """Part 2 solution"""
    return get_first_non_repeating_set_idx(input_str, 14)


if __name__ == "__main__":
    print(part1(TEST_CASES[0][0]))
    print(part2(TEST_CASES[0][0]))
    pass
