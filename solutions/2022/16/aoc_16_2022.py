"""Day 16 of Advent of Code 2022"""
from __future__ import annotations

import heapq
import re
from itertools import combinations
from typing import NamedTuple


TEST_DATA = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

PARSE_REGEX = re.compile(
    r"Valve ([A-Z]{2}) has flow rate=(\d+); "
    r"tunnels? leads? to valves? ([A-Z]{2}(?:, [A-Z]{2})*)",
)

TEST_CASES = ((TEST_DATA, 1651, None),)

from collections import defaultdict


Rates = dict[str, int]
Graph = dict[str, set[str]]
WeightedGraph = dict[str, set[tuple[str, int]]]


def parse_input(input_str: str) -> tuple[Rates, Graph]:
    rates: dict[str, int] = defaultdict(int)
    graph: Graph = defaultdict(set)

    for line in input_str.splitlines():
        valve, flow_rate, leads_to = PARSE_REGEX.findall(line)[0]
        graph[valve].update(leads_to.split(", "))

        if (flow_rate := int(flow_rate)) == 0:
            continue

        rates[valve] = int(flow_rate)

    all_nodes = set(graph.keys())

    graph["IN"] = {"AA"}
    graph["OUT"] = set()

    for leads_to in graph.values():
        all_nodes.update(leads_to)

    for node in all_nodes:
        if node in ("IN", "OUT"):
            continue

        graph[node].add("OUT")

    return rates, graph


def shortest_path(graph: Graph, start: str, end: str) -> tuple[str, ...]:

    visited = set()
    stack: list[tuple[str, ...]] = [(start,)]

    while stack:
        path = stack.pop(0)
        node = path[-1]

        if node not in visited:
            visited.add(node)

            if node == end:
                return path

            for next_node in graph[node]:
                stack.append((*path, next_node))

    return ()


def preview_testcase1(graph: Graph, rates: Rates, total_time: int) -> None:
    correct_path = ("IN", "DD", "BB", "JJ", "HH", "EE", "CC", "OUT")
    minute = 0
    total_ppm = 0
    total_pressure = 0
    for node, next_node in zip(correct_path, correct_path[1:]):
        time_to_move = len(shortest_path(graph, node, next_node))
        minute += time_to_move
        rate = rates[next_node]
        new_pressure = rate * (total_time - minute + 1)

        total_ppm += rate
        total_pressure += new_pressure

        print(f"Move from {node} -> {next_node}")
        print(f"  - It takes {time_to_move} minutes to get there and open it")
        print(f"  - At minute {minute} it will begin producing pressure at {rate} per minute")
        print(f"  - At minute {total_time} it will have produced {new_pressure} pressure")
        print(f"  - Total pressure so far: {total_pressure} ({total_ppm} per minute)")
        print()


def condense_graph(graph: Graph, rates: Rates) -> WeightedGraph:
    new_graph = defaultdict(set)
    for n1, n2 in combinations(["IN", "OUT", *rates.keys()], 2):
        for start, end in [(n1, n2), (n2, n1)]:
            if path := shortest_path(graph, start, end):
                new_graph[start].add((end, len(path)))

    return new_graph


class State(NamedTuple):

    path: tuple[str, ...]
    time: int
    pressure: int
    done: bool = False

    @property
    def last_node(self) -> str:
        return self.path[-1]

    @property
    def all_nodes(self) -> set[str]:
        return set(self.path)

    def __hash__(self) -> int:
        return hash(self.path)


def part1(input_str: str) -> float:
    """Part 1 solution"""

    MAX_TIME = 30

    rates, graph = parse_input(input_str)
    new_graph = condense_graph(graph, rates)

    preview_testcase1(graph, rates, MAX_TIME)

    initial_state = State(("IN",), 0, 0)
    stack = [(0, initial_state)]

    best_pressure = -float("inf")
    best_state = None
    while stack:
        _, state = heapq.heappop(stack)

        if state.time > MAX_TIME or state.last_node == "OUT":

            if state.pressure >= best_pressure:
                best_pressure = state.pressure
                best_state = state

            continue

        for next_node, distance in new_graph[state.last_node]:
            if next_node in state.path:
                continue

            rate = rates.get(next_node, 0)
            time_to_open = distance + state.time
            new_pressure = rate * (MAX_TIME - time_to_open + 1)

            new_state = State(
                state.path + (next_node,),
                time_to_open,
                state.pressure + new_pressure,
            )

            heapq.heappush(stack, ((-new_state.pressure, new_state)))

    print(best_state)
    return best_pressure


class CombinedState(NamedTuple):
    me: State
    elephant: State

    @property
    def all_nodes(self) -> set[str]:
        return self.me.all_nodes | self.elephant.all_nodes

    @property
    def pressure(self) -> int:
        return self.me.pressure + self.elephant.pressure

    @property
    def done(self) -> bool:
        return self.me.done and self.elephant.done


def part2(input_str: str) -> int:
    """Part 2 solution"""

    MAX_TIME = 26

    rates, graph = parse_input(input_str)
    new_graph = condense_graph(graph, rates)

    my_initial_state = State(("IN",), 0, 0)
    elephant_initial_state = State(("IN",), 0, 0)

    initial_state = CombinedState(my_initial_state, elephant_initial_state)
    stack = [initial_state]

    best_pressure = -float("inf")
    best_state = None

    seen_paths = set()

    while stack:

        state = stack.pop()

        if state.done or set(rates.keys()) <= state.all_nodes:
            print(state)

            seen_paths.add(state.me.path)
            seen_paths.add(state.elephant.path)

            if state.pressure >= best_pressure:
                best_pressure = state.pressure
                best_state = state

            continue

        for next_node, distance in new_graph[state.me.last_node]:
            if next_node in state.all_nodes:
                continue

            if state.me.done:
                my_new_state = State(
                    state.me.path,
                    state.me.time,
                    state.me.pressure,
                    done=True,
                )

            else:

                rate = rates.get(next_node, 0)
                time_to_open = distance + state.me.time
                new_pressure = rate * (MAX_TIME - time_to_open + 1)

                done = time_to_open > MAX_TIME or next_node == "OUT"

                my_new_state = State(
                    state.me.path + (next_node,),
                    time_to_open,
                    state.me.pressure + new_pressure,
                    done=done,
                )

            for next_node, distance in new_graph[state.elephant.last_node]:
                if next_node in state.all_nodes.union(my_new_state.all_nodes):
                    continue

                if state.elephant.done:
                    elephant_new_state = State(
                        state.elephant.path,
                        state.elephant.time,
                        state.elephant.pressure,
                        done=True,
                    )

                else:

                    rate = rates.get(next_node, 0)
                    time_to_open = distance + state.elephant.time
                    new_pressure = rate * (MAX_TIME - time_to_open + 1)

                    done = time_to_open > MAX_TIME or next_node == "OUT"

                    elephant_new_state = State(
                        state.elephant.path + (next_node,),
                        time_to_open,
                        state.elephant.pressure + new_pressure,
                        done=done,
                    )

                stack.append(CombinedState(my_new_state, elephant_new_state))

    print("Best state:")
    print(best_state.me)
    print(best_state.elephant)
    print("Total pressure:", best_pressure)

    return best_pressure


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
