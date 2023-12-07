"""Day 7 of Advent of Code 2023"""
from collections import Counter
from enum import Enum
from functools import total_ordering
from itertools import product
from typing import Type
from typing import TypeVar


TEST_DATA = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

TEST_CASES = ((TEST_DATA, None, None),)

NORMAL_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
WILD_ORDER = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


@total_ordering
class HandType(Enum):
    five_of_a_kind = 7
    four_of_a_kind = 6
    full_house = 5
    three_of_a_kind = 4
    two_pair = 3
    one_pair = 2
    high_card = 1

    def __lt__(self, other):
        return self.value < other.value


def get_hand_type(cards: str) -> HandType:
    set_len = len(set(cards))

    if set_len == 1:
        return HandType.five_of_a_kind

    counts = Counter(cards)
    most_common = counts.most_common(1)[0][1]

    if most_common == 4:
        return HandType.four_of_a_kind

    if 3 in counts.values() and 2 in counts.values():
        return HandType.full_house

    if most_common == 3:
        return HandType.three_of_a_kind

    if set_len == 3:
        return HandType.two_pair

    if set_len == 4:
        return HandType.one_pair

    if set_len == 5:
        return HandType.high_card

    raise ValueError("Invalid hand")


@total_ordering
class Hand:
    cards: str
    wager: int
    hand_type: HandType

    card_order = NORMAL_ORDER

    def __init__(self, cards: str, wager: int):
        self.cards = cards
        self.wager = wager
        self.hand_type: HandType = self.get_hand_type()

    def get_hand_type(self) -> HandType:
        return get_hand_type(self.cards)

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.hand_type == other.hand_type:
            for card1, card2 in zip(self.cards, other.cards):
                if card1 == card2:
                    continue
                else:
                    return self.card_order.index(card1) < self.card_order.index(card2)

        return self.hand_type < other.hand_type

    def __repr__(self):
        return f"{self.__class__.__name__}({self.cards!r}, {self.wager!r})"


class WildHand(Hand):
    card_order = WILD_ORDER

    def __init__(self, cards: str, wager: int):
        super().__init__(cards, wager)

    def get_hand_type(self) -> HandType:
        best = super().get_hand_type()
        num_wilds = self.cards.count("J")

        if num_wilds == 0:
            return best

        if num_wilds == 5 or num_wilds == 4:
            return HandType.five_of_a_kind

        for perm in product(self.card_order, repeat=num_wilds):
            cards = self.cards
            for card in perm:
                cards = cards.replace("J", card, 1)

            best = max(best, get_hand_type(cards))

        return best


_T = TypeVar("_T", bound=Hand)


def get_hands(input_str: str, hand_cls: Type[_T]) -> list[_T]:
    hands = []
    for line in input_str.splitlines():
        cards, wager = line.split()
        hands.append(hand_cls(cards, int(wager)))

    return sorted(hands)


def part1(input_str: str) -> int:
    """Part 1 solution"""
    hands = get_hands(input_str, Hand)
    return sum(i * hand.wager for i, hand in enumerate(hands, 1))


def part2(input_str: str) -> int:
    """Part 2 solution"""
    hands = get_hands(input_str, WildHand)
    return sum(i * hand.wager for i, hand in enumerate(hands, 1))


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
