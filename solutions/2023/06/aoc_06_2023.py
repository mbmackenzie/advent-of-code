"""Day 6 of Advent of Code 2023

let s = time holding button, t = total time of race, d = distance to travel, then,

d  =  s * (t - s)
d  =  st - s^2
   => s^2 - ts + d = 0

Using quadratic formula, we find roots of the equation,
and then find the number of integers between them.

Use d + 1 to account for the fact that we are looking for the number of integers greater than d.
"""
import math
from typing import Iterator
from typing import Literal
from typing import NamedTuple
from typing import overload

# import functools

TEST_DATA = """\
Time:      7  15   30
Distance:  9  40  200
"""

TEST_CASES = ((TEST_DATA, 288, 71503),)


class Race(NamedTuple):
    time: int
    distance: int


@overload
def parse_input(input_str: str, combine: Literal[False]) -> Iterator[list[int]]:
    ...


@overload
def parse_input(input_str: str, combine: Literal[True]) -> Iterator[int]:
    ...


def parse_input(input_str: str, combine: bool = False) -> Iterator[list[int] | int]:
    for line in input_str.splitlines():
        _, *values = line.split()

        if combine:
            yield int("".join(values))
        else:
            yield [int(v) for v in values]


def quadratic(a: float, b: float, c: float) -> tuple[float, float]:
    """Solve quadratic equation for pos and neg roots"""
    # (-b +/- sqrt(b^2 - 4ac)) / 2a

    pos = (-b + (b**2 - 4 * a * c) ** 0.5) / (2 * a)
    neg = (-b - (b**2 - 4 * a * c) ** 0.5) / (2 * a)

    return pos, neg


def get_num_winning_holds(race) -> int:
    lower, upper = sorted(quadratic(1, -race.time, race.distance + 1))
    return math.floor(upper) - math.ceil(lower) + 1


def part1(input_str: str) -> int:
    """Part 1 solution"""

    races = [Race(t, d) for t, d in zip(*parse_input(input_str, combine=False))]

    # cheeky one liner using part 2 solution
    # return functools.reduce(lambda a, r: a * get_num_winning_holds(r), races, 1)

    tot = 1

    for race in races:
        tot *= sum(1 for s in range(race.time + 1) if s * (race.time - s) > race.distance)

    return tot


def part2(input_str: str) -> int:
    """Part 2 solution"""

    race = Race(*parse_input(input_str, combine=True))
    return get_num_winning_holds(race)


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
