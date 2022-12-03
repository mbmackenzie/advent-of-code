"""Day 6: Lanternfish"""
from aoc.solution import Solution

TEST_DATA = """
3,4,3,1,2
""".strip()


def find_population(initial_fish: list[int], max_days: int = 80) -> int:
    lifetimes = {i: 0 for i in range(9)}
    for fish in initial_fish:
        lifetimes[fish] += 1

    for _ in range(max_days):
        ready_to_spawn = lifetimes[0]
        lifetimes = {i: lifetimes[i + 1] for i in range(8)}
        lifetimes[6] += ready_to_spawn
        lifetimes[8] = ready_to_spawn

    return sum(lifetimes.values())


class Day06(Solution):
    """Solution to day 6 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 6, "Lanternfish")

    def _part_one(self) -> int:
        """How many lanternfish would there be after 80 days?"""
        return find_population(self.data)

    def _part_two(self) -> int:
        """How many lanternfish would there be after 256 days?"""
        return find_population(self.data, max_days=256)

    def _get_data(self) -> list[int]:
        data = self.input.as_list()[0]
        return [int(x) for x in data.split(",")]


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day06()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 5934
    assert solution.part_two() == 26984457539


if __name__ == "__main__":
    test_solution(TEST_DATA)
