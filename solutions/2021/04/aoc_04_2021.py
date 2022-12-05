"""Day 4"""
import re

from aoc.reformaters import combine_nonblank_lines
from aoc.solution import Solution

TEST_DATA = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
 """.strip()


Grid = list[list[int]]


class Board:
    """A bingo board"""

    def __init__(self, values: list[int], size: int = 5):
        self.values = values
        self.size = size
        self.marked: list[int] = []

    @property
    def winning(self) -> bool:
        grid, gridT = self._make_grids()
        return self._check_grid(grid) or self._check_grid(gridT)

    @property
    def unmarked(self) -> list[int]:
        return [v for v in self.values if v not in self.marked]

    def check_num(self, value: int) -> None:
        if value in self.values:
            self.marked.append(value)

    def _check_grid(self, grid: Grid) -> bool:
        return any([sum(row) == self.size for row in grid])

    def _make_grids(self) -> tuple[Grid, Grid]:
        grid = [[0] * self.size for _ in range(self.size)]
        gridT = [[0] * self.size for _ in range(self.size)]

        for i, v in enumerate(self.values):
            row, col = divmod(i, self.size)

            if v in self.marked:
                grid[row][col] = 1
                gridT[col][row] = 1

        return grid, gridT


class Day04(Solution):
    """Solution to day 4 of the 2021 Advent of Code"""

    pulls: list[int]

    def __init__(self) -> None:
        super().__init__(2021, 4, "")

    def _part_one(self) -> int:
        """What will your final score be if you choose that board?"""
        for pull in self.pulls:
            for board in self.data:
                board.check_num(pull)

                if board.winning:
                    unmarked_sum = sum(board.unmarked)
                    return pull * unmarked_sum

        return -1

    def _part_two(self) -> int:
        """Once it wins, what would its final score be?"""
        winning_boards: set[int] = set()
        for pull in self.pulls:
            for i, board in enumerate(self.data):
                if i in winning_boards:
                    continue

                board.check_num(pull)

                if board.winning:
                    if len(winning_boards) == len(self.data) - 1:
                        return pull * sum(board.unmarked)

                    winning_boards.add(i)

        return -1

    def _pop_lines(self) -> None:
        self.pulls = list(map(int, self.input.pop_line().split(",")))

    def _get_data(self) -> list[Board]:
        def parse_board(input: str) -> Board:
            return Board(list(map(int, re.split(r"\s+", input))))

        return self.input.as_list(parse_board)

    def _reformat_data(self) -> None:
        self.input.reformat(combine_nonblank_lines)


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day04()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 4512
    assert solution.part_two() == 1924


if __name__ == "__main__":
    test_solution(TEST_DATA)
