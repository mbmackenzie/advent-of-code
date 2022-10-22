import os
import sys
from subprocess import run
from tempfile import TemporaryDirectory
from typing import Optional
from typing import Sequence


def _run_test_cases(
    year: int,
    day: int,
    pytest_args: Optional[Sequence[str]] = None,
) -> None:

    with open("tools/_assets/test_day.txt") as f:
        test_file = f.read()

    with TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, f"aoc{year}_{day:02}.py")

        with open(filename, "w") as f:
            f.write(test_file.format(year=year, day=day))

        pytest_cmd = f"{sys.executable} -m pytest {filename}"
        if pytest_args is not None:
            pytest_cmd += " " + " ".join(pytest_args)

        if os.name == "nt":
            _run_on_windows(tmpdir, pytest_cmd)
        else:
            run(pytest_cmd, shell=True, check=True)


def _run_on_windows(tmpdir: str, pytest_cmd: str) -> None:
    run(f"powershell.exe cd {tmpdir}; {pytest_cmd}", check=True)


if __name__ == "__main__":
    _run_test_cases(2019, 1, ["-vv", "-s"])
