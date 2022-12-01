import importlib.util
import os
import sys
from subprocess import run
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import Sequence

from tools.caching import load_cached_data
from tools.parsing import SolutionFunction


def load_solution(year: int, day: int) -> ModuleType:
    spec = importlib.util.spec_from_file_location("solution", f"{year}/day{day:02}.py")

    if spec is None:
        raise ImportError("Could not import solution file.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    return module


def preview_solution(year: int, day: int, raise_errors: bool = False) -> None:

    input_str = load_cached_data(year, day)
    solution = load_solution(year, day)

    for part in (1, 2):

        func: SolutionFunction | None = getattr(solution, f"part{part}", None)

        if func is None:
            raise ImportError(f"Part {part} was not found in module.")

        try:
            result = func(input_str)
            print(f"Part {part}: {result}")
        except NotImplementedError:
            print(f"Part {part}: Not implemented yet")
        except Exception as e:
            print(f"Part {part}: Failed with {e.__class__.__name__}")

            if raise_errors:
                raise


def run_solution_part(year: int, day: int, part: int) -> int:
    input_str = load_cached_data(year, day)
    solution = load_solution(year, day)

    func: SolutionFunction | None = getattr(solution, f"part{part}", None)

    if func is None:
        raise ImportError(f"Part {part} was not found in module.")

    try:
        return func(input_str)
    except Exception:
        raise ValueError(f"Part {part} failed. Use aoc-run to investigate.")


def _run_pytest_on_windows(tmpdir: str, pytest_cmd: str) -> None:
    run(f"powershell.exe cd {tmpdir}; {pytest_cmd}", check=True)


def _run_pytest_on_unix(tmpdir: str, pytest_cmd: str) -> None:
    run(f"cd {tmpdir} && {pytest_cmd}", shell=True, check=True)


def run_test_cases(year: int, day: int, pytest_args: Sequence[str] | None = None) -> None:

    with open("tools/_assets/test_day.txt") as f:
        test_file = f.read()

    with TemporaryDirectory() as tmpdir:
        print(f"Running tests in '{tmpdir}'")
        filename = os.path.abspath(os.path.join(tmpdir, f"aoc{year}_{day:02}.py"))

        with open(filename, "w") as f:
            f.write(test_file.format(year=year, day=day))

        pytest_cmd = f"{sys.executable} -m pytest {os.path.basename(filename)}"
        if pytest_args is not None:
            pytest_cmd += " " + " ".join(pytest_args)

        if os.name == "nt":
            _run_pytest_on_windows(tmpdir, pytest_cmd)
        else:
            _run_pytest_on_unix(tmpdir, pytest_cmd)
