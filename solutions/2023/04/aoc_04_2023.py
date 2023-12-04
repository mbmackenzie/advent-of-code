"""Day 4 of Advent of Code 2023"""

from collections import defaultdict
from typing import Iterator, NamedTuple


TEST_DATA = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 1
"""

TEST_CASES = ((TEST_DATA, 13, 30),)

Digits = set[int]


class Card(NamedTuple):
    num: int
    winning_digits: Digits
    picks: Digits

    @property
    def num_correct(self) -> int:
        return len(self.winning_digits.intersection(self.picks))


def iter_cards(input_str: str) -> Iterator[Card]:
    for card_num, line in enumerate(input_str.splitlines(), 1):
        digits = line.split(":")[1]
        winning_digits_str, _, picks_str = digits.partition("|")

        winning_digits = set([int(d) for d in winning_digits_str.split()])
        picks = set([int(d) for d in picks_str.split()])

        yield Card(card_num, winning_digits, picks)


def part1(input_str: str) -> int:
    """Part 1 solution"""
    return sum(
        2 ** (card.num_correct - 1)
        for card in iter_cards(input_str)
        if card.num_correct > 0
    )


def part2(input_str: str) -> int:
    """Part 2 solution"""

    card_stack = defaultdict(lambda: 1)

    for card in iter_cards(input_str):
        current_copies = card_stack[card.num]
        for j in range(card.num + 1, card.num + card.num_correct + 1):
            card_stack[j] += current_copies

    return sum(card_stack.values())


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
