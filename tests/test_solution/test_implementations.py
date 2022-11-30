from aoc import Solution


class Solution1(Solution):
    def __init__(self) -> None:
        super().__init__(0, 0, "")

    def _part_one(self) -> int:
        assert self.data == ["a", "b", "c"]
        return 1

    def _part_two(self) -> int:
        assert self.data == ["a", "b", "c"]
        return 1

    def _get_data(self) -> list[str]:
        return ["a", "b", "c"]


class Solution2(Solution):
    def __init__(self) -> None:
        super().__init__(0, 0, "")

    def _part_one(self) -> int:
        assert self.data == ["a", "b", "c"]
        return 1

    def _part_two(self) -> int:
        assert self.data == ["1", "2", "3"]
        return 1

    def _get_data_for_part_one(self) -> list[str]:
        return ["a", "b", "c"]

    def _get_data_for_part_two(self) -> list[str]:
        return ["1", "2", "3"]


def test_part_data_with_get_data() -> None:
    s = Solution1()
    s.set_input_data([""])

    assert s.part_one()
    assert s.part_two()


def test_part_data_with_get_part_data() -> None:
    s = Solution2()
    s.set_input_data([""])

    assert s.part_one()
    assert s.part_two()
