"""Day 19 of Advent of Code 2022"""
from __future__ import annotations

import re
from collections import defaultdict
from math import prod
from typing import NamedTuple

from tools import AOC_TESTING

TEST_DATA = """\
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
"""

TEST_CASES = ((TEST_DATA, 33, None),)

ORE_ROBOT = re.compile(r"Each ore robot costs (\d+) ore\.")
CLAY_ROBOT = re.compile(r"Each clay robot costs (\d+) ore\.")
OBSIDIAN_ROBOT = re.compile(r"Each obsidian robot costs (\d+) ore and (\d+) clay\.")
GEODE_ROBOT = re.compile(r"Each geode robot costs (\d+) ore and (\d+) obsidian\.")


class Blueprint(NamedTuple):
    """Blueprint for a robot"""

    ore: int
    clay: int
    obsidian: tuple[int, int]
    geode: tuple[int, int]

    def max_robots_needed(self, robot: str) -> int:
        """Return the max number of robots needed to build a robot"""
        if robot == "geode":
            return 10000

        if robot == "ore":
            return max(self.ore, self.clay, self.obsidian[0], self.geode[0])

        if robot == "clay":
            return self.obsidian[1]

        if robot == "obsidian":
            return self.geode[1]

        raise ValueError(f"Invalid robot: {robot}")


class Supplies:
    def __init__(
        self,
        ore: int = 0,
        clay: int = 0,
        obsidian: int = 0,
        geodes: int = 0,
        ore_robots: int = 1,
        clay_robots: int = 0,
        obsidian_robots: int = 0,
        geode_robots: int = 0,
    ) -> None:

        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geodes = geodes
        self.ore_robots = ore_robots
        self.clay_robots = clay_robots
        self.obsidian_robots = obsidian_robots
        self.geode_robots = geode_robots

    def new(self) -> Supplies:
        return Supplies(
            ore=self.ore,
            clay=self.clay,
            obsidian=self.obsidian,
            geodes=self.geodes,
            ore_robots=self.ore_robots,
            clay_robots=self.clay_robots,
            obsidian_robots=self.obsidian_robots,
            geode_robots=self.geode_robots,
        )

    def add_robot(self, robot: str) -> Supplies:
        self.ore_robots += int(robot == "ore")
        self.clay_robots += int(robot == "clay")
        self.obsidian_robots += int(robot == "obsidian")
        self.geode_robots += int(robot == "geode")

        return self

    def update(self) -> Supplies:
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geodes += self.geode_robots

        return self

    def robots(self, robot: str) -> int:
        return getattr(self, f"{robot}_robots")


def parse_input(input_str: str) -> list[Blueprint]:

    if AOC_TESTING:
        tmp_input = input_str.split("\n\n")
        tmp_parts = []
        for bp in tmp_input:
            bp = " ".join(map(str.strip, bp.split("\n")))
            tmp_parts.append(bp)

        input_str = "\n".join(tmp_parts)

    blueprints = []

    for blueprint in input_str.splitlines():

        bp_args: dict[str, int | tuple[int, int]] = {}
        for robot, regex in zip(
            ["ore", "clay", "obsidian", "geode"],
            (ORE_ROBOT, CLAY_ROBOT, OBSIDIAN_ROBOT, GEODE_ROBOT),
        ):
            match = regex.search(blueprint)
            if not match:
                raise ValueError(f"Invalid blueprint: {blueprint}")

            if len(match.groups()) == 1:
                bp_args[robot] = int(match.group(1))

            elif len(match.groups()) == 2:
                bp_args[robot] = (int(match.group(1)), int(match.group(2)))

        blueprints.append(Blueprint(**bp_args))  # type: ignore

    return blueprints


def get_possible_moves(supplies: Supplies, blueprint: Blueprint) -> list[str]:
    """Return a list of possible moves"""

    if supplies.ore >= blueprint.geode[0] and supplies.obsidian >= blueprint.geode[1]:
        return ["geode"]

    moves = []
    if supplies.ore >= blueprint.ore:
        moves.append("ore")

    if supplies.ore >= blueprint.clay:
        moves.append("clay")

    if supplies.ore >= blueprint.obsidian[0] and supplies.clay >= blueprint.obsidian[1]:
        moves.append("obsidian")

    moves.append("wait")
    return moves


def build_robot(supplies: Supplies, robot: str, blueprint: Blueprint) -> None:
    """Build a robot"""

    if robot == "ore":
        supplies.ore -= blueprint.ore

    elif robot == "clay":
        supplies.ore -= blueprint.clay

    elif robot == "obsidian":
        supplies.ore -= blueprint.obsidian[0]
        supplies.clay -= blueprint.obsidian[1]

    elif robot == "geode":
        supplies.ore -= blueprint.geode[0]
        supplies.obsidian -= blueprint.geode[1]

    else:
        raise ValueError(f"Invalid robot: {robot}")


def get_num_geodes_opened(blueprint: Blueprint, max_time: int) -> int:
    stack: list[tuple[int, Supplies, set[str]]] = [(0, Supplies(), set())]
    best_each_minute: dict[int, int] = defaultdict(int)

    while stack:

        minute, supplies, skipped = stack.pop(0)
        best_each_minute[minute] = max(best_each_minute[minute], supplies.geodes)

        if minute > max_time or best_each_minute[minute] != supplies.geodes:
            continue

        possible_moves = set(get_possible_moves(supplies, blueprint))

        for move in possible_moves:

            new_supplies = supplies.new()

            if move == "wait":
                stack.append((minute + 1, new_supplies.update(), possible_moves))

            elif move in skipped:
                continue

            elif new_supplies.robots(move) + 1 > blueprint.max_robots_needed(move):
                continue

            else:
                build_robot(new_supplies, move, blueprint)
                stack.insert(0, (minute + 1, new_supplies.update().add_robot(move), set()))

    return best_each_minute[max_time]


def part1(input_str: str) -> int:
    """Part 1 solution"""

    blueprints = parse_input(input_str)
    total_quality = 0

    for i, blueprint in enumerate(blueprints, 1):
        geodes_opened = get_num_geodes_opened(blueprint, 24)
        total_quality += i * geodes_opened
        # print(f"Blueprint {i} - opened {geodes_opened} geodes ({i * geodes_opened} quality)")

    return total_quality


def part2(input_str: str) -> int:
    """Part 2 solution"""

    blueprints = parse_input(input_str)
    num_geodes = map(lambda bp: get_num_geodes_opened(bp, 32), blueprints[:3])

    return prod(num_geodes)


if __name__ == "__main__":
    AOC_TESTING = True  # noqa: F811

    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
