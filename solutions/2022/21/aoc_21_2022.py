"""Day 21 of Advent of Code 2022"""


TEST_DATA = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

"""
pppw = (cczh / lfqf)
     = (sllz + lgvd) / 4
     = (4 + (ljgn * ptdq)) / 4
     = (4 + (2 * (humn - dvpt))) / 4
     = (4 + (2 * (humn - 3))) / 4 = 150

==> 4 + (2 * (humn - 3)) = 600
==> 2 * (humn - 3) = 596
==> humn - 3 = 298
==> humn = 301
"""

TEST_CASES = ((TEST_DATA, None, None),)


def parse_input(input_str: str) -> dict[str, int | tuple[str, str, str]]:
    """Parse the input"""
    monkeyz: dict[str, int | tuple[str, str, str]] = dict()

    for line in input_str.splitlines():
        name, value = line.split(":")
        if value.strip().isdigit():
            monkeyz[name] = int(value)
        else:
            left, opp, right = value.split()
            monkeyz[name] = (left, right, opp)

    return monkeyz


def part1(input_str: str) -> int:
    """Part 1 solution"""

    monkeyz = parse_input(input_str)

    while any(isinstance(value, tuple) for value in monkeyz.values()):
        for name, value in monkeyz.items():
            if not isinstance(value, tuple):
                continue

            left, right, opp = value

            left_monkey_val = monkeyz[left]
            right_monkey_val = monkeyz[right]

            if isinstance(left_monkey_val, int) and isinstance(right_monkey_val, int):
                if opp == "+":
                    monkeyz[name] = left_monkey_val + right_monkey_val
                elif opp == "-":
                    monkeyz[name] = left_monkey_val - right_monkey_val
                elif opp == "*":
                    monkeyz[name] = left_monkey_val * right_monkey_val
                elif opp == "/":
                    monkeyz[name] = left_monkey_val // right_monkey_val
                elif opp == "=":
                    continue
                else:
                    raise ValueError(f"Invalid opp: {opp}")

    assert isinstance(monkeyz["root"], int)
    return monkeyz["root"]


def get_submonkeyz(monkeyz: dict[str, int | tuple[str, str, str]], name: str) -> list[str]:

    submonkeyz = [name]

    stack = [name]
    while stack:
        name = stack.pop()
        value = monkeyz[name]

        if isinstance(value, int):
            submonkeyz.append(name)
            continue

        left, right, _ = value
        submonkeyz.append(left)
        submonkeyz.append(right)

        stack.append(left)
        stack.append(right)

    return submonkeyz


def get_what_monkey_yells(
    monkeyz: dict[str, int | tuple[str, str, str]],
    final_monkey: str,
) -> int:

    while any(isinstance(value, tuple) for value in monkeyz.values()):
        for name, value in monkeyz.items():
            if not isinstance(value, tuple):
                continue

            left, right, opp = value

            left_monkey_val = monkeyz[left]
            right_monkey_val = monkeyz[right]

            if isinstance(left_monkey_val, int) and isinstance(right_monkey_val, int):
                if opp == "+":
                    monkeyz[name] = left_monkey_val + right_monkey_val
                elif opp == "-":
                    monkeyz[name] = left_monkey_val - right_monkey_val
                elif opp == "*":
                    monkeyz[name] = left_monkey_val * right_monkey_val
                elif opp == "/":
                    monkeyz[name] = left_monkey_val // right_monkey_val
                else:
                    raise ValueError(f"Invalid opp: {opp}")

    assert isinstance(monkeyz[final_monkey], int)
    return monkeyz[final_monkey]


from copy import deepcopy


