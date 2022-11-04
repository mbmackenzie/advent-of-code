from functools import wraps
from typing import Any
from typing import Protocol


class SolutionFunction(Protocol):
    def __call__(self, input_str: str, testing: bool = False) -> int:
        ...


class PreParsedFunction(Protocol):
    def __call__(self, data: Any, testing: bool = False) -> int:
        ...


def int_per_row(func: PreParsedFunction) -> SolutionFunction:
    @wraps(func)
    def wrapper(input_str: str, testing: bool = False) -> int:
        transformed = [int(row.strip()) for row in input_str.splitlines() if row]
        return func(transformed, testing=testing)

    return wrapper


def comma_separated_ints(func: PreParsedFunction) -> SolutionFunction:
    @wraps(func)
    def wrapper(input_str: str, testing: bool = False) -> int:
        transformed = [int(num.strip()) for num in input_str.split(",") if num]
        return func(transformed, testing=testing)

    return wrapper
