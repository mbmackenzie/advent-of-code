import pytest
from tools.main import _get_parser


@pytest.mark.parametrize(
    "input, day, year, day_year",
    [
        (None, None, None, None),
        (["-d", "1"], 1, None, None),
        (["-y", "2020"], None, 2020, None),
        (["-d", "1", "-y", "2020"], 1, 2020, None),
        (["01-2020"], None, None, "01-2020"),
        (["01-20"], None, None, "01-20"),
    ],
)
def test_get_parser(input, day, year, day_year):
    parser = _get_parser()
    args = parser.parse_args(input)

    assert args.day == day
    assert args.year == year
    assert args.day_year == day_year
