import re
from enum import auto
from enum import Enum
from typing import Pattern


class Response(Enum):
    CORRECT_ANSWER = auto(), re.compile(r"That's the right answer")
    INCORRECT_ANSWER = auto(), re.compile(r"That's not the right answer")
    NOT_UNLOCKED_YET = auto(), re.compile(r"Please don't repeatedly request this endpoint")
    TOO_FREQUENT = auto(), re.compile(r"gave an answer too recently.*You have (?P<time>\d+)s left")
    ALREADY_ANSWERED = auto(), re.compile(r"Did you already complete it")

    def __init__(self, value: auto, regex: Pattern[str]) -> None:
        self._value_: auto = value
        self._regex_: Pattern[str] = regex

    @property
    def regex(self) -> Pattern[str]:
        """Return the regex"""
        return self._regex_