def part2(input_str: str) -> int:
    """Part 2 solution"""

    monkeyz = parse_input(input_str)

    root_val = monkeyz["root"]
    assert isinstance(root_val, tuple)
    monkeyz["root"] = (root_val[0], root_val[1], "=")

    me = "humn"
    monkeyz[me] = -1

    left_submonkeys = get_submonkeyz(monkeyz, root_val[0])
    right_submonkeys = get_submonkeyz(monkeyz, root_val[1])

    if me in left_submonkeys:
        known_monkey = root_val[1]
        known_monkeyz = {k: v for k, v in monkeyz.items() if k in right_submonkeys}

        unknown_submonkeys = left_submonkeys
        unknown_monkey = root_val[0]
        unknown_monkeyz = {k: v for k, v in monkeyz.items() if k in left_submonkeys}

    else:
        known_monkey = root_val[0]
        known_monkeyz = {k: v for k, v in monkeyz.items() if k in left_submonkeys}

        unknown_submonkeys = right_submonkeys
        unknown_monkey = root_val[1]
        unknown_monkeyz = {k: v for k, v in monkeyz.items() if k in right_submonkeys}

    known_monkey_yells = get_what_monkey_yells(known_monkeyz, known_monkey)

    expression = []
    level = 0

    stack = [(unknown_monkey, [])]
    while stack:
        name, expression_level = stack.pop()
        value = unknown_monkeyz[name]

        if isinstance(value, int):
            expression_traversal = expression
            for lvl in expression_level[:-1]:
                expression_traversal = expression_traversal[lvl]

            expression_traversal[expression_level[-1]] = value
            continue

        left, right, opp = value

        expression_traversal = expression
        for lvl in expression_level:
            expression_traversal = expression_traversal[lvl]

        expression_traversal.append([])
        expression_traversal.append(opp)
        expression_traversal.append([])

        stack.append((left, expression_level + [0]))
        stack.append((right, expression_level + [2]))

    old_expression = deepcopy(expression)

    while True:

        stack = [[]]
        while stack:
            expression_level = stack.pop()

            expression_traversal = expression
            for lvl in expression_level:
                expression_traversal = expression_traversal[lvl]

            if isinstance(expression_traversal, int):
                continue

            elif (
                len(expression_traversal) == 3
                and isinstance(expression_traversal[0], int)
                and isinstance(expression_traversal[2], int)
                and all(x >= 0 for x in (expression_traversal[0], expression_traversal[2]))
            ):
                left, opp, right = expression_traversal

                if opp == "+":
                    new_value = left + right
                elif opp == "-":
                    new_value = left - right
                elif opp == "*":
                    new_value = left * right
                elif opp == "/":
                    new_value = left // right

                expression_reset = expression
                for lvl in expression_level[:-1]:
                    expression_reset = expression_reset[lvl]

                expression_reset[expression_level[-1]] = new_value

            else:

                stack.append((expression_level + [0]))
                stack.append((expression_level + [2]))

        if expression == old_expression:
            break

        old_expression = deepcopy(expression)

    while expression != -1:

        left, opp, right = expression

        if not (isinstance(left, int) or isinstance(right, int)):
            raise ValueError(f"Invalid expression: {expression}")

        if isinstance(left, int) and left != -1:
            val = left
            expression = right
        elif isinstance(right, int) or right != -1:
            val = right
            expression = left

        if opp == "+":
            known_monkey_yells -= val
        elif opp == "-" and left == val:
            known_monkey_yells -= val
            known_monkey_yells *= -1
        elif opp == "-" and right == val:
            known_monkey_yells += val
        elif opp == "*":
            known_monkey_yells //= val
        elif opp == "/":
            known_monkey_yells *= val

    we_yell = known_monkey_yells

    print(f"\nWe ({me}) yell:              {we_yell}")

    print(
        f"Known monkey ({known_monkey}) yells:  ",
        get_what_monkey_yells(known_monkeyz, known_monkey),
    )

    unknown_monkeyz[me] = we_yell
    print(
        f"UnKnown monkey ({unknown_monkey}) yells:",
        get_what_monkey_yells(unknown_monkeyz, unknown_monkey),
    )
    print()

    return we_yell


if __name__ == "__main__":
    # print(part1(TEST_DATA))
    print(part2(TEST_DATA))
    pass
