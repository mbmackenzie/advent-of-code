from functools import wraps
from typing import Any
from typing import Protocol


class SolutionFunction(Protocol):
    def __call__(self, input_str: str, testing: bool = False) -> int:
        ...


class PreParsedFunction(Protocol):
    def __call__(self, data: Any, testing: bool = False) -> int:
        ...


def _delimited_ints(input_str: str, delimiter: str) -> list[int]:
    return [int(num.strip()) for num in input_str.split(delimiter) if num]


def delimited_ints(func: PreParsedFunction, delimiter: str) -> SolutionFunction:
    @wraps(func)
    def wrapper(input_str: str, testing: bool = False) -> int:
        return func(_delimited_ints(input_str, delimiter), testing=testing)

    return wrapper


def line_separated_ints(func: PreParsedFunction) -> SolutionFunction:
    @wraps(func)
    def wrapper(input_str: str, testing: bool = False) -> int:
        return func(_delimited_ints(input_str, "\n"), testing=testing)

    return wrapper


def comma_separated_ints(func: PreParsedFunction) -> SolutionFunction:
    @wraps(func)
    def wrapper(input_str: str, testing: bool = False) -> int:
        return func(_delimited_ints(input_str, ","), testing=testing)

    return wrapper
