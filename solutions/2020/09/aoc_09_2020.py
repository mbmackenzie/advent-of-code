"""Day 9: Encoding Error"""
from itertools import combinations

from aoc import Solution


def number_is_valid(value: int, previous_values: list[int]) -> bool:
    for term1, term2 in combinations(previous_values, 2):
        if term1 == term2:
            continue

        if term1 + term2 == value:
            return True

    return False


def find_first_invalid_value(values: list[int], preamble_len: int = 25) -> int:
    for i, value in enumerate(values[preamble_len:], preamble_len):
        if not number_is_valid(value, values[i - preamble_len : i]):
            return value

    return -1


def find_contiguous_set(target_sum: int, values: list[int]) -> list[int]:
    """Returns set of at least 2 contiguous values that add to target sum."""
    i = 0
    set_ = []
    sum_ = 0

    while sum_ <= target_sum:

        sum_ += values[i]
        set_.append(values[i])

        if sum_ == target_sum and len(set_) >= 2:
            return set_

        i += 1

    return []


class Day09(Solution):
    """Solution to day 9 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 9, "Encoding Error")

    def _part_one(self) -> int:
        """What is the first invalid value?"""
        return find_first_invalid_value(self.data)

    def _part_two(self) -> int:
        """Find contiguous set numbers (len >= 2) in data that add to first invalid value"""
        first_invalid_value = find_first_invalid_value(self.data)
        for i, _ in enumerate(self.data):
            if contiguous_set := find_contiguous_set(first_invalid_value, self.data[i:]):
                return min(contiguous_set) + max(contiguous_set)

        return -1

    def _get_data(self) -> list[int]:
        return self.input.as_list(int)
