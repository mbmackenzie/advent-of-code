from functools import wraps
from typing import Any
from typing import Protocol


class SolutionFunction(Protocol):
    def __call__(self, input_str: str) -> int:
        ...


class PreParsedFunction(Protocol):
    def __call__(self, data: Any) -> int:
        ...


class Parser(Protocol):
    def __call__(self, func: PreParsedFunction) -> SolutionFunction:
        ...


def _delimited_ints(input_str: str, delimiter: str) -> list[int]:
    return [int(num.strip()) for num in input_str.split(delimiter) if num]


def delimited_ints(delimiter: str) -> Parser:
    def decorator(func: PreParsedFunction) -> SolutionFunction:
        @wraps(func)
        def wrapper(input_str: str) -> int:
            return func(_delimited_ints(input_str, delimiter))

        return wrapper

    return decorator


def line_separated_ints(func: PreParsedFunction) -> SolutionFunction:
    @wraps(func)
    def wrapper(input_str: str) -> int:
        return func(_delimited_ints(input_str, "\n"))

    return wrapper


def comma_separated_ints(func: PreParsedFunction) -> SolutionFunction:
    @wraps(func)
    def wrapper(input_str: str) -> int:
        return func(_delimited_ints(input_str, ","))

    return wrapper


def split_lines(func: PreParsedFunction) -> SolutionFunction:
    @wraps(func)
    def wrapper(input_str: str) -> int:
        return func(input_str.splitlines())

    return wrapper


def group_lines(lines_per_group: int, split_groups: bool = False) -> Parser:
    def decorator(func: PreParsedFunction) -> SolutionFunction:
        @wraps(func)
        def wrapper(input_str: str) -> int:
            lines = input_str.splitlines()
            groups = list(zip(*[iter(lines)] * lines_per_group))

            if not split_groups:
                return func(["\n".join(group) for group in groups])

            return func(list(groups))

        return wrapper

    return decorator
