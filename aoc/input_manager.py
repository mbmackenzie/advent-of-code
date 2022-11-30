import pathlib

import requests


class InputManager:
    def __init__(self, year: int, day: int):
        self.year = year
        self.day = day

        self.cache_dir = pathlib.Path(".aoc_cache")
        self.cache_dir.mkdir(exist_ok=True)

        self.cache_file = self.cache_dir / f"{year}-{day:02}.txt"

    def create_input_file(self) -> None:
        if self.cache_file.exists():
            print(f"Using cached input file: ./{self.cache_file}")
            data = self.cache_file.read_text()
        else:
            print("Fetching input file from adventofcode.com!")
            data = self.__make_request()
            self.cache_file.write_text(data)

        pathlib.Path("input.txt").write_text(data)

    def __make_request(self) -> str:
        session_cookie = pathlib.Path(".env").read_text().strip()
        session_header = {"Cookie": f"session={session_cookie}"}
        url = f"https://adventofcode.com/{self.year}/day/{self.day}/input"

        return requests.get(url, headers=session_header).text
