"""Day 2: Dive!"""
from typing import NamedTuple

from aoc.solution import Solution


TEST_DATA = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".strip()


class Command(NamedTuple):
    value: int
    forward: bool = False


def execute_commands(commands: list[Command], use_aim: bool = False) -> tuple[int, int]:
    hpos = depth = 0

    if use_aim:
        aim = 0

    for command in commands:
        if command.forward:
            hpos += command.value
            if use_aim:
                depth += command.value * aim
        else:
            if use_aim:
                aim += command.value
            else:
                depth += command.value

    return hpos, depth


class Day02(Solution):
    """Solution to day 2 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 2, "Dive!")

    def _part_one(self) -> int:
        """TODO"""
        hpos, depth = execute_commands(self.data)
        return hpos * depth

    def _part_two(self) -> int:
        """TODO"""
        hpos, depth = execute_commands(self.data, use_aim=True)
        return hpos * depth

    def _get_data(self) -> list[Command]:
        def get_command(input: str) -> Command:
            unit, value = input.split(" ")
            if unit == "up":
                return Command(-int(value))
            elif unit == "down":
                return Command(int(value))
            else:
                return Command(int(value), forward=True)

        return self.input.as_list(get_command)


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day02()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 150
    assert solution.part_two() == 900


if __name__ == "__main__":
    test_solution(TEST_DATA)
