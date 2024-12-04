from __future__ import annotations

import pathlib
import re
from collections import Counter
from dataclasses import dataclass
from dataclasses import field
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


@dataclass
class Node:
    name: str
    value: int
    parent: Node | None = field(repr=False, default=None)
    children: list[Node] = field(repr=False, default_factory=list)
    weight = -1

    def _get_weight(self) -> int:
        return self.value + sum(n._get_weight() for n in self.children)


def map_nodes(names: list[str], nodes: list[Node], input_lines: list[str]):
    for i, line in enumerate(input_lines):
        if "->" in line:
            left = nodes[i]

            for right_name in line.partition(" -> ")[-1].split(", "):
                right_idx = names.index(right_name)
                right = nodes[right_idx]

                right.parent = left
                left.children.append(right)

    for node in nodes:
        node.weight = node._get_weight()


def part1(input_str: str) -> str:
    lines = input_str.splitlines()

    names = [l.partition(" ")[0] for l in lines]
    nodes = [Node(n, -1) for n in names]

    map_nodes(names, nodes, input_lines=lines)

    for node in nodes:
        if node.parent is None:
            return node.name

    raise ValueError("no bottom program found")


def part2(input_str: str) -> int:
    lines = input_str.splitlines()

    names = [l.partition(" ")[0] for l in lines]
    values = [int(re.findall(r"\((\d+)\)", l)[0]) for l in lines]
    nodes = [Node(n, v) for n, v in zip(names, values)]

    map_nodes(names, nodes, input_lines=lines)

    parent = None
    for node in nodes:
        if node.parent is None:
            parent = node
            break

    if not parent:
        raise ValueError("no bottom program found")

    for node in nodes:
        if not node.children:
            continue

        weights = Counter([c.weight for c in node.children])
        if len(weights) != 2:
            continue

        rev = {v: k for k, v in weights.items()}
        diff = rev[2] - rev[1]

        return {c.weight: c.value for c in node.children}[rev[1]] + diff


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, "tknk"),
    ],
    [
        (TEST_DATA, 60),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
