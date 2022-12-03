"""Day 17: Trick Shot"""
import re
from collections import namedtuple

from aoc.solution import Solution


TEST_DATA = """
target area: x=20..30, y=-10..-5
""".strip()

TargetArea = namedtuple("TargetArea", ["x1", "x2", "y1", "y2"])
Velocity = namedtuple("Velocity", ["dx", "dy"])


class Probe:
    max_height: int

    def __init__(self, initial_velocity: Velocity, target_area: TargetArea) -> None:
        self.initial_velocity = initial_velocity
        self.target_area = target_area

        self.reaches_target = self._is_reachable()

    def _is_reachable(self) -> bool:
        x = y = 0
        dx = self.initial_velocity.dx
        dy = self.initial_velocity.dy

        max_height = 0
        while not (
            self.target_area.x1 <= x <= self.target_area.x2
            and self.target_area.y1 <= y <= self.target_area.y2
        ):
            x += dx
            y += dy
            max_height = max(max_height, y)

            dx = max(dx - 1, 0)
            dy -= 1

            if x > self.target_area.x2 or y < self.target_area.y1:
                return False

        self.max_height = max_height
        return True


def get_probes(target_area: TargetArea) -> list[Probe]:
    good_probes: list[Probe] = []

    for x in range(1, target_area.x2 + 1):
        for y in range(target_area.y1, abs(target_area.y1) + 1):
            probe = Probe(Velocity(x, y), target_area)
            if probe.reaches_target:
                good_probes.append(probe)

    return good_probes


class Day17(Solution):
    """Solution to day 17 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 17, "Trick Shot")

    def _part_one(self) -> int:
        """TODO"""
        return max([probe.max_height for probe in get_probes(self.data)])

    def _part_two(self) -> int:
        """TODO"""
        return len(get_probes(self.data))

    def _get_data(self) -> TargetArea:
        ta_str = self.input.as_list()[0]
        ta_re = re.compile(r"(-?\d+)")

        return TargetArea(*map(int, ta_re.findall(ta_str)))


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day17()
    solution.set_input_data(data.split("\n"))

    part_one = solution.part_one()
    assert part_one == 45, f"Part one failed, got {part_one}"

    part_two = solution.part_two()
    assert part_two == 112, f"Part two failed, got {part_two}"


if __name__ == "__main__":
    test_solution(TEST_DATA)
