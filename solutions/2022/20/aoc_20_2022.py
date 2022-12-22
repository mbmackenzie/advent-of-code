"""Day 20 of Advent of Code 2022"""
from collections import deque


TEST_DATA = """\
1
2
-3
3
-2
0
4
"""

TEST_CASES = ((TEST_DATA, 3, 1623178306),)


def rotate_to_index(message: deque[tuple[int, int]], index: int) -> None:
    """Rotate the deque to the given index"""

    while True:

        deque_index, _ = message[0]
        if deque_index == index:
            return

        message.rotate(-1)


def rotate_to_value(message: deque[tuple[int, int]], value: int) -> None:
    """Rotate the deque to the given value"""

    while True:

        _, deque_value = message[0]
        if deque_value == value:
            return

        message.rotate(-1)


def perform_mixing(og_message: list[tuple[int, int]], message: deque[tuple[int, int]]) -> None:
    """Perform the mixing"""

    for index, value in og_message:
        rotate_to_index(message, index)
        message.popleft()
        message.rotate(-1 * value)
        message.appendleft((index, value))


def calc_grove_sum(message: deque[tuple[int, int]]) -> int:
    """Calculate the sum of the values in the grove"""

    grove_sum = 0
    for grove_index in (1000, 2000, 3000):
        grove_sum += message[grove_index % len(message)][1]

    return grove_sum


def part1(input_str: str) -> int:
    """Part 1 solution"""

    og_message = [(i, int(line)) for i, line in enumerate(input_str.splitlines())]
    message = deque(og_message)

    perform_mixing(og_message, message)
    rotate_to_value(message, 0)
    return calc_grove_sum(message)


def part2(input_str: str) -> int:
    """Part 2 solution"""

    DECRYPTION_KEY = 811589153

    input_ints = [int(line) for line in input_str.splitlines()]
    og_message = [(i, value * DECRYPTION_KEY) for i, value in enumerate(input_ints)]

    message = deque(og_message)

    for _ in range(10):
        perform_mixing(og_message, message)

    rotate_to_value(message, 0)
    return calc_grove_sum(message)


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
