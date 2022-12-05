"""Day 21: Dirac Dice"""
from functools import lru_cache
from itertools import product
from typing import Counter

from aoc.solution import Solution

TEST_DATA = """
Player 1 starting position: 4
Player 2 starting position: 8
""".strip()


class DeterministicDice:
    def __init__(self) -> None:
        self.next_val = 1
        self.roll_count = 0

    def roll(self) -> int:
        ret = self.next_val
        if self.next_val == 100:
            self.next_val = 1
        else:
            self.next_val += 1

        self.roll_count += 1
        return ret

    def mutli_roll(self, num: int = 3) -> tuple[int, ...]:
        return tuple(self.roll() for _ in range(num))


def update_space(space: int) -> int:
    while space > 10:
        space -= 10
    return space


class Day21(Solution):
    """Solution to day 21 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 21, "Dirac Dice")

    def _part_one(self) -> int:
        """TODO"""
        dice = DeterministicDice()
        pos1, score1 = self.data[0], 0
        pos2, score2 = self.data[1], 0

        while True:
            roll_total = sum(dice.mutli_roll())
            pos1 = update_space(pos1 + roll_total)
            score1 += pos1
            if score1 >= 1000:
                return score2 * dice.roll_count

            roll_total = sum(dice.mutli_roll())
            pos2 = update_space(pos2 + roll_total)
            score2 += pos2
            if score2 >= 1000:
                return score1 * dice.roll_count

    def _part_two(self) -> int:
        """TODO"""
        pos1, score1 = self.data[0], 0
        pos2, score2 = self.data[1], 0
        possible_rolls = Counter(sum(p) for p in product((1, 2, 3), repeat=3))

        @lru_cache(maxsize=None)
        def get_win_counts(
            pos1: int,
            score1: int,
            pos2: int,
            score2: int,
        ) -> tuple[int, int]:
            player1_wins = player2_wins = 0
            for roll_total, count in possible_rolls.items():
                pos1_ = update_space(pos1 + roll_total)
                score1_ = score1 + pos1_
                if score1_ >= 21:
                    player1_wins += count
                else:
                    p2_wins, p1_wins = get_win_counts(pos2, score2, pos1_, score1_)
                    player1_wins += p1_wins * count
                    player2_wins += p2_wins * count

            return player1_wins, player2_wins

        return max(get_win_counts(pos1, score1, pos2, score2))

    def _get_data(self) -> tuple[int, int]:
        data = self.input.as_list()
        p1 = int(data[0].split(": ")[1])
        p2 = int(data[1].split(": ")[1])
        return p1, p2


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day21()
    solution.set_input_data(data.split("\n"))

    part_one = solution.part_one()
    assert part_one == 739785, f"Part one failed, got {part_one}"

    part_two = solution.part_two()
    assert part_two == 444356092776315, f"Part two failed, got {part_two}"


if __name__ == "__main__":
    test_solution(TEST_DATA)
