"""Day 10 of Advent of Code 2022"""
from collections import defaultdict
from pathlib import Path
from typing import Iterator
from typing import Protocol

SMALL_TEST_DATA = """\
noop
addx 3
addx -5
"""

with open(Path(__file__).parent / "sample.txt") as f:
    TEST_DATA = f.read()

TEST_CASES = ((TEST_DATA, 13140, "See printed output"),)


class CycleHook(Protocol):
    def __call__(self, cycle: int, X: int) -> None:
        ...


def iter_commands(commands: list[str]) -> Iterator[tuple[int, int]]:
    for command in commands:
        if command == "noop":
            yield 1, 0
        elif command.startswith("addx"):
            yield 2, int(command.split()[1])


def start_cycle(
    commands: list[str],
    mid_cycle_hook: CycleHook | None = None,
    end_cycle_hook: CycleHook | None = None,
) -> tuple[int, int]:

    # init system
    X, cycle, waiting = 1, 0, 0

    # create command iterator, and get first command
    todo = iter_commands(commands)
    wait, add = next(todo)

    # start the system
    while True:

        # update cycle and waiting
        cycle += 1
        waiting += 1

        # run mid cycle hook if it exists
        if mid_cycle_hook is not None:
            mid_cycle_hook(cycle, X)

        # if we've waited as long as the command takes:
        if waiting == wait:

            # update register, reset waiting, and get next command
            X += add
            waiting = 0

            if end_cycle_hook is not None:
                end_cycle_hook(cycle, X)

            try:
                wait, add = next(todo)
            except StopIteration:
                break

    return cycle, X


def create_sprite(X: int) -> dict[int, int]:
    sprite: dict[int, int] = defaultdict(int)
    for i in range(X - 1, X + 2):
        sprite[i] = 1

    return sprite


def part1(input_str: str) -> int:
    """Part 1 solution"""

    interesting_signal_strength = 0

    def mid_cycle_hook(cycle: int, X: int) -> None:
        nonlocal interesting_signal_strength
        if cycle == 20 or (cycle - 20) % 40 == 0:
            interesting_signal_strength += cycle * X

    start_cycle(input_str.splitlines(), mid_cycle_hook)
    return interesting_signal_strength


def part2(input_str: str) -> str:
    """Part 2 solution"""

    sprite: dict[int, int] = create_sprite(1)

    def mid_cycle_hook(cycle: int, X: int) -> None:
        nonlocal sprite

        if sprite[((cycle - 1) % 40)] == 1:
            print("#", end="")
        else:
            print(".", end="")

        if cycle % 40 == 0:
            print()

    def end_cycle_hook(cycle: int, X: int) -> None:
        nonlocal sprite
        sprite = create_sprite(X)

    print()
    print("=" * 40)
    start_cycle(input_str.splitlines(), mid_cycle_hook, end_cycle_hook)
    print("=" * 40)
    return "See printed output"


if __name__ == "__main__":

    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
