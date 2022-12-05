import argparse
from typing import Sequence

import importlib_metadata


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aoc")

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {importlib_metadata.version('advent_of_code')}",
    )

    args = parser.parse_args(argv)
    print(args)
    # subparsers = parser.add_subparsers(dest="command")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
