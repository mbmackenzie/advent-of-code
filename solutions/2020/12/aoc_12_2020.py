"""Day 12: Rain Risk"""
from aoc import Solution


class Day12(Solution):
    """Solution to day 12 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 12, "Rain Risk")

    def _part_one(self) -> int:
        """Find the final position of the boat"""
        facing = "E"
        position = [0, 0]  # [east/west, north/south]

        def get_position_update(direction: str, value: int) -> list[int]:
            idx = {"E": 0, "W": 0, "N": 1, "S": 1}[direction]
            const = {"E": 1, "W": -1, "N": 1, "S": -1}[direction]

            update = [0, 0]
            update[idx] += const * value

            return update

        def get_new_direction(direction: str, turn: str, amount: int) -> str:
            directions = ["N", "E", "S", "W"]
            current_idx = directions.index(direction)
            turn_const = {"R": 1, "L": -1}[turn]

            new_idx = (current_idx + (turn_const * amount // 90)) % 4

            try:
                return directions[new_idx]
            except IndexError:
                print(direction, turn, amount, new_idx)
                raise IndexError

        for command, value in self.data:
            if command in ("L", "R"):
                facing = get_new_direction(facing, command, value)
                continue

            direction = facing if command == "F" else command
            position_update = get_position_update(direction, value)
            position[0] += position_update[0]
            position[1] += position_update[1]

        return sum(map(abs, position))  # type: ignore

    def _part_two(self) -> int:
        """TODO"""
        return NotImplemented

    def _get_data(self) -> list[tuple[str, int]]:
        def parse(input: str) -> tuple[str, int]:
            return input[0], int(input[1:])

        return self.input.as_list(parse)
