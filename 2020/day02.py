"""Day 2"""
from aoc import Solution


def parse_password(data: str) -> tuple[int, int, str, str]:
    """Parse the input data into a tuple of (num1, num2, letter, password)"""
    nums, letter, password = data.split()
    nums_list = nums.split("-")
    return int(nums_list[0]), int(nums_list[1]), letter[:-1], password


class Day02(Solution):
    """Solution to day 2 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 2, "")

    def _part_one(self) -> int:
        """Checks how many passwords have between min and max occurences of a letter"""

        def check_password(min: int, max: int, letter: str, password: str) -> bool:
            """Check if the password meets the criteria"""
            return min <= password.count(letter) <= max

        return sum(check_password(*password) for password in self.data)

    def _part_two(self) -> int:
        """Checks how many passwords have letter at idx1 XOR idx2"""

        def check_password(idx1: int, idx2: int, letter: str, password: str) -> bool:
            """Check if the password meets the criteria"""
            return (password[idx1 - 1] == letter) ^ (password[idx2 - 1] == letter)

        return sum(check_password(*password) for password in self.data)

    def _get_data(self) -> list[tuple[int, int, str, str]]:
        return self.input.as_list(mutate=parse_password)
