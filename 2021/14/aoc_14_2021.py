"""Day 14: Extended Polymerization"""
from collections import Counter
from itertools import pairwise

from aoc.solution import Solution

TEST_DATA = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".strip()


InsertionRules = dict[str, str]


def run_pair_insertion(template: str, rules: InsertionRules, num_steps: int = 10) -> Counter[str]:
    pair_counts = Counter(["".join(p) for p in pairwise(template)])

    for _ in range(num_steps):
        new_pair_counts: Counter[str] = Counter()
        element_counts: Counter[str] = Counter()

        for pair, count in pair_counts.items():
            left, middle, right = pair[0], rules[pair], pair[1]

            new_pair_counts[left + middle] += count
            new_pair_counts[middle + right] += count

            element_counts[left] += count
            element_counts[middle] += count

        element_counts[template[-1]] += 1
        pair_counts = new_pair_counts

    return element_counts


def get_element_difference(element_counts: Counter[str]) -> int:
    sorted_counts = sorted(element_counts.values())
    return sorted_counts[-1] - sorted_counts[0]


class Day14(Solution):
    """Solution to day 14 of the 2021 Advent of Code"""

    template: str

    def __init__(self) -> None:
        super().__init__(2021, 14, "Extended Polymerization")

    def _part_one(self) -> int:
        """
        After 10 steps, what do you get if you take the quantity of the most common element
        and subtract the quantity of the least common element?
        """
        element_counts = run_pair_insertion(self.template, self.data)
        return get_element_difference(element_counts)

    def _part_two(self) -> int:
        """
        After 40 steps, what do you get if you take the quantity of the most common element
        and subtract the quantity of the least common element?
        """
        element_counts = run_pair_insertion(self.template, self.data, num_steps=40)
        return get_element_difference(element_counts)

    def _pop_lines(self) -> None:
        self.template = self.input.pop_line()

    def _get_data(self) -> InsertionRules:
        rules: InsertionRules = dict()
        data: list[str] = self.input.as_list()

        for line in data:
            pair, value = line.split(" -> ")
            rules[pair] = value

        return rules


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day14()
    solution.set_input_data(data.split("\n"))

    part_one = solution.part_one()
    assert part_one == 1588, f"Part one failed, got {part_one}"

    part_two = solution.part_two()
    assert part_two == 2188189693529, f"Part two failed, got {part_two}"


if __name__ == "__main__":
    test_solution(TEST_DATA)
