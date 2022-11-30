from typing import Any
from typing import Callable
from typing import Optional

from mypy_extensions import KwArg

MutateFunction = Callable[[str, KwArg()], Any]
FormatterFunction = Callable[[list[str], KwArg()], list[str]]


class InputHandler:
    """Class to reformat and mutate input data"""

    def __init__(self, input_data: list[str]):
        self.__content = [x.strip() for x in input_data]

    @property
    def content(self) -> list[str]:
        return self.__content

    def pop_line(self) -> str:
        """Remove the first element of the content list and return it"""
        item = self.__content.pop(0)

        while self.__content[0] == "":
            self.__content.pop(0)

        return item

    def as_list(
        self, mutate: Optional[MutateFunction] = None, **kwargs: Any
    ) -> list[Any]:
        """Mutate each element in the input list

        Parameters
        ----------
        mutate : Callable[[str, ...], Any], optional
            A function to apply to each element, by default None

        Returns
        -------
        list[Any]
            The mutated data
        """
        if not mutate:
            return self.content

        return [mutate(x, **kwargs) for x in self.content]

    def reformat(self, formater: FormatterFunction, **kwargs: Optional[Any]) -> None:
        """Change the format of the input data

        You might want to do this if the original list of strings from the input data
        doesn't lend itself to the desired format. For example, if the input data is
        has groups of lines that should be together, but are seperated by newlines,
        you can reformat the data to make each group a single element in the list.

        See `aoc.reformaters`

        Parameters
        ----------
        formater : Callable[[list[str], ...], list[str]]
            A function that takes a list of strings and returns a new list of strings.
        """
        if self.__content:
            self.__content = formater(self.content, **kwargs)
