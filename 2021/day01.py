"""Advent of Code 2021, Day 01"""
from typing import Iterable
from typing import Sequence


TEST_DATA = "199 200 208 210 200 207 240 269 260 263"
TEST_CASES = [(TEST_DATA, 7, 5)]


def parse_input(input_str: str) -> Sequence[int]:
    """Parse the input data into a list of integers"""
    return list(map(int, input_str.split()))


def get_num_increases(data: Sequence[int]) -> int:
    """
    Get the total number of times the value of the next element
    in the list is greater than the value of the previous element

    Examples
    --------
    >>> get_num_increases([1, 3, 4, 2, 5])
    3
    """
    return sum(b > a for a, b in zip(data[:-1], data[1:]))


def create_windows(data: Sequence[int], window_size: int) -> Iterable[Sequence[int]]:
    """
    Create a tuple of windows of a given size

    Examples
    --------
    >>> list(create_windows([1, 2, 3, 4, 5], 3))
    [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    """
    return zip(*(data[i:] for i in range(window_size)), strict=False)


def part1(input_str: str) -> int:
    """How many measurements are larger than the previous measurement?"""
    return get_num_increases(parse_input(input_str))


def part2(input_str: str) -> int:
    """How many increases if you use the sum of windows of three
    consecutive measurements?
    """
    windows = create_windows(parse_input(input_str), 3)
    window_sums = [sum(window) for window in windows]
    return get_num_increases(window_sums)
