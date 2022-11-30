from aoc.input_handler import InputHandler


def test_pop_line() -> None:
    """Test that pop_line removes the first element from content"""
    data = ["A", "B", "C", "D"]
    ih = InputHandler(data)

    first_line = ih.pop_line()
    assert first_line == "A"
    assert ih.content == ["B", "C", "D"]


def test_as_list_no_mutatations() -> None:
    """Test that as_list with no mutate arg returns the data"""
    data = ["A", "B", "C", "D"]
    ih = InputHandler(data)

    assert ih.as_list() == data


def test_as_list_int_mutation() -> None:
    """Test that as_list with mutate=int returns a list of ints"""
    data = ["1", "2", "3", "4"]
    ih = InputHandler(data)

    assert ih.as_list(mutate=int) == [1, 2, 3, 4]
