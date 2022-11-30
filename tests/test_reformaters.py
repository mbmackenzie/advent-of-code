from aoc.reformaters import combine_nonblank_lines


def test_combine_nonblank_lines() -> None:
    data = ["A", "B", "C", "", "1", "2", "3"]
    assert combine_nonblank_lines(data, sep="") == ["ABC", "123"]
