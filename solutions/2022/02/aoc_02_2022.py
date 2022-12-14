"""Day 2 of Advent of Code 2022

Column 1 = player 1 move
    A for Rock, B for Paper, and C for Scissors

WHEN Column 2 is player 2 move:
    X for Rock, Y for Paper, and Z for Scissors

WHEN column 2 is outcome:
    X means lose, Y means draw, and Z means win

POINTS
 - 1 for Rock, 2 for Paper, and 3 for Scissors
 - 0 if you lost, 3 if the round was a draw, and 6 if you won
"""

TEST_DATA = """\
A Y
B X
C Z
"""

TEST_CASES = ((TEST_DATA, 15, 12),)

OUTCOMES = {
    "AX": 3,  # Rock v Paper
    "AY": 6,  # Rock v Scissors
    "AZ": 0,  # Rock v Rock
    "BX": 0,  # Paper v Paper
    "BY": 3,  # Paper v Scissors
    "BZ": 6,  # Paper v Rock
    "CX": 6,  # Scissors v Paper
    "CY": 0,  # Scissors v Scissors
    "CZ": 3,  # Scissors v Rock
}

CHOICE = {"X": 1, "Y": 2, "Z": 3}
FORCE = {"X": 0, "Y": 3, "Z": 6}


def part1(input_str: str) -> int:
    """Part 1 solution"""

    games = map(str.split, input_str.splitlines())
    return sum(OUTCOMES[f"{p1}{p2}"] + CHOICE[p2] for p1, p2 in games)


def part2(input_str: str) -> int:
    """Part 2 solution"""

    games = map(str.split, input_str.splitlines())

    # go from [p1, p2]: outcome -> [p1, outcome]: p2
    what_do = {f"{c[0]}{o}": c[1] for c, o in OUTCOMES.items()}

    # FORCE[c2] is the outcome score, we need to find the choice score
    return sum((o := FORCE[c2]) + CHOICE[what_do[f"{p1}{o}"]] for p1, c2 in games)


if __name__ == "__main__":
    part1(TEST_DATA)
    part2(TEST_DATA)
