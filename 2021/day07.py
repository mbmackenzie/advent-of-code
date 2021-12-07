"""Day 7: The Treachery of Whales"""
import statistics

from aoc.solution import Solution

TEST_DATA = """
16,1,2,0,4,2,7,1,2,14
""".strip()


class Day07(Solution):
    """Solution to day 7 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 7, "The Treachery of Whales")

    def _part_one(self) -> int:
        """How much fuel must they spend to align to that position?"""
        median_h = int(statistics.median(self.data))
        return sum(abs(h - median_h) for h in self.data)

    def _part_two(self) -> int:
        """How much fuel must they spend to align to that position?"""

        def total_fuel(moves: int) -> int:
            return sum(i for i in range(1, moves + 1))

        mean_h = int(statistics.mean(self.data))

        return min(
            sum(total_fuel(abs(h - mean_h)) for h in self.data),
            sum(total_fuel(abs(h - (mean_h + 1))) for h in self.data),
        )

    def _get_data(self) -> list[int]:
        data = self.input.as_list()
        return [int(d) for d in data[0].split(",")]


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day07()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 37
    assert solution.part_two() == 168


if __name__ == "__main__":
    test_solution(TEST_DATA)
