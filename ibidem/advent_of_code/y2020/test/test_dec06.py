from unittest.mock import patch

import pytest

from ibidem.advent_of_code.y2020.dec06 import load1, load2, part1, part2

GROUPS = """\
abc

a
b
c

ab
ac

a
a
a
a

b
"""


class TestDec06:
    @pytest.fixture
    def input(self, tmp_path):
        input_file = tmp_path / "input.txt"
        input_file.write_text(GROUPS)
        with patch("ibidem.advent_of_code.y2020.dec06.get_input_name") as gin:
            gin.return_value = input_file
            yield gin

    def test_load1(self, input):
        groups = load1()
        assert len(groups) == 5
        assert [len(g) for g in groups] == [3, 3, 3, 1, 1]

    def test_part1(self, input):
        assert part1() == 11

    def test_load2(self, input):
        groups = load2()
        assert len(groups) == 5
        assert [len(g) for g in groups] == [26 - 3, 26 - 0, 26 - 1, 26 - 1, 26 - 1]

    def test_part2(self, input):
        assert part2() == 6
