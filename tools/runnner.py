import argparse
from pathlib import Path
from typing import Callable
from typing import Sequence

from rich.console import Console
from rich.table import Table

console = Console()
PartFn = Callable[[str], int | str]

TestCase = tuple[str, int | str]
TestCases = tuple[list[TestCase], list[TestCase]]


def aoc_runner(
    argv: Sequence[str] | None,
    part1: PartFn,
    part2: PartFn,
    input_file: Path,
    test_cases: TestCases,
) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--part", type=int, default=1)
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args(argv)

    fn = {1: part1, 2: part2}[args.part]

    if args.test:
        table = create_test_result_table()

        for i, (test_data, expected) in enumerate(test_cases[args.part - 1], 1):
            result = fn(test_data)
            add_row(table, i, result, expected)

        console.print(table)
        return 0

    input_data = input_file.read_text().strip()
    print(fn(input_data))

    return 0


def create_test_result_table() -> Table:
    table = Table(title="TEST RESULTS", min_width=80, title_justify="left")
    table.add_column("TEST CASE")
    table.add_column("RESULT", style="cyan")
    table.add_column("EXPECTED", style="yellow")
    table.add_column("PASS")

    return table


def add_row(table: Table, tc: int, actual: int | str, expected: int | str) -> None:
    pass_str = "[green]PASS" if actual == expected else "[red]FAIL"
    table.add_row(str(tc), str(actual), str(expected), pass_str)
