"""Day 7: Handy Haversacks"""
import re

from aoc import Solution


def generic_num_paths_to_target_bag(
    data: list[list[int]], bags: list[str], target: str
) -> int:
    """Generic solution"""
    ends_at_target = [0] * len(bags)
    target_idx = bags.index(target)

    def get_possible_parent_indices(bag_idx: int) -> list[int]:
        parent_counts = [row[bag_idx] for row in data]
        return [i for i, count in enumerate(parent_counts) if count > 0]

    def find_possible_sources(bag_idx: int) -> None:
        possible_parents = get_possible_parent_indices(bag_idx)
        for parent_idx in possible_parents:
            if ends_at_target[parent_idx] != 1:
                ends_at_target[parent_idx] = 1
                find_possible_sources(parent_idx)

    find_possible_sources(target_idx)
    return sum(ends_at_target)


def generic_total_bags_in_target_bag(
    data: list[list[int]], bags: list[str], target: str
) -> int:
    """Generic solution"""
    target_idx = bags.index(target)

    def get_children(parent_idx: int) -> list[int]:
        return [i for i, count in enumerate(data[parent_idx]) if count > 0]

    def get_all_children(parent_idx: int) -> int:
        val = 1  # Count itself
        children = get_children(parent_idx)
        for child_idx in children:
            bag_count = data[parent_idx][child_idx]
            val += bag_count * get_all_children(child_idx)

        return val

    return get_all_children(target_idx) - 1  # don't count the first bag


class Day07(Solution):
    """Solution to day 7 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 7, "Handy Haversacks")

    def _part_one(self) -> int:
        bags, data = self.data
        return generic_num_paths_to_target_bag(data, bags, "shiny gold")

    def _part_two(self) -> int:
        bags, data = self.data
        return generic_total_bags_in_target_bag(data, bags, "shiny gold")

    def _get_data(self) -> tuple[list[str], list[list[int]]]:
        data = self.input.as_list()

        unique_bags = [bag.split(" bags contain ")[0] for bag in data]
        n_unique_bags = len(unique_bags)

        bag_regex = re.compile(r"(\d)\s([\w\s]+)\sbags?")
        return_data = [[0] * n_unique_bags for _ in range(n_unique_bags)]

        for line in data:
            parent_name, child_bags = line[:-1].split(" bags contain ")
            parent_idx = unique_bags.index(parent_name)

            for count, child_name in bag_regex.findall(child_bags):
                child_idx = unique_bags.index(child_name)
                return_data[parent_idx][child_idx] += int(count)

        return unique_bags, return_data
