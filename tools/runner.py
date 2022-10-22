import importlib.util
from dataclasses import dataclass
from types import ModuleType
from typing import Callable
from typing import Iterable
from typing import Optional

from tools.caching import _load_cached_data


PartFuncion = Callable[[str], int]


@dataclass
class TestCase:
    input_str: str
    part1: Optional[int]
    part2: Optional[int]


def load_solution(year: int, day: int) -> ModuleType:
    spec = importlib.util.spec_from_file_location("aoc.solution", f"{year}/day{day:02}.py")

    if spec is None:
        raise ImportError("Could not import solution file.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    return module


def _run_solution(year: int, day: int, parts: Iterable[str]) -> None:

    for part in parts:
        solution = load_solution(year, day)
        func = getattr(solution, f"part{part}")

        input_str = _load_cached_data(year, day)
        result = func(input_str)

        print(f"Part {part} result: {result}")
