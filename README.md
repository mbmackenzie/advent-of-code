# Advent of Code

https://adventofcode.com

## Solutions

_Example_

| Year | Stars per Language             |
| ---- | ------------------------------ |
| 2020 | `{ "python": 32 , "rust": 0 }` |
| 2019 | `{ "python": 38 , "rust": 0 }` |

## Toolkit

GOAL: A toolkit for testing, running, submitting, and benchmarking solutions in any language.

```bash
(comming soon...) pip install mbm-aoc-toolkit
```

### Initialize your workspace

```bash
aoc init [--username <username> --token <token>]
```

The username and token are optional. If not provided you will be prompted for them, but can also ignore this. The point of these is to connect the solutions to your account's specific input, as well as allow the toolkit to pull data, submit solutions, work with leaderboards, etc...

### Create a new solution

Quickly create a new solution template for a given day, in a given language. This will also download the input for that day if you have provided a username and token.

```bash
aoc new --lang=python --year=2022 --day=1

# or
aoc new --lang=python 01-22 # or any other day-year format
```

If you are going for speed, you can set your preferred language in the config file or with the `config` command. This will be the default language for new solutions. Also note, if you don't provide the year/day it will default to the current day.

```bash
# set default language
aoc config --lang=python
aoc new
```

If you know how you want to parse the data, you can also provide the key for it. This will include the desired parser in the solution template.

```bash
aoc new --lang=python --parser=one_int_per_line

# see available parsers
aoc parsers --lang=python
```

### Testing your solution

```bash
aoc test
```

This will run the tester for the selected day, year, and language. The tester will run the solution against the provided test cases, but not the actual input.

### Running and \[optionally\] benchmarking your solution

```bash
aoc run --timeit
```

This will run the solution for the selected day, year, and language. If you provide the `--timeit` flag, it will also time the solution, and give you benchmarks relative to your other solutions in the same language.

When you know you have a correct solution, save it to benchmark future implementations.

```bash
aoc run --save-correct-answers
```

### Submitting your solution

```bash
aoc submit --part [1|2]
```

Submit the output of your solution to the AoC website. You will be prompted for your token if you have not provided it. You can also provide the `--part` flag, it will default to part 1 if no known answer exists, and then part 2 if an answer for part 1 exists.

### Other fun things: Leaderboards, Personal Stats, etc...

```bash
# pull leaderboard, save it as stats through day 3
aoc leaderboard pull --day=3

# view the leaderboard
aoc leaderboard show --top=3
```

```text
    Advent of Code 2022 - Standings through Day 03
======================================================

Rank  Name                  Stars  Points  Rank Change
----  --------------------  -----  ------  -----------
1     Bob Mackenzie           6      55        ↑ 1
2     Matt Mackenzie          6      54        ↓ 1
3     Jane Mackenzie          6      47        ↑ 4

* Congratulations to Jane Mackenzie for getting points
on the global leaderboard yesterday!
```
