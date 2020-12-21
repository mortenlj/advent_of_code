from unittest.mock import patch

import pytest

from ibidem.advent_of_code.y2020.dec18 import *

EXPRESSIONS = [
    "2 * 3 + (4 * 5)",
    "5 + (8 * 3 + 9 + 3 * 4 * 3)",
    "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
    "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",
]
RESULTS = [26, 437, 12240, 13632]

TEST_HOMEWORK = "\n".join(EXPRESSIONS)
TEST_RESULT = sum(RESULTS)


class TestDec18():
    @pytest.fixture(autouse=True)
    def input(self, tmp_path):
        input_file = tmp_path / "input.txt"
        input_file.write_text(TEST_HOMEWORK)
        with patch("ibidem.advent_of_code.y2020.dec18.get_input_name") as gin:
            gin.return_value = input_file
            yield gin

    def test_load(self):
        homework = load()
        assert len(homework) == 4
        assert [len(g) for g in homework] == [9, 15, 23, 27]

    def test_tokenize_line(self):
        actual = tokenize_line(TEST_HOMEWORK.splitlines(keepends=False)[0])
        assert actual[0].type == tokenize.NUMBER
        assert actual[0].string == "2"
        assert actual[3].type == tokenize.OP
        assert actual[3].string == "+"

    @pytest.mark.parametrize("line, expected", (
            ("2", 2),
            ("2 + 2", 4),
            (EXPRESSIONS[0], RESULTS[0]),
            (EXPRESSIONS[1], RESULTS[1]),
            (EXPRESSIONS[2], RESULTS[2]),
            (EXPRESSIONS[3], RESULTS[3]),
    ))
    def test_solve_expression(self, line, expected):
        expression = tokenize_line(line)
        actual = solve_expression(expression)
        assert actual == expected

    def test_part1(self):
        homework = load()
        actual = part1(homework)
        assert actual == TEST_RESULT
