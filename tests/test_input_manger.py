import os
from pathlib import Path
from tempfile import TemporaryDirectory

import responses

from aoc.input_manager import InputManager

TEST_URL = "https://adventofcode.com/2021/day/1/input"


@responses.activate
def test_download_file_if_no_cache(capsys) -> None:
    responses.add(responses.GET, TEST_URL, body="1,2,3,4,5", status=200)

    with TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        Path(".env").touch()

        InputManager(2021, 1).create_input_file()
        assert capsys.readouterr().out.startswith("Fetching input file")

        input_file = Path("input.txt").read_text()
        assert input_file == "1,2,3,4,5"


@responses.activate
def test_download_file_if_cache(capsys) -> None:
    responses.add(responses.GET, TEST_URL, body="1,2,3,4,5", status=200)

    with TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        Path(".env").touch()

        cached = Path(".aoc_cache/2021-01.txt")
        cached.parent.mkdir(parents=True, exist_ok=True)
        cached.write_text("5,4,3,2,1")

        InputManager(2021, 1).create_input_file()
        assert capsys.readouterr().out.startswith("Using cached input file")

        input_file = Path("input.txt").read_text()
        assert input_file == "5,4,3,2,1"
