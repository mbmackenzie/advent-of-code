from __future__ import annotations

import pathlib
import time
from datetime import datetime
from typing import Literal

import httpx
import typer
from pydantic import BaseModel
from rich import print

CurrentPuzzleFile = pathlib.Path(".current_puzzle")


class Puzzle(BaseModel):
    day: int
    year: int
    part: int

    def save(self) -> None:
        CurrentPuzzleFile.write_text(self.model_dump_json())

    def delete(self) -> None:
        CurrentPuzzleFile.unlink()

    @classmethod
    def load(cls) -> Puzzle | None:
        if not CurrentPuzzleFile.exists():
            return None

        return cls.model_validate_json(CurrentPuzzleFile.read_text())


def get_year() -> int:
    return datetime.now().year


def get_day() -> int:
    return datetime.now().day


def is_december() -> bool:
    return datetime.now().month == 12


def days_until_december() -> int:
    dec1 = datetime(datetime.now().year, 12, 1)
    today = datetime.now()

    if today.month == 12:
        return 0

    return (dec1 - today).days


class PuzzleError(Exception):
    pass


def get_puzzle(
    current: Puzzle | None,
    day: int | None,
    year: int | None,
    part: int | None = None,
    next: bool = False,
) -> Puzzle:
    if current:
        if day:
            current.day = day

        if year:
            current.year = year

        if part:
            current.part = part

        return current

    if part is None:
        part = 1

    if not is_december():
        if next:
            return Puzzle(day=1, year=get_year(), part=part)

        if not day:
            print("[red]'day' is required if it's not December!", end=" ")
            print(f"[green]🎄 Only {days_until_december()} days more to go! 🎄")
            raise typer.Exit()

    if next:
        return Puzzle(day=get_day() + 1, year=get_year(), part=part)

    if not day:
        day = get_day()

    if not year:
        year = get_year()
        if not is_december():
            year -= 1
            print(f"[yellow]It's not December yet! Using previous year: {year}")

    return Puzzle(day=day, year=year, part=part)


def read_token() -> str:
    token_path = pathlib.Path(".token")

    if not token_path.exists():
        raise FileNotFoundError("Token not found!")

    return token_path.read_text().strip()


def get_headers(token: str) -> dict[str, str]:
    return {
        "Cookie": f"session={token}",
        "User-Agent": "Matt Mackenzie, @mbmackenzie on GitHub",
    }


def fetch_input(day: int, year: int, token: str) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = get_headers(token)
    response = httpx.get(url, headers=headers).raise_for_status()
    return response.text


def try_fetch_input(day: int, year: int, token: str, attempts: int = 3, delay: int = 5) -> str:
    for i in range(attempts):
        try:
            return fetch_input(day, year, token)
        except Exception as e:
            print(f"Failed to fetch input: {e}")
            print(f"Attempt {i + 1} of {attempts}.. Retrying in {delay} seconds..")
            time.sleep(delay)

    raise Exception(f"Failed to fetch input after {attempts} attempts!")


Status = Literal["Correct", "Incorrect", "Already completed", "Please wait"]

CORRECT = "That's the right answer!"
INCORRECT = "That's not the right answer"
PLEASE_WAIT = "You gave an answer too recently"
ALREADY_COMPLETED = "Did you already complete it?"


def correct(response: str) -> bool:
    return CORRECT in response


def incorrect(response: str) -> bool:
    return INCORRECT in response


def already_completed(response: str) -> bool:
    return ALREADY_COMPLETED in response


def please_wait(response: str) -> bool:
    return PLEASE_WAIT in response


def submit_answer(day: int, year: int, token: str, part: int, answer: str) -> Status:
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    headers = get_headers(token)

    data = {
        "level": part,
        "answer": answer,
    }

    response = httpx.post(url, headers=headers, data=data).raise_for_status()

    if correct(response.text):
        return "Correct"

    if incorrect(response.text):
        return "Incorrect"

    if already_completed(response.text):
        return "Already completed"

    if please_wait(response.text):
        return "Please wait"

    raise Exception(f"Unknown response! {response.text}")
