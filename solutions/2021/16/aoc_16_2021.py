"""Day 16: Packet Decoder"""
from __future__ import annotations

from functools import reduce

import pytest
from aoc.solution import Solution

PRINT_PACKETS = False


class Packet:
    version: int
    type_id: int
    unused: str
    value: int

    def __init__(self, bin_string: str, depth: int = 0) -> None:
        self.depth = depth
        self.version, self.type_id = Packet.get_header(bin_string)

    @staticmethod
    def get_header(bin_string: str) -> tuple[int, int]:
        return int(bin_string[:3], 2), int(bin_string[3:6], 2)

    @staticmethod
    def create(bin_string: str, depth: int = 0) -> Packet:
        _, type_id = Packet.get_header(bin_string)

        if type_id == 4:
            return LiteralPacket(bin_string, depth)

        return OperatorPacket(bin_string, depth)

    def __repr__(self) -> str:
        return f"{' ' * self.depth}{type(self).__name__}" + "({})"


class LiteralPacket(Packet):
    value: int

    def __init__(self, bin_string: str, depth: int = 0) -> None:
        super().__init__(bin_string, depth)
        self.value = self._get_value(bin_string[6:])

        if PRINT_PACKETS:
            print(self)

    def _get_value(self, bin_string: str) -> int:
        digits = ""

        for i in range(0, len(bin_string), 5):
            segment = bin_string[i : i + 5]
            if len(segment) != 5:
                break
            digits += segment[1:]
            if segment[0] == "0":
                break

        self.unused = bin_string[i + 5 :]
        return int(digits, 2)

    def __repr__(self) -> str:
        rep_str = f"version={self.version}, type_id={self.type_id}, value={self.value}"
        return super().__repr__().format(rep_str)


class OperatorPacket(Packet):
    def __init__(self, bin_string: str, depth: int = 0) -> None:
        super().__init__(bin_string, depth)
        bin_string = bin_string[6:]

        self.length_type_id = int(bin_string[0])
        bin_string = bin_string[1:]

        bit_len = {0: 15, 1: 11}[self.length_type_id]
        self.sp_val = int(bin_string[:bit_len], 2)
        bin_string = bin_string[bit_len:]

        if PRINT_PACKETS:
            print(self)

        self.subpackets = self._get_subpackets(bin_string)
        self.value: int = self._get_value()

    @property
    def sub_values(self) -> list[int]:
        return [p.value for p in self.subpackets]

    def get_all_sub_versions(self) -> list[int]:
        versions = [self.version]
        for packet in self.subpackets:
            if isinstance(packet, LiteralPacket):
                versions.append(packet.version)
            elif isinstance(packet, OperatorPacket):
                versions.extend(packet.get_all_sub_versions())

        return versions

    def _get_value(self) -> int:

        if len(self.sub_values) >= 2:
            first, second = self.sub_values[:2]

        match self.type_id:
            case 0:
                return sum(self.sub_values)
            case 1:
                return reduce(lambda x, y: x * y, self.sub_values)
            case 2:
                return min(self.sub_values)
            case 3:
                return max(self.sub_values)
            case 5:
                return 1 if first > second else 0
            case 6:
                return 1 if first < second else 0
            case 7:
                return 1 if first == second else 0
            case _:
                raise ValueError(f"Invalid type_id: {self.type_id}")

    def _get_subpackets(self, bin_string: str) -> list[Packet]:

        packets: list[Packet] = []

        if self.length_type_id == 0:
            self.unused = bin_string[self.sp_val :]
            bin_string = bin_string[: self.sp_val]

        while bin_string:

            if len(bin_string) < 6:
                break

            _, type_id = Packet.get_header(bin_string)

            if type_id == 4:
                new_pkt: Packet = LiteralPacket(bin_string, depth=self.depth + 1)
            else:
                new_pkt = OperatorPacket(bin_string, depth=self.depth + 1)

            bin_string = new_pkt.unused
            packets.append(new_pkt)

            if self.length_type_id == 1:
                if len(packets) == self.sp_val:
                    self.unused = bin_string
                    break

        return packets

    def __repr__(self) -> str:
        rep_str = (
            f"version={self.version}, type_id={self.type_id}, "
            f"length_type_id={self.length_type_id}, "
            f"sp_val={self.sp_val}"
        )
        return super().__repr__().format(rep_str)


def make_packet(hex_string: str) -> Packet:
    bin_string = bin(int(hex_string, 16))[2:]

    if len(bin_string) % 4 != 0:
        padding = "0" * (4 - (len(bin_string) % 4))
        bin_string = padding + bin_string

    return Packet.create(bin_string)


class Day16(Solution):
    """Solution to day 16 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 16, "Packet Decoder")

    def _part_one(self) -> int:
        """
        Decode the structure of your hexadecimal-encoded BITS transmission;
        what do you get if you add up the version numbers in all packets?
        """
        packet = make_packet(self.data)
        return sum(packet.get_all_sub_versions())  # type: ignore

    def _part_two(self) -> int:
        """
        What do you get if you evaluate the expression represented by your
        hexadecimal-encoded BITS transmission?
        """
        packet = make_packet(self.data)
        return packet.value

    def _get_data(self) -> str:
        return self.input.as_list()[0]


@pytest.mark.parametrize(
    "data,part,expected",
    [
        ("8A004A801A8002F478", "part_one", 16),
        ("620080001611562C8802118E34", "part_one", 12),
        ("C0015000016115A2E0802F182340", "part_one", 23),
        ("A0016C880162017C3686B18A3D4780", "part_one", 31),
        ("C200B40A82", "part_two", 3),
        # ("04005AC33890", "part_two", 54),
        ("880086C3E88112", "part_two", 7),
        ("CE00C43D881120", "part_two", 9),
        ("D8005AC2A8F0", "part_two", 1),
        ("F600BC2D8F", "part_two", 0),
        ("9C005AC2F8F0", "part_two", 0),
        ("9C0141080250320F1802104A08", "part_two", 1),
    ],
)
def test_solution(data: str, part: str, expected: int) -> None:
    """Test the solution"""
    solution = Day16()
    solution.set_input_data(data.split("\n"))

    assert getattr(solution, part)() == expected


if __name__ == "__main__":
    pytest.main(["2021/day16.py"])
