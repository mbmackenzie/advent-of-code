"""Day 10"""
from typing import Optional

from aoc.solution import Solution


TEST_DATA = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip()

CORRUPTED_POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}
MISSING_POINTS = {")": 1, "]": 2, "}": 3, ">": 4}

BRACKET_MAP = {"{": "}", "[": "]", "(": ")", "<": ">"}


def parse_bracket_pairs(line: str) -> tuple[list[str], Optional[str]]:
    """Parse bracket pairs

    Returns:
        list[str]: The stack of brackets that were not closed
        Optional[str]: If present, this is the bracket that is corrupted
    """
    stack: list[str] = []
    for char in line:
        if char in BRACKET_MAP.keys():
            stack.append(char)

        if char in BRACKET_MAP.values():
            if char != BRACKET_MAP[stack[-1]]:
                return stack, char
            else:
                stack.pop()

    return stack, None


def complete_line(line: str) -> Optional[str]:
    """Complete a line"""
    stack, char = parse_bracket_pairs(line)
    if char:
        return None
    return "".join(reversed([BRACKET_MAP[char] for char in stack]))


def get_corrupted_score(line: str) -> int:
    _, char = parse_bracket_pairs(line)
    if char:
        return CORRUPTED_POINTS[char]

    return 0


class Day10(Solution):
    """Solution to day 10 of the 2021 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2021, 10, "")

    def _part_one(self) -> int:
        """TODO"""
        return sum(get_corrupted_score(line) for line in self.data)

    def _part_two(self) -> int:
        """TODO"""

        def calc_score(closings: str) -> int:
            score = 0
            for char in closings:
                score = (score * 5) + MISSING_POINTS[char]
            return score

        scores = []
        for line in self.data:
            closings = complete_line(line)
            if closings:
                scores.append(calc_score(closings))

        scores.sort()
        return scores[len(scores) // 2]


def test_solution(data: str) -> None:
    """Test the solution"""
    solution = Day10()
    solution.set_input_data(data.split("\n"))

    assert solution.part_one() == 26397
    assert solution.part_two() == 288957


if __name__ == "__main__":
    test_solution(TEST_DATA)
