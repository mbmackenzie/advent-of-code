"""Day 12: Passage Pathing"""
from collections import defaultdict
from typing import NamedTuple

import pytest
from aoc.solution import Solution

CaveSystem = dict[str, set[str]]


def find_total_paths(cave_system: CaveSystem, allow_double_visits: bool = False) -> int:
    class State(NamedTuple):
        path: tuple[str, ...]
        double_visit: bool

    paths: set[tuple[str, ...]] = set()

    initial_state = State(("start",), False)
    stack: list[State] = [initial_state]

    while stack:
        state = stack.pop()
        cave = state.path[-1]

        if cave == "end":
            paths.add(state.path)
            continue

        for next_cave in cave_system[cave]:
            if next_cave == "start":
                continue

            if next_cave.isupper() or next_cave not in state.path:
                new_state = State((*state.path, next_cave), state.double_visit)
                stack.append(new_state)
                continue

            if allow_double_visits:
                if not state.double_visit and state.path.count(next_cave) == 1:
                    new_state = State((*state.path, next_cave), True)
                    stack.append(new_state)
                continue

    return len(paths)


class Day12(Solution):
    """Solution to day 12 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 12, "Passage Pathing")

    def _part_one(self) -> int:
        """
        How many paths through this cave system are there that visit
        small caves at most once?
        """
        return find_total_paths(self.data)

    def _part_two(self) -> int:
        """Given these new rules, how many paths through this cave system are there?"""
        return find_total_paths(self.data, allow_double_visits=True)

    def _get_data(self) -> CaveSystem:
        cave_system: CaveSystem = defaultdict(set)

        for line in self.input.as_list():
            cave1, cave2 = line.split("-")
            cave_system[cave1].add(cave2)

            if not (cave1 == "start" or cave2 == "end"):
                cave_system[cave2].add(cave1)

        return cave_system


TEST_DATA1 = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip()

TEST_DATA2 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""".strip()

TEST_DATA3 = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""".strip()


@pytest.mark.parametrize(
    "data,part,expected",
    [
        (TEST_DATA1, "part_one", 10),
        (TEST_DATA2, "part_one", 19),
        (TEST_DATA3, "part_one", 226),
        (TEST_DATA1, "part_two", 36),
        (TEST_DATA2, "part_two", 103),
        (TEST_DATA3, "part_two", 3509),
    ],
)
def test_solution_part_one(data: str, part: str, expected: int) -> None:
    """Test the solution"""
    solution = Day12()
    solution.set_input_data(data.split("\n"))

    assert getattr(solution, part)() == expected


if __name__ == "__main__":
    pytest.main(["2021/day12.py"])
