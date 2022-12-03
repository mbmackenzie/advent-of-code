"""Day 1: Sonar Sweep"""
from aoc.solution import Solution


TEST_DATA = """
199
200
208
210
200
207
240
269
260
263
""".strip()


def get_num_increases(data: list[int]) -> int:
    """
    Get the total number of times the value of the next element
    in the list is greater than the value of the previous element

    >>> get_num_increases([1, 3, 4, 2, 5])
    3
    """
    return sum(b > a for a, b in zip(data[:-1], data[1:]))


class Day01(Solution):
    """Solution to day 1 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 1, "Sonar Sweep")

    def _part_one(self) -> int:
        """How many measurements are larger than the previous measurement?"""
        return get_num_increases(self.data)

    def _part_two(self) -> int:
        """
        How many increases if you use the sum of windows of three
        consecutive measurements?
        """
        windows = zip(self.data[:-2], self.data[1:-1], self.data[2:])
        return get_num_increases([sum(w) for w in windows])

    def _get_data(self) -> list[int]:
        return self.input.as_list(int)


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day01()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 7
    assert solution.part_two() == 5


if __name__ == "__main__":
    test_solution(TEST_DATA)
