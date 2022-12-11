"""Day 11 of Advent of Code 2022"""
import re
from functools import reduce
from typing import Iterable
from typing import Literal
from typing import Sequence

TEST_DATA = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

TEST_CASES = ((TEST_DATA, 10605, 2713310158),)


STARTING_ITEMS = re.compile(r"Starting items: (.+)")
TEST = re.compile(r"Test: divisible by (\d+)")
IF_TRUE = re.compile(r"If true: throw to monkey (\d+)")
IF_FALSE = re.compile(r"If false: throw to monkey (\d+)")
OPERATOR = re.compile(r"Operation: new = old (.) .*")
OPERAND = re.compile(r"Operation: new = old .* (.+)")


class Monkey:
    def __init__(
        self,
        starting_items: list[int],
        operator: str,
        operand: int | Literal["old"],
        test_val: int,
        if_true: int,
        if_false: int,
    ):
        self.starting_items = starting_items
        self.operator = operator
        self.operand = operand
        self.test_val = test_val
        self.if_true = if_true
        self.if_false = if_false

    def doop(self, item: int) -> int:

        if self.operand == "old":
            operand = item
        else:
            operand = self.operand

        if self.operator == "*":
            return item * operand
        elif self.operator == "+":
            return item + operand
        else:
            raise ValueError(f"Unknown operator {self.operator}")

    def test(self, item: int) -> int:
        if item % self.test_val == 0:
            return self.if_true
        else:
            return self.if_false


def parse_monkeyz(input_str: str) -> list[Monkey]:

    monkeyz = []

    for monkey_str in input_str.split("\n\n"):

        operand = OPERAND.findall(monkey_str)[0]
        if operand != "old":
            operand = int(operand)

        monkey = Monkey(
            [int(item) for item in STARTING_ITEMS.findall(monkey_str)[0].split(", ")],
            OPERATOR.findall(monkey_str)[0],
            operand,
            int(TEST.findall(monkey_str)[0]),
            int(IF_TRUE.findall(monkey_str)[0]),
            int(IF_FALSE.findall(monkey_str)[0]),
        )

        monkeyz.append(monkey)

    return monkeyz


def product(iterable: Iterable[int]) -> int:
    return reduce(lambda x, y: x * y, iterable)


def print_inspections(inspections: dict[int, int]) -> None:
    print("Most Active Monkey:")
    for monkey, num_inspections in inspections.items():
        print(f"Monkey {monkey}: inspected items {num_inspections} times")


def init_inspections(monkeyz: list[Monkey]) -> tuple[list[int], list[int], dict[int, int], int]:
    items = []
    inspectors = []
    inspections = {monkey: 0 for monkey in range(len(monkeyz))}
    lcm = product(monkey.test_val for monkey in monkeyz)

    for monkey_id, monkey in enumerate(monkeyz):
        for item in monkey.starting_items:
            items.append(item)
            inspectors.append(monkey_id)

    return items, inspectors, inspections, lcm


def throw_them_items(
    rounds: int,
    monkeyz: list[Monkey],
    very_worried: bool,
    checkpoints: Sequence[int] | None = None,
) -> dict[int, int]:

    items, inspectors, inspections, lcm = init_inspections(monkeyz)

    for _round in range(rounds):
        for id, monkey in enumerate(monkeyz):
            for i, (item, inspector) in enumerate(zip(items, inspectors)):

                if inspector != id:
                    continue

                inspections[id] += 1
                new_item = monkey.doop(item) // 3 if very_worried else monkey.doop(item) % lcm

                items[i] = new_item
                inspectors[i] = monkey.test(new_item)

        if checkpoints and _round + 1 in checkpoints:
            print_inspections(inspections)

    return inspections


def part1(input_str: str) -> int:
    """Part 1 solution"""
    checkpoints = None  # list(range(2, 11)) + [15, 20]

    monkeyz = parse_monkeyz(input_str)
    inspections = throw_them_items(20, monkeyz, very_worried=True, checkpoints=checkpoints)

    return product(sorted(inspections.values())[-2:])


def part2(input_str: str) -> int:
    """Part 2 solution"""
    checkpoints = None  # (1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000)

    monkeyz = parse_monkeyz(input_str)
    inspections = throw_them_items(10000, monkeyz, very_worried=False, checkpoints=checkpoints)

    return product(sorted(inspections.values())[-2:])


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
