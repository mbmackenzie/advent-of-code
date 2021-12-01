"""Day 14"""
import re
from dataclasses import dataclass

from aoc.solution import Solution


TEST_DATA = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""".strip()


@dataclass
class Chunk:
    """Chunk of instructions that use a certain mask"""

    mask: str
    instructions: list[tuple[int, int]]


def mask_value(mask: str, value: int) -> int:
    """Mask a value"""
    value_str = f"{value:b}".zfill(len(mask))
    masked_str = "".join([v if m == "X" else m for v, m in zip(value_str, mask)])

    return int(masked_str, 2)


class Day14(Solution):
    """Solution to day 14 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 14, "")

    def _part_one(self) -> int:
        """What is the sum of in memory values after executing the program?"""
        memory = {}

        for chunk in self.data:
            for address, value in chunk.instructions:
                masked_value = mask_value(chunk.mask, value)
                memory[address] = masked_value

        return sum(memory.values())

    def _part_two(self) -> int:
        """TODO"""
        return NotImplemented

    def _get_data(self) -> list[Chunk]:
        def get_chunk(data_str: str) -> Chunk:
            data = data_str.split("\n")
            cleaned: list[tuple[int, int]] = []
            for instruction in data[1:]:
                if not instruction:
                    continue

                match = re.match("mem\[(\d+)\] = (\d+)", instruction)
                if not match:
                    raise ValueError(f"Invalid instruction, {instruction}")

                groups = match.groups()
                cleaned.append((int(groups[0]), int(groups[1])))

            return Chunk(data[0][7:], cleaned)

        return self.input.as_list(get_chunk)

    def _reformat_data(self) -> None:
        """Chunk data by mask"""

        def block_by_mask(content: list[str]) -> list[str]:
            content_str = "\n".join([item.strip() for item in content])
            split_by_mask = [x for x in re.split(r"(mask = \w+)", content_str) if x]

            data = []
            for i in range(0, len(split_by_mask), 2):
                data.append(split_by_mask[i] + split_by_mask[i + 1])

            return data

        self.input.reformat(block_by_mask)


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day14()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 165
    assert solution.part_two() == NotImplemented


if __name__ == "__main__":
    test_solution(TEST_DATA)
