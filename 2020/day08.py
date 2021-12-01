"""Day 8"""
from aoc import Solution


def run_program(program: list[tuple[str, int]], init_value: int = 0) -> tuple[int, int]:
    accumulator = init_value
    visited = [0] * len(program)

    i = 0
    while True:

        if i >= len(program) or visited[i] == 1:
            break

        visited[i] = 1
        command, value = program[i]

        if command == "jmp":
            i += value
            continue

        if command == "acc":
            accumulator += value

        i += 1

    return i, accumulator


class Day08(Solution):
    """Solution to day 8 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 8, "")

    def _part_one(self) -> int:
        """What is the final value in the accumulator?"""
        _, accumulator = run_program(self.data)
        return accumulator

    def _part_two(self) -> int:
        """What is the final value in the accumulator after fixing the program"""
        for i, (command, value) in enumerate(self.data):
            fixed_program = self.data.copy()

            if command == "nop":
                fixed_program[i] = ("jmp", value)
            elif command == "jmp":
                fixed_program[i] = ("nop", value)

            last_idx, accumulator = run_program(fixed_program)

            if last_idx == len(fixed_program):
                break

        return accumulator

    def _get_data(self) -> list[tuple[str, int]]:
        def parse_command(command: str) -> tuple[str, int]:
            """Parse a command"""
            command_list = command.split(" ")
            return command_list[0], int(command_list[1])

        return self.input.as_list(parse_command)
