import pathlib
from typing import Sequence

from tools.runnner import aoc_runner
from tools.runnner import TestCases


def parse(input_str: str) -> tuple:
    ints = list(map(int, input_str.strip()))

    file_locs = {}
    file_sizes = {}
    free = {}

    disk = []
    c = 0
    idx = 0

    for i, v in enumerate(ints):
        if i % 2 == 0:
            file_locs[idx] = c
            for j in range(v):
                disk.append(idx)
                c += 1

            file_sizes[idx] = v
            idx += 1
        else:
            free[c] = v
            for j in range(v):
                disk.append(None)
                c += 1

    max_idx = max(file_locs.keys())  # number of file_locs

    return disk, file_locs, file_sizes, free, max_idx


def part1(input_str: str) -> int:
    disk, *_ = parse(input_str)
    emptys = list(reversed([i for i, v in enumerate(disk) if v is None]))

    # loop backwards through disk
    for i in range(len(disk) - 1, emptys[-1], -1):
        first_none = disk.index(None)
        idx_check = max(i, first_none)
        contig_not_none = all(v is not None for v in disk[:idx_check])

        # print(i, first_none, idx_check, contig_not_none, "".join(str(v) if v is not None else "." for v in disk))

        if contig_not_none:
            break

        if len(emptys) == 0:
            break

        if disk[i] is None:
            continue

        # print(emptys)

        e = emptys.pop()

        disk[e] = disk[i]
        disk[i] = None

    # disk = [v for v in disk if v is not None]
    # print("".join(str(v) if v is not None else "." for v in disk))
    return sum(i * (v or 0) for i, v in enumerate(disk))


def part2(input_str: str) -> int:
    disk, file_locs, file_sizes, free, max_idx = parse(input_str)
    moved = set()
    rounds_no_moves = 0  # number of rounds with no moves - if this gets too high, break

    for i in range(100):
        rounds_no_moves += 1

        # loop through file_locs from right to left
        for idx in range(max_idx, -1, -1):
            if idx in moved:
                continue

            file_start = file_locs[idx]
            file_size = file_sizes[idx]

            # find free blocks from left to right
            free_blocks = sorted(free.keys())
            for free_block in free_blocks:
                # if free block is after file start, skip
                if free_block >= file_start:
                    break

                # if free block is too small, skip
                block_size = free[free_block]
                if block_size < file_size:
                    continue

                # move file
                for j in range(file_size):
                    disk[free_block + j] = idx
                    disk[file_start + j] = None

                # block is exactly the right size, remove it
                if file_size == block_size:
                    del free[free_block]

                # block is larger than file, split it
                else:
                    free[free_block + file_size] = block_size - file_size
                    del free[free_block]

                moved.add(idx)
                rounds_no_moves = 0
                break

        if len(moved) == max_idx + 1:
            break

        # if no moves were made, break
        if rounds_no_moves >= 1:
            break

    else:
        # pass
        raise ValueError("No solution found")

    # check_file_locs(disk, file_sizes)
    return sum(i * (v or 0) for i, v in enumerate(disk))


def check_file_locs(disk: list[int | None], file_sizes: dict[int, int]) -> None:
    i = 0

    while i < len(disk):
        file_idx = disk[i]
        if file_idx is None:
            i += 1
            continue

        file_size = file_sizes[file_idx]

        for j in range(file_size):
            if disk[i + j] != file_idx:
                print("".join(str(v) if v is not None else "." for v in disk))
                raise ValueError(f"File {file_idx} not contiguous")

        if disk[i + file_size] == file_idx:
            print("".join(str(v) if v is not None else "." for v in disk))
            raise ValueError(f"File {file_idx} too long")

        i += file_size


INPUT_FILE = pathlib.Path(__file__).parent / "input.txt"

TEST_DATA = """\
2333133121414131402
"""

TEST_CASES: TestCases = (
    [
        (TEST_DATA, 1928),
    ],
    [
        (TEST_DATA, 2858),
    ],
)


def main(argv: Sequence[str] | None = None) -> int:
    return aoc_runner(argv, part1, part2, INPUT_FILE, TEST_CASES)


if __name__ == "__main__":
    raise SystemExit(main())
