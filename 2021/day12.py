"""Day 12: Passage Pathing"""
from collections import defaultdict
from typing import Optional

from aoc.solution import Solution

TEST_DATA = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip()

Cave = tuple[str, bool]
CaveSystem = dict[str, list[str]]

total = 0


def find_total_paths(
    graph: CaveSystem,
    big_caves: set[str],
    start: str = "start",
    end: str = "end",
    visited: Optional[dict[str, bool]] = None,
    path: Optional[list[str]] = None,
    total: int = 0,
) -> int:

    if not visited:
        visited = defaultdict(lambda: False)

    if not path:
        path = []

    visited[start] = True
    path.append(start)

    if start in big_caves:
        visited[start] = False

    if start == end:
        total += 1
    else:
        for node in graph[start]:
            if visited[node] is False:
                total = find_total_paths(
                    graph, big_caves, node, end, visited, path, total
                )

    path.pop()
    visited[start] = False

    return total


def find_total_paths2(
    graph: CaveSystem,
    big_caves: set[str],
    small_cave_exception: str,
    start: str = "start",
    end: str = "end",
    visited: Optional[dict[str, bool]] = None,
    path: Optional[list[str]] = None,
    total: int = 0,
    paths: Optional[list[list[str]]] = None,
    small_cave_count: int = 0,
) -> tuple[int, list[list[str]]]:

    if not visited:
        visited = defaultdict(lambda: False)

    if not path:
        path = []

    if not paths:
        paths = []

    visited[start] = True
    path.append(start)

    if start in big_caves:
        visited[start] = False

    if start == small_cave_exception:
        small_cave_count += 1
        if small_cave_count < 2:
            visited[start] = False

    if start == end:
        total += 1
        paths.append(path.copy())
    else:
        for node in graph[start]:
            if visited[node] is False:
                total, paths = find_total_paths2(
                    graph,
                    big_caves,
                    small_cave_exception,
                    node,
                    end,
                    visited,
                    path,
                    total,
                    paths,
                    small_cave_count,
                )

    path.pop()
    visited[start] = False

    return total, paths


class Day12(Solution):
    """Solution to day 12 of the 2021 Advent of Code"""

    big_caves: set[str]
    small_caves: set[str]

    def __init__(self) -> None:
        super().__init__(2021, 12, "Passage Pathing")

    def _part_one(self) -> int:
        """TODO"""
        return find_total_paths(self.data, self.big_caves)

    def _part_two(self) -> int:
        """TODO"""
        all_paths = []

        print(len(self.small_caves))

        for i, small_cave in enumerate(self.small_caves):
            print(f"{i}/{len(self.small_caves)}")
            tot, paths = find_total_paths2(self.data, self.big_caves, small_cave)
            print(f"Found {tot} paths")
            for path in paths:
                if path not in all_paths:
                    all_paths.append(path)
            print(f"Found {len(all_paths)} unique paths")

        return len(all_paths)

    def _get_data(self) -> CaveSystem:
        self.big_caves = set()
        self.small_caves = set()
        system: CaveSystem = defaultdict(list)

        def make_cave(name: str) -> str:
            if name == name.upper():
                self.big_caves.add(name)
            else:
                if name not in ("start", "end"):
                    self.small_caves.add(name)

            return name

        def make_caves(line: str) -> tuple[str, str]:
            node1, node2 = line.split("-")
            return make_cave(node1), make_cave(node2)

        caves = self.input.as_list(make_caves)
        for cave1, cave2 in caves:
            system[cave1].append(cave2)

            if not (cave1 == "start" or cave2 == "end"):
                system[cave2].append(cave1)

        return system


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day12()
    solution.set_input_data(data.split("\n"))

    part_one = solution.part_one()
    part_two = solution.part_two()
    assert part_one == 10, f"Part one test failed, got {part_one}"
    assert part_two == 36, f"Part one test failed, got {part_two}"


if __name__ == "__main__":
    test_solution(TEST_DATA)
