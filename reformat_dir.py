"""Hacky script to reformat the directory structure of my Advent of Code solutions."""
import argparse
import glob
import os
from typing import Any


def run_command(func: Any, *args: Any, **kwargs: Any) -> None:
    args_str = (
        ", ".join(str(a) for a in args) + ", " + ", ".join(f"{k}={v}" for k, v in kwargs.items())
    )

    print(f"{func.__name__}({args_str})")
    if os.environ.get("DEBUG"):
        return

    func(*args, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.debug or args.dry_run:
        os.environ["DEBUG"] = "1"

    print("STEP 1: Move files to a day sub-directories")
    dirs = glob.glob("20*/")
    for d in dirs:
        files = glob.glob(f"{d}/day*.*")
        for f in files:

            old_path = os.path.split(f)
            day_num = old_path[-1][3:5]

            new_folder = os.path.join(d, day_num)
            if not os.path.exists(new_folder):
                run_command(os.mkdir, new_folder)

            new_path = os.path.join(new_folder, "sol.py")
            run_command(os.rename, f, new_path)

    print("STEP 2: Rename files")
    files = glob.glob("20*/*/sol.py")
    for f in files:
        path = os.path.normpath(f)
        year, day, _ = path.split(os.sep)
        new_name = os.path.join(year, day, f"aoc_{day}_{year}.py")
        run_command(os.rename, f, new_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
