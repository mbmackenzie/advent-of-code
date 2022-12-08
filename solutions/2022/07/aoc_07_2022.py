"""Day 7 of Advent of Code 2022"""
from collections import defaultdict
from pathlib import PurePosixPath as Path


TEST_DATA = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

TEST_CASES = ((TEST_DATA, 95437, 24933642),)


def get_tree(input_str: str) -> tuple[dict[str, int], set[str]]:
    tree: dict[str, int] = defaultdict(int)
    current_path = Path("/")
    all_paths: set[str] = set()

    for line in input_str.splitlines():
        if line.startswith("$ cd "):
            goto = line[5:].strip()
            if goto == "/":
                current_path = Path("/")
            elif goto == "..":
                current_path = current_path.parent
            else:
                current_path = current_path / goto
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("dir "):
            dir_name = line[4:].strip()
            all_paths.add(str(current_path / dir_name))
        else:
            size, name = line.split()
            tree[str(current_path / name)] = int(size)
            all_paths.add(str(current_path))

    return tree, all_paths


def get_directory_sizes(tree: dict[str, int], all_paths: set[str]) -> dict[str, int]:
    total_sizes: dict[str, int] = defaultdict(int)

    for path in all_paths:
        for file, size in tree.items():
            files_path = str(Path(file).parent)
            if files_path.startswith(path):
                total_sizes[path] += size

    return total_sizes


def part1(input_str: str) -> int:
    """Part 1 solution"""

    tree, all_paths = get_tree(input_str)
    folder_sizes = get_directory_sizes(tree, all_paths)

    return sum(filter(lambda x: x <= 100000, folder_sizes.values()))


def part2(input_str: str) -> int:
    """Part 2 solution"""

    TOTAL_DISK_SPACE = 70_000_000
    REQUIRED_SPACE = 30_000_000

    tree, all_paths = get_tree(input_str)
    folder_sizes = get_directory_sizes(tree, all_paths)

    unused = TOTAL_DISK_SPACE - folder_sizes["/"]
    return min(filter(lambda x: (x + unused) >= REQUIRED_SPACE, folder_sizes.values()))


if __name__ == "__main__":
    # print(part1(TEST_DATA))
    print(part2(TEST_DATA))
