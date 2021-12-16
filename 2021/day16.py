"""Day 16: Packet Decoder"""
from dataclasses import dataclass

import pytest
from aoc.solution import Solution


@dataclass
class Packet:
    version: int
    type_id: int


class LiteralPacket(Packet):
    value: int

    def __init__(self, version: int, type_id: int, bin_string: str) -> None:
        super().__init__(version, type_id)
        self.value = self._get_value(bin_string)

    def _get_value(self, bin_string: str) -> int:
        digits = ""
        for i in range(0, len(bin_string), 5):
            segment = bin_string[i : i + 5]
            if len(segment) == 5:
                digits += segment[1:]

        return int(digits, 2)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"(version={self.version}, type_id={self.type_id}, value={self.value})"
        )


class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int, bin_string: str) -> None:
        super().__init__(version, type_id)
        self.length_id = int(bin_string[0])

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"(version={self.version}, type_id={self.type_id}, length_id={self.length_id})"
        )


def make_packet(hex_string: str) -> Packet:
    bin_string = bin(int(hex_string, 16))[2:]

    version = int(bin_string[:3], 2)
    type_id = int(bin_string[3:6], 2)

    if type_id == 4:
        return LiteralPacket(version, type_id, bin_string[6:])

    return OperatorPacket(version, type_id, bin_string[6:])


class Day16(Solution):
    """Solution to day 16 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 16, "Packet Decoder")

    def _part_one(self) -> int:
        """TODO"""
        for packet in self.data:
            print(packet)
        return NotImplemented

    def _part_two(self) -> int:
        """TODO"""
        return NotImplemented

    def _get_data(self) -> list[str]:
        return self.input.as_list(make_packet)


# @pytest.mark.parametrize(
#     "data,part,expected",
#     [
#         ("8A004A801A8002F478", "part_one", 16),
#         ("620080001611562C8802118E34", "part_one", 12),
#         ("C0015000016115A2E0802F182340", "part_one", 23),
#         ("A0016C880162017C3686B18A3D4780", "part_one", 31),
#     ],
# )
def test_solution(data: str, part: str, expected: int) -> None:
    """Test the solution"""
    solution = Day16()
    solution.set_input_data(data.split("\n"))

    assert getattr(solution, part)() == expected


if __name__ == "__main__":
    # pytest.main(["2021/day16.py"])
    test_solution("D2FE28\n38006F45291200\nEE00D40C823060", "part_one", NotImplemented)
