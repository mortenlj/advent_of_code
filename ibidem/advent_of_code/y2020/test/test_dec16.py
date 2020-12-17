from unittest.mock import patch

import pytest

from ibidem.advent_of_code.y2020.dec16 import *

INPUT = """\
class: 1-3 or 5-7
seat row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

RULES = [
    Input("class", Range(0, 1), Range(4, 19)),
    Input("row", Range(0, 5), Range(8, 19)),
    Input("seat", Range(0, 13), Range(16, 19)),
]

NEARBY = np.array([
    [3, 9, 18],
    [15, 1, 5],
    [20, 0, 0],
    [5, 14, 9],
    [19, 19, 19],
    [0, 0, 0],
    [8, 4, 16],
    [0, 20, 0],
    [5, 1, 13],
    [0, 0, 20],
])


class TestDec16():
    @pytest.fixture(autouse=True)
    def input_data(self, tmp_path):
        input_file = tmp_path / "input.txt"
        input_file.write_text(INPUT)
        with patch("ibidem.advent_of_code.y2020.dec16.get_input_name") as gin:
            gin.return_value = input_file
            yield gin

    def test_load(self):
        input = load()
        assert len(input.field_rules) == 3
        assert input.your_ticket == [7, 1, 14]
        assert input.nearby_tickets[0] == [7, 3, 47]
        assert input.nearby_tickets[-1] == [38, 6, 12]
        assert len(input.nearby_tickets) == 4

    def test_part1(self):
        input = load()
        result = part1(input)
        assert result == 71

    def test_find_field_order(self):
        invalid, results = find_invalid(RULES, NEARBY)
        order = find_field_order(RULES, invalid, results, 3)
        assert order["row"] == 0
        assert order["class"] == 1
        assert order["seat"] == 2
        assert len(order) == 3
