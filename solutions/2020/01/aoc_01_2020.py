"""Day 01: Report Repair"""
from functools import reduce
from itertools import combinations

from aoc import Solution


TEST_DATA = """
1721
979
366
299
675
1456
""".strip()


def generic_solution(data: list[int], n_terms: int, target_sum: int) -> int:
    """
    Find the n_terms numbers in data that add to target_sum. return their product

    Returns -1 if no valid combination is found
    """
    combinations_list = list(combinations(data, n_terms))
    for combination in combinations_list:
        if sum(combination) == target_sum:
            return reduce(lambda x, y: x * y, combination)

    return -1


class Day01(Solution):
    """Solution to day one of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 1, "Report Repair")

    def _part_one(self) -> int:
        """Find two numbers in data that add to 2020 and return their product"""
        return generic_solution(self.data, 2, 2020)

    def _part_two(self) -> int:
        """Find three numbers in data that add to 2020 and return their product"""
        return generic_solution(self.data, 3, 2020)

    def _get_data(self) -> list[int]:
        """Read the data from the file"""
        return self.input.as_list(int)


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day01()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 514579
    assert solution.part_two() == 241861950


if __name__ == "__main__":
    test_solution(TEST_DATA)
