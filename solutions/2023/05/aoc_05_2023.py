"""Day 5 of Advent of Code 2023"""
from typing import NamedTuple


TEST_DATA = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

TEST_CASES = ((TEST_DATA, 35, 46),)


class SeedGroup(NamedTuple):
    start: int
    offset: int

    @property
    def upper(self) -> int:
        # inclusive
        return self.start + self.offset - 1

    @property
    def lower(self) -> int:
        return self.start


class MapValues(NamedTuple):
    dest: int
    source: int
    offset: int

    @property
    def source_upper(self) -> int:
        return self.source + self.offset - 1

    @property
    def source_lower(self) -> int:
        return self.source

    def map_to_dest(self, value: int) -> int:
        return self.dest + (value - self.source)

    def check_in_range(self, value: int) -> bool:
        return self.source_lower <= value <= self.source_upper


class Map(NamedTuple):
    name: str
    maps: list[MapValues]

    def get_mapping(self, value: int) -> int:
        for map_values in self.maps:
            if map_values.check_in_range(value):
                return map_values.map_to_dest(value)

        return value

    def map_group(self, seed_group: SeedGroup) -> list[int]:
        seeds = [seed_group]

        needs_mapping = []
        already_mapped = []

        for m in self.maps:
            for s in seeds:
                good, bad = do_mapping(s, m)

                needs_mapping.extend(bad)
                already_mapped.extend(good)

            seeds = needs_mapping
            needs_mapping = []

        already_mapped.extend(seeds)
        return already_mapped


def do_mapping(s: SeedGroup, m: MapValues) -> list[SeedGroup]:
    needs_mapping = []
    already_mapped = []

    # CASE 1: Seed is completely outside of the range
    if s.upper < m.source_lower or s.lower > m.source_upper:
        needs_mapping.append(s)

    # CASE 2: Seed is completely inside of the range
    elif m.source_lower <= s.lower <= s.upper <= m.source_upper:
        already_mapped.append(SeedGroup(m.map_to_dest(s.lower), s.offset))

    # CASE 3: Seed is partially inside of the range on the left
    elif m.source_lower <= s.lower <= m.source_upper <= s.upper:
        # inside on the left, gets mapped
        left = SeedGroup(m.map_to_dest(s.lower), m.source_upper - s.lower + 1)
        already_mapped.append(left)

        # outside map on the right, continues
        right = SeedGroup(m.source_upper + 1, s.upper - m.source_upper)
        needs_mapping.append(right)

    # CASE 4: Seed is partially inside of the range on the right
    elif s.lower <= m.source_lower <= s.upper <= m.source_upper:
        # outside on the left, continues
        left = SeedGroup(s.lower, m.source_lower - s.lower)
        needs_mapping.append(left)

        # inside on the right, gets mapped
        right = SeedGroup(m.map_to_dest(m.source_lower), s.upper - m.source_lower + 1)
        already_mapped.append(right)

    # CASE 5: Map is completely inside of the seed range
    elif s.lower <= m.source_lower <= m.source_upper <= s.upper:
        # outside on the left, continues
        left = SeedGroup(s.lower - 1, m.source_lower - s.lower)
        needs_mapping.append(left)

        # inside the map, gets mapped
        middle = SeedGroup(m.map_to_dest(m.source_lower), m.offset)
        already_mapped.append(middle)

        # outside on the right, continues
        right = SeedGroup(m.source_upper + 1, s.upper - m.source_upper)
        needs_mapping.append(right)

    else:
        raise ValueError("Something else happened...?")

    return already_mapped, needs_mapping


def parse_input(input_str: str) -> tuple[list[int], list[Map]]:
    """Parse input into a list of seeds and a list of maps"""

    lines = input_str.splitlines()

    seeds = [int(c) for c in lines.pop(0).split()[1:]]
    lines.pop(0)

    maps = []
    for grp in "\n".join(lines).split("\n\n"):
        grp_lines = grp.splitlines()
        map_name = grp_lines.pop(0).split()[0]

        map_values = []
        for line in grp_lines:
            map_values.append(MapValues(*[int(c) for c in line.split()]))

        maps.append(Map(map_name, map_values))

    return seeds, maps


def part1(input_str: str) -> int:
    """Part 1 solution"""

    seeds, maps = parse_input(input_str)

    min_map = float("inf")

    for seed in seeds:
        for m in maps:
            seed = m.get_mapping(seed)

        min_map = min(min_map, seed)

    return min_map


def part2(input_str: str) -> int:
    """Part 2 solution"""
    seeds, maps = parse_input(input_str)

    seed_grps = []
    for num1, num2 in zip(seeds[::2], seeds[1::2]):
        seed_grps.append(SeedGroup(num1, num2))

    new_seed_grps = []

    for m in maps:
        for grp in seed_grps:
            new_seed_grps.extend(m.map_group(grp))

        seed_grps = new_seed_grps
        new_seed_grps = []

    return min(seed_grps, key=lambda x: x.start).start


if __name__ == "__main__":
    print(part1(TEST_DATA))
    print(part2(TEST_DATA))
