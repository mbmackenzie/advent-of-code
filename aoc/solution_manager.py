import os
from pathlib import Path
from typing import Optional

from aoc.helpers import read_asset


def read_solution_template() -> str:
    """Read the template file"""
    return read_asset("solution_template.txt")


def create_dir(dirpath: Path) -> None:
    """Create a directory"""
    if os.path.exists(dirpath):
        return

    os.mkdir(dirpath)


def save_file(filepath: Path, content: Optional[str] = None) -> None:
    """Save the content to disk"""
    if not filepath.parent.exists():
        create_dir(filepath.parent)

    with open(filepath, "w") as f:
        if content:
            f.write(content)


class SolutionManager:
    """Manage the creation of a solution"""

    year: int
    day: int
    name: Optional[str]

    def __init__(self, year: int, day: int, name: Optional[str] = None):
        self.year = year
        self.day = day
        self.name = name

    @property
    def solution_filepath(self) -> Path:
        filepath = os.path.join(f"{self.year}", f"day{self.day:02}.py")
        return Path(filepath)

    @property
    def has_solution_file(self) -> bool:
        """Check if the solution file exists"""
        return self.solution_filepath.exists()

    def create(self) -> "SolutionManager":
        """Create the solution file using the template"""

        if os.path.exists(self.solution_filepath):
            raise FileExistsError()

        template = self._create_solution_template()
        self.create_solution_file(template)
        return self

    def create_solution_file(self, template: str) -> None:
        """Save the solution file"""
        save_file(self.solution_filepath, template)

    def _create_solution_template(self) -> str:
        """Create a template for a solution and return the filepath"""
        template = read_solution_template()
        return self._format_solution_template(template)

    def _format_solution_template(self, template: str) -> str:
        """Format the template for a solution"""

        name = self.name if self.name else ""
        docstring = f"Day {self.day}" + (f": {self.name}" if self.name else "")
        return template.format(
            year=self.year, day=self.day, name=name, docstring=docstring
        )
