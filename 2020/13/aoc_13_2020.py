"""Day 13"""
import pytest
from aoc.solution import Solution

TEST_DATA = """
939
67,x,7,59,61
""".strip()


def get_first_timestamp(busses: list[int]) -> int:
    """Get the first timestamp"""
    return NotImplemented


def get_best_possible_time(bus_number: int, min_time: int) -> int:
    """Get the best possible time"""
    if min_time % bus_number == 0:
        return min_time
    else:
        return (min_time // bus_number + 1) * bus_number


class Day13(Solution):
    """Solution to day 13 of the 2020 Advent of Code"""

    min_time: int

    def __init__(self) -> None:
        super().__init__(2020, 13, "")

    def _part_one(self) -> int:
        """TODO"""
        busses = [x for x in self.data if x > 0]
        best_times = [get_best_possible_time(bus_number, self.min_time) for bus_number in busses]

        best_time = min(best_times)
        best_bus = busses[best_times.index(best_time)]

        return (best_time - self.min_time) * best_bus

    def _part_two(self) -> int:
        """Return earliest time stamp"""
        return NotImplemented

    def _get_data(self) -> list[int]:
        data = self.input.as_list()
        self.min_time = int(data[0])

        return [int(x) if x != "x" else -1 for x in data[1].split(",")]


def test_solution() -> None:
    """Test the solution"""
    solution = Day13()
    solution.set_input_data(TEST_DATA.split("\n"))

    assert solution.part_one() == 295
    assert solution.part_two() == 1068781


@pytest.mark.parametrize(
    "busses, expected",
    [
        ([17, -1, 13, 19], 3417),
        ([67, 7, 59, 61], 754018),
        ([67, -1, 7, 59, 61], 779210),
        ([67, 7, -1, 59, 61], 1261476),
        ([1789, 37, 47, 1889], 1202161486),
    ],
)
def test_get_first_timestamp(busses: list[int], expected: int) -> None:
    assert get_first_timestamp(busses) == expected


if __name__ == "__main__":
    test_solution()
