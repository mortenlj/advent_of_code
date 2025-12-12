import io
import textwrap
from collections import namedtuple

import pytest

from ibidem.advent_of_code.y2024.dec09 import load, part1, part2, Disk

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(1928, 2858, io.StringIO(textwrap.dedent("2333133121414131402"))),
]


class TestDec09:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded: Disk):
        assert len(loaded.files) == 10
        assert len(loaded.free_blocks) == 14
        assert len(loaded.used_blocks) == 28
        assert loaded.files[0].blocks == [0, 1]
        assert loaded.files[1].blocks == [5, 6, 7]
        assert all(v in loaded.free_blocks for v in (2, 3, 4, 8, 9, 10))

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
