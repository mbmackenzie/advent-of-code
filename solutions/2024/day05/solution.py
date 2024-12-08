from __future__ import annotations

import pathlib
from dataclasses import dataclass
from dataclasses import field
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def parse(input_str):
    rules_str, pages_str = input_str.split("\n\n")

    rules = []
    for line in rules_str.splitlines():
        x, _, y = line.partition("|")
        rules.append((int(x), int(y)))

    pages = []
    for line in pages_str.strip().splitlines():
        pages.append([int(c) for c in line.split(",")])

    return rules, pages


def create_nodes(rules: list[tuple[int, int]]):
    nodes: dict[int, Node] = {}

    for l, r in rules:
        if l not in nodes:
            nodes[l] = Node(l)

        if r not in nodes:
            nodes[r] = Node(r)

        nodes[r].left.add(l)
        nodes[l].right.add(r)

    return nodes


def compute(nodes: dict[int, Node], page: list[int]):
    for i in range(len(page)):
        p = page[i]
        node = nodes[p]

        if not set(page[0:i]) <= node.left:
            return False

        if not set(page[i + 1 : -1]) <= node.right:
            return False

    return True


def part1(input_str: str) -> int:
    rules, pages = parse(input_str)
    nodes = create_nodes(rules)
    valid = [compute(nodes, page) for page in pages]

    return sum(p[(len(p) // 2)] for p, v in zip(pages, valid) if v)


@dataclass
class Node:
    value: int
    left: set[int] = field(default_factory=set)
    right: set[int] = field(default_factory=set)


def part2(input_str: str) -> int:
    rules, pages = parse(input_str)
    nodes = create_nodes(rules)
    valid = [compute(nodes, page) for page in pages]

    new_pages = [p for p, v in zip(pages, valid) if not v]

    for page in new_pages:
        curr = -1
        while not compute(nodes, page):
            i = curr
            p = page[i]
            node = nodes[p]

            if set(page[0:i]) <= node.left:
                curr -= 1
                continue

            while not set(page[0:i]) <= node.left:
                page[i - 1], page[i] = page[i], page[i - 1]
                i -= 1

    return sum(p[(len(p) // 2)] for p in new_pages)


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 143),
    ],
    [
        (TEST_DATA, 123),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
