# Advent of Code

## Solutions

https://adventofcode.com

Solution framework: https://github.com/mbmackenzie/advent-of-code-starter

---

## Framework

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

https://adventofcode.com/

A framework for implementing Advent of Code solutions in Python.

## Quick Start

Pip install the project so you have access to the `aoc` command.

```bash
pip install aoc-starter
```

Create an empty directory you want to write your solutions in.

```bash
aoc init
```

Now, you are ready to start implementing your solutions!

```bash
aoc create 01 --year 2021
```

This will create python file, `2021/day01.py`, where you'll implement the solution.

After you've implemented the solution, you can run it with:

```bash
aoc run 01 --year 2021 -i input.txt
```

## Solution Implementation

The file `2021/day01.py` will have a concrete class, `Solution01` that extends the base `Solution` class from `aoc-starter`.

There are a variety of methods that must/can be defined to best implement your solution.

### Part Functions

These are the only abstract methods in the base class and therefore must be implemented.

```python
def _part_one(self) -> int:
    ...

def _part_two(self) -> int:
    ...
```

These functions should return the integer answer to Advent of Code problems. The input data can be accessed using the data property, `self.data`.

### Parsing data

There are three functions you can use to parse the data:

```python
def _get_data(self) -> list[Any]:
    ...

def _get_data_for_part_one(self) -> list[Any]:
    ...

def _get_data_for_part_two(self) -> list[Any]:
    ...
```

The `_get_data` function is the default, so if you don't implement one of the others then `_get_data` is used. If there are differences in how the data should be parsed between each part you can use the more specific functions.

Inside these functions, you need to return the data as a list, down the line this return value is stored in `self.data`.

#### The input handler

The solution base class has a property `input`, that is of type `aoc.InputHandler`. This object is the intermediary between the raw data and the solution. When parsing data, you can use the `self.input.as_list` function to interact with the raw content.

```python
# default, return the content as a list of strings
def _get_data(self) -> list[str]:
    return self.input.as_list()

# parse as a certain type
def _get_data(self) -> list[int]:
    return self.input.as_list(int)

# use a custom parser
def _get_data(self) -> list[tuple[str, int]]:
    def parser(content: str, **kwargs) -> tuple[str, int]:
        key, val = content.split(": ")
        return key, int(val)

    return self.input.as_list(parser)
```

### Reformatting input file

You can use the `_reformat_data` function to change how the input data looks.

### Pop Lines

Sometimes the input file has a line at the beginning that is different from the actual data. The `InputHandler` has a method `pop_line` that removes and returns the first line in raw content. If you want to use this before any reformats happen, you can override the `_pop_lines` method in the solution.

```python
class Day01(Solution):

    first_line: str

    def _pop_lines(self) -> None:
        self.first_line = self.input.pop_line()
```
