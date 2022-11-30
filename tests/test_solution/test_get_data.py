from aoc import Solution
from testing.mixins import BlankSolutionPartMixin


class Solution1(BlankSolutionPartMixin, Solution):
    def __init__(self) -> None:
        super().__init__(0, 0, "")

    def _get_data(self) -> list[str]:
        return self.input.as_list()


class Solution2(BlankSolutionPartMixin, Solution):
    def __init__(self) -> None:
        super().__init__(0, 0, "")

    def _get_data(self) -> list[str]:
        return self.input.as_list(mutate=int)


class Solution3(BlankSolutionPartMixin, Solution):
    def __init__(self) -> None:
        super().__init__(0, 0, "")

    def _get_data(self) -> list[int]:
        return self.input.as_list(int)

    def _get_data_for_part_one(self) -> list[int]:
        data = self.input.as_list(int)
        return [d + 1 for d in data]

    def _get_data_for_part_two(self) -> list[int]:
        data = self.input.as_list(int)
        return [d + 2 for d in data]


def test_get_data_is_default() -> None:
    data = "a b c d e f".split()
    expected = ["a", "b", "c", "d", "e", "f"]

    s = Solution1()
    s.set_input_data(data)

    got_data = s._get_data()
    assert got_data == expected
    assert s._get_data_for_part_one() == got_data
    assert s._get_data_for_part_two() == got_data


def test_get_data_is_default_with_mutation() -> None:
    data = "1 2 3 4 5 6".split()
    expected = [1, 2, 3, 4, 5, 6]

    s = Solution2()
    s.set_input_data(data)

    got_data = s._get_data()
    assert got_data == expected
    assert s._get_data_for_part_one() == got_data
    assert s._get_data_for_part_two() == got_data


def test_part_data_getters_are_used() -> None:
    data = "1 2 3 4 5".split()
    expected1 = [2, 3, 4, 5, 6]
    expected2 = [3, 4, 5, 6, 7]

    s = Solution3()
    s.set_input_data(data)

    assert s._get_data_for_part_one() == expected1
    assert s._get_data_for_part_two() == expected2
