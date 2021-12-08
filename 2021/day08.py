"""Day 8: Seven Segment Search"""
from aoc.solution import Solution

Data = tuple[list[str], list[str]]

TEST_DATA = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".strip()


class Day08(Solution):
    """Solution to day 8 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 8, "Seven Segment Search")

    def _part_one(self) -> int:
        """In the output values, how many times do digits 1, 4, 7, or 8 appear?"""
        total = 0
        for _, output in self.data:
            total += sum(len(segment) in (2, 3, 4, 7) for segment in output)

        return total

    def _part_two(self) -> int:
        """What do you get if you add up all of the output values?"""

        def find_by_len(wires: list[str], length: int) -> str:
            for wire in wires:
                if len(wire) == length:
                    return wire

            raise ValueError(f"No wire of length {length} found")

        def segment_contains_other(segment: str, other: str) -> bool:
            for char in other:
                if char not in segment:
                    return False
            return True

        total = 0
        for wires, outputs in self.data:
            assignments = {}
            assignments[1] = find_by_len(wires, 2)
            assignments[4] = find_by_len(wires, 4)
            assignments[7] = find_by_len(wires, 3)
            assignments[8] = find_by_len(wires, 7)

            for wire in [w for w in wires if len(w) == 6]:
                if segment_contains_other(wire, assignments[1]):
                    if segment_contains_other(wire, assignments[4]):
                        assignments[9] = wire
                    else:
                        assignments[0] = wire
                else:
                    assignments[6] = wire

            for wire in [w for w in wires if len(w) == 5]:
                if segment_contains_other(wire, assignments[1]):
                    assignments[3] = wire
                else:
                    if segment_contains_other(assignments[9], wire):
                        assignments[5] = wire
                    else:
                        assignments[2] = wire

            digits = []
            for segment in outputs:
                for key, value in assignments.items():
                    if sorted(segment) == sorted(value):
                        digits.append(key)

            total += int("".join(map(str, digits)))

        return total

    def _get_data(self) -> list[Data]:
        def parse_input(input_data: str) -> Data:
            parts = input_data.split(" | ")
            return parts[0].split(), parts[1].split()

        return self.input.as_list(parse_input)


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day08()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 26
    assert solution.part_two() == 61229


if __name__ == "__main__":
    test_solution(TEST_DATA)
