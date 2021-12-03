"""Day 3"""
from typing import NamedTuple

from aoc.solution import Solution


TEST_DATA = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".strip()


class BinNum(NamedTuple):
    """Wrapper for binary number with useful methods"""

    value: str

    @staticmethod
    def from_list(bits: list[int]) -> "BinNum":
        """Create a new binary number from a list of ones and zeros"""
        return BinNum("".join([str(b) for b in bits]))

    @staticmethod
    def list_to_int(bits: list[int]) -> int:
        """Go straight from list of ones and zeros to a decimal int"""
        return BinNum.from_list(bits).as_int()

    def as_int(self) -> int:
        """Convert binary number to integer"""
        return int(self.value, 2)

    def get_bit(self, position: int) -> int:
        """Get the value of a single bit at a given position"""
        return int(self.value[position])

    def __len__(self) -> int:
        return len(self.value)


class Report(NamedTuple):
    """Container for a list of numbers"""

    nums: list[BinNum]

    @property
    def bits(self) -> int:
        """Number of bits in each number"""
        return len(self.nums[0])

    def get_bits_at_position(self, position: int) -> list[int]:
        """Get the bit at the given position for every number in the report"""
        return [b.get_bit(position) for b in self.nums]

    def get_majority_bit(self, position: int) -> int:
        """
        Find the bit that occurs the most at the given position
        for every number in the report
        """
        bits = self.get_bits_at_position(position)
        return int(sum(bits) >= (len(self.nums) - sum(bits)))

    def filter_nums_by_bit(self, value: int, position: int) -> "Report":
        """
        Make a new report with only the numbers that have the
        given value at the given position
        """
        return Report([b for b in self.nums if b.get_bit(position) == value])

    def __len__(self) -> int:
        return len(self.nums)


class Day03(Solution):
    """Solution to day 3 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 3, "")

    def _part_one(self) -> int:
        """What is the power consumption of the submarine?"""
        report: Report = self.data

        gamma = []
        epsilon = []

        for bit_idx in range(report.bits):
            majority_bit = report.get_majority_bit(bit_idx)
            gamma.append(majority_bit)
            epsilon.append(1 - majority_bit)

        return BinNum.list_to_int(gamma) * BinNum.list_to_int(epsilon)

    def _part_two(self) -> int:
        """What is the life support rating of the submarine?"""

        def get_rating(report: Report, flip_majority: bool = False) -> BinNum:
            """Get the life support component rating"""
            for bit_idx in range(report.bits):
                majority_bit = report.get_majority_bit(bit_idx)

                if flip_majority:
                    majority_bit = 1 - majority_bit

                report = report.filter_nums_by_bit(majority_bit, bit_idx)

                if len(report) == 1:
                    break

            return report.nums[0]

        oxygen_rating = get_rating(self.data)
        co2_rating = get_rating(self.data, flip_majority=True)
        return oxygen_rating.as_int() * co2_rating.as_int()

    def _get_data(self) -> Report:
        return Report(self.input.as_list(BinNum))


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day03()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 198
    assert solution.part_two() == 230


if __name__ == "__main__":
    test_solution(TEST_DATA)
