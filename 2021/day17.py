"""Day 17: Trick Shot"""
import re
from dataclasses import dataclass
from dataclasses import field

from aoc.solution import Solution


TEST_DATA = """
target area: x=20..30, y=-10..-5
""".strip()


@dataclass
class TargetArea:
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def check_within(self, x: int, y: int) -> bool:
        return (self.min_x <= x <= self.max_x) and (self.min_y <= y <= self.max_y)


@dataclass(unsafe_hash=True)
class Velocity:
    x: int
    y: int

    def apply_drag(self) -> None:
        if self.x != 0:
            self.x += -1 * (1 if self.x > 0 else -1)

        self.y -= 1


@dataclass
class Probe:
    initial_velocity: Velocity
    target_area: TargetArea = field(repr=False)

    x: int = field(init=False)
    y: int = field(init=False)
    velocity: Velocity = field(init=False, repr=False)
    path: list[tuple[int, int]] = field(init=False, repr=False)

    @property
    def max_height(self) -> int:
        return max(self.path, key=lambda p: p[1])[1]

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def reset(self) -> None:
        self.x = 0
        self.y = 0
        self.velocity = Velocity(self.initial_velocity.x, self.initial_velocity.y)
        self.path = []
        self.step_count = 0

    def run_step(self) -> None:
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.velocity.apply_drag()
        self.path.append((self.x, self.y))

        self.step_count += 1

    def eventually_lands_in_target(self) -> bool:
        self.reset()
        while not self.target_area.check_within(self.x, self.y):
            self.run_step()

            if self.x > self.target_area.max_x or self.y < self.target_area.min_y:
                return False

        return True


def get_velocities(target_area: TargetArea, chunk_size: int = 200) -> set[Velocity]:
    good_initial_velocities: set[Velocity] = set()
    start_x = 1
    start_y = target_area.min_y

    while True:
        hits_added = 0
        end_x = start_x + chunk_size
        end_y = start_y + chunk_size

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                initial_velocity = Velocity(x, y)
                p = Probe(initial_velocity, target_area)
                if p.eventually_lands_in_target():
                    good_initial_velocities.add(initial_velocity)
                    hits_added += 1

        if hits_added == 0:
            break

        start_x = end_x
        start_y = end_y

    return good_initial_velocities


class Day17(Solution):
    """Solution to day 17 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 17, "Trick Shot")

    def _part_one(self) -> int:
        """TODO"""
        target_area: TargetArea = self.data

        heights = []
        for initial_velocity in get_velocities(target_area, chunk_size=1000):
            p = Probe(initial_velocity, target_area)
            if p.eventually_lands_in_target():
                heights.append(p.max_height)

        return max(heights)

    def _part_two(self) -> int:
        """TODO"""
        target_area: TargetArea = self.data

        initial_velocities = get_velocities(target_area, chunk_size=1000)
        return len(initial_velocities)

    def _get_data(self) -> TargetArea:
        goal_str = self.input.as_list()[0]
        return TargetArea(*[int(v) for v in re.findall(r"(-?\d+)", goal_str)])


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day17()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 45
    assert solution.part_two() == 112


if __name__ == "__main__":
    test_solution(TEST_DATA)
