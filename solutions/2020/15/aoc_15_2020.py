"""Day 15: Rambunctious Recitation"""
from aoc.solution import Solution

TEST_DATA = """
0,3,6
""".strip()


def play_game(number_of_turns: int, initial_numbers: list[int]) -> int:
    """Play the game"""
    last_time_said: dict[int, int] = dict()
    second_to_last_time_said: dict[int, int] = dict()

    for turn in range(number_of_turns):

        # if initial number, say it
        if turn < len(initial_numbers):
            num = initial_numbers[turn]

        # if not heard before, say 0
        elif num not in second_to_last_time_said:
            num = 0

        # say the difference between most recent and second most recent
        # turn it was heard
        else:
            num = last_time_said[num] - second_to_last_time_said[num]

        # if heard it once before, remember it
        if num in last_time_said:
            second_to_last_time_said[num] = last_time_said[num]

        # we just head it
        last_time_said[num] = turn

    return num


class Day15(Solution):
    """Solution to day 15 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 15, "Rambunctious Recitation")

    def _part_one(self) -> int:
        """What will be the 2020th number spoken?"""
        return play_game(2020, self.data)

    def _part_two(self) -> int:
        """Given your starting numbers, what will be the 30000000th number spoken?"""
        return play_game(30_000_000, self.data)

    def _get_data(self) -> list[str]:
        return self.input.as_list(lambda line: [int(x) for x in line.split(",")])[0]


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day15()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 436
    assert solution.part_two() == 175594


if __name__ == "__main__":
    test_solution(TEST_DATA)
