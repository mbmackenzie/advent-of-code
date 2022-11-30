"""The abstract solution class"""
from abc import ABC
from abc import abstractmethod
from timeit import timeit as get_best_time
from typing import Any
from typing import Optional

from aoc.input_handler import InputHandler


class SolutionResult:
    """Class for storing the result of a solution."""

    def __init__(
        self, result: Any, time: Optional[float], number: Optional[int]
    ) -> None:
        """Initialize the solution result.

        Parameters
        ----------
        result : Any
            The result of the solution.

        time : Optional[float]
            The time taken to solve the solution.

        number : Optional[int]
            The number of repetitions when calculating the time.
        """
        self.result = result
        self.time = time
        self.number = number

    @property
    def avg_time(self) -> float:
        """Return the average time of execution. Returns -1 if not timing."""
        if not self.time:
            return -1

        time = self.time if self.time else 0
        number = self.number if self.number else 0
        return time / number

    def __str__(self) -> str:
        """Return the string representation of the solution result."""
        return f"{self.result}"

    def __repr__(self) -> str:
        return self.__str__()


class Solution(ABC):
    """Base class for a solution

    This class should be inherited by concrete solutions.
    There are varying functions that must be, and can be implemented.

    You can call the class to create a tuple of results from part one and part two.

    Parameters
    ----------
    year : int
        The year of the problem

    day : int
        The day of the problem

    name : Optional[str], optional
        The fun name of the problem, by default None

    """

    def __init__(self, year: int, day: int, name: str):
        self.year = year
        self.day = day
        self.name = name

        self.input: InputHandler
        self.__data: list[Any]

    @property
    def data(self) -> Any:
        """The data, reformated and mutated"""

        if not self.__data and isinstance(self.__data, list):
            raise ValueError("Data should not be empty")

        return self.__data

    def set_input_data(self, input_data: list[str]) -> None:
        """Reload and reformat the input file.

        Parameters
        ----------
        input_data : list[str]
            The input data as a list of strings.
        """
        self.input = InputHandler(input_data)
        self._pop_lines()
        self._reformat_data()

    def part_one(self) -> int:
        """Set part one data and return part one result.

        Returns
        -------
        result : int
        """
        self.__data = self._get_data_for_part_one()
        return self._part_one()

    def part_two(self) -> int:
        """Set part two data and return part two result.

        Returns
        -------
        result : int
        """
        self.__data = self._get_data_for_part_two()
        return self._part_two()

    @abstractmethod
    def _part_one(self) -> int:
        """Implement part one solution here"""

    @abstractmethod
    def _part_two(self) -> int:
        """Implement part two solution here"""

    def _pop_lines(self) -> None:
        """Remove lines from the beginning of the input data, before any reformatting"""

    def _reformat_data(self) -> None:
        """Change how the input data is formatted BEFORE any mutations."""

    def _get_data(self) -> list[Any]:
        """
        Process the input data to return a list.
        The return default is the input data as a list of strings, delimeted by newlines.
        This function is used to load the data for both part one and two if
        _get_data_for_part_one and _get_data_for_part_two are not implemented.

        You can change the implementation to return a list of whatever you want. For example::

            def _get_data(self) -> list[int]:
                return self.input.as_list(mutate=int)

        See how the solutions.input_reader.InputReader.as_list() method is used to
        process the import data.
        """
        return self.input.as_list()

    def _get_data_for_part_one(self) -> list[Any]:
        """
        Used if you need to have specific input processing for part one.
        See Solution._get_data to understand how to implement.
        """
        return self._get_data()

    def _get_data_for_part_two(self) -> list[Any]:
        """
        Used if you need to have specific input processing for part two.
        See Solution._get_data to understand how to implement.
        """
        return self._get_data()

    def __make_solution_result(
        self, func_name: str, timeit: bool, number: int
    ) -> SolutionResult:
        """Create a solution result.

        Parameters
        ----------
        func_name : str
            part_one or part_two

        timeit : bool
            Should the execution time be measured?

        number : int
            The number of repititions to measure the time.

        Returns
        -------
        SolutionResult
        """
        part_func = getattr(self, f"_{func_name}")
        data_func = getattr(self, f"_get_data_for_{func_name}")

        self.__data = data_func()
        return SolutionResult(
            result=part_func(),
            time=get_best_time(part_func, number=number) if timeit else None,
            number=number,
        )

    def __call__(
        self, timeit: bool = False, number: int = 1000
    ) -> tuple[SolutionResult, SolutionResult]:
        """Convenience function to get both part one and two results.

        Parameters
        ----------
        timeit : bool, optional
            Whether to time the execution of each part, by default False
        number : int, optional
            The number of repititions to time, by default 1000

        Returns
        -------
        tuple[SolutionResult, SolutionResult]
            Part one result, part two result
        """
        return (
            self.__make_solution_result("part_one", timeit, number),
            self.__make_solution_result("part_two", timeit, number),
        )

    def __str__(self) -> str:
        return f"Day {self.day}, {self.year}" + (f" - {self.name}" if self.name else "")
