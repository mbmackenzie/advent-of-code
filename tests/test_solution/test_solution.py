from aoc import Solution
from testing.mixins import BlankSolutionPartMixin


class Solution1(BlankSolutionPartMixin, Solution):
    def __init__(self):
        super().__init__(2021, 0, "Testing Testing")


class Solution2(BlankSolutionPartMixin, Solution):
    def __init__(self):
        super().__init__(2021, 0, "")


def test_solution_str_with_name() -> None:
    s = Solution1()
    assert str(s) == "Day 0, 2021 - Testing Testing"


def test_solution_str_with_no_name() -> None:
    s = Solution2()
    assert str(s) == "Day 0, 2021"
