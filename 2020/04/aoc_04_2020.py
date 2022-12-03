"""Day 4: Passport Processing"""
import re

from aoc import Solution
from aoc.reformaters import combine_nonblank_lines


def is_valid_hgt(hgt: str) -> bool:
    match = re.match(r"^(\d+)(cm|in)$", hgt)

    if not match:
        return False

    return (match[2] == "cm" and 150 <= int(match[1]) <= 193) or (
        match[2] == "in" and 59 <= int(match[1]) <= 76
    )


VALID_PASSPORT_RULES = {
    "byr": lambda x: re.match(r"^\d{4}$", x) and 1920 <= int(x) <= 2002,
    "iyr": lambda x: re.match(r"^\d{4}$", x) and 2010 <= int(x) <= 2020,
    "eyr": lambda x: re.match(r"^\d{4}$", x) and 2020 <= int(x) <= 2030,
    "hgt": is_valid_hgt,
    "hcl": lambda x: re.match(r"^#[a-f0-9]{6}$", x),
    "ecl": lambda x: x in "amb blu brn gry grn hzl oth".split(" "),
    "pid": lambda x: re.match(r"^[0-9]{9}$", x),
}


def parse_passport(item_str: str) -> dict[str, str]:
    item_list = [item.split(":") for item in item_str.split(" ")]
    return {item[0]: item[1] for item in item_list}


class Day04(Solution):
    """Solution to day 4 of the 2020 Advent of Code"""

    def __init__(self) -> None:
        super().__init__(2020, 4, "Passport Processing")

    def _part_one(self) -> int:
        """How many passports are valid?"""

        def is_valid_passport(passport: dict[str, str]) -> bool:
            return all(key in passport for key in VALID_PASSPORT_RULES.keys())

        return sum(is_valid_passport(passport) for passport in self.data)

    def _part_two(self) -> int:
        """How many passports are valid?"""

        def is_valid_passport(passport: dict[str, str]) -> bool:
            for key, validate in VALID_PASSPORT_RULES.items():
                if key not in passport:  # Missing key
                    return False

                if not validate(passport[key]):  # Invalid value
                    return False

            return True

        return sum(is_valid_passport(passport) for passport in self.data)

    def _reformat_data(self) -> None:
        self.input.reformat(combine_nonblank_lines)

    def _get_data(self) -> list[dict[str, str]]:
        return self.input.as_list(parse_passport)


if __name__ == "__main__":
    solution = Day04()
    print(solution())
