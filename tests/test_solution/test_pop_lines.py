from aoc import Solution
from testing.mixins import BlankSolutionPartMixin


class Solution1(BlankSolutionPartMixin, Solution):
    first_line: str

    def __init__(self) -> None:
        super().__init__(0, 0, "")

    def _pop_lines(self) -> None:
        self.first_line = self.input.pop_line()


class Solution2(BlankSolutionPartMixin, Solution):
    first_line: str

    def __init__(self) -> None:
        super().__init__(0, 0, "")

    def _pop_lines(self) -> None:
        self.first_line = self.input.pop_line()

    def _reformat_data(self) -> None:
        def reformatter(content: list[str]) -> list[str]:
            return ["".join(content)]

        self.input.reformat(reformatter)  # type: ignore


class Solution3(BlankSolutionPartMixin, Solution):
    pops: list[str] = []

    def __init__(self) -> None:
        super().__init__(0, 0, "")

    def _pop_lines(self) -> None:
        self.pops.append(self.input.pop_line())
        self.pops.append(self.input.pop_line())


def test_pop_lines() -> None:
    data = ["A", "B", "C", "D"]
    s = Solution1()
    s.set_input_data(data)

    assert s.first_line == "A"
    assert s.input.content == ["B", "C", "D"]


def test_pop_lines_with_reformat() -> None:
    data = ["A", "B", "C", "D"]
    s = Solution2()
    s.set_input_data(data)

    assert s.first_line == "A"
    assert s.input.content == ["BCD"]


def test_pop_lines_removes_empty_lines() -> None:
    data = ["A", "", "B", "C", "D"]
    s = Solution1()
    s.set_input_data(data)

    assert s.first_line == "A"
    assert s.input.content == ["B", "C", "D"]


def test_multi_pop_lines() -> None:
    data = ["A", "B", "C", "D"]
    s = Solution3()
    s.set_input_data(data)

    assert s.pops == ["A", "B"]
    assert s.input.content == ["C", "D"]
