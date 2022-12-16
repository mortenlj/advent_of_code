import io

import pytest

from ibidem.advent_of_code.y2022.dec15 import load, part1, part2, remove

TEST_INPUT = io.StringIO("""\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""")

PART1_RESULT = 26
PART2_RESULT = 56000011


class TestDec15():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 14
        assert all(len(p) == 2 for p in loaded)
        assert all(all(len(x) == 2 for x in p) for p in loaded)
        assert loaded[0][0][0] == 2
        assert loaded[0][0][1] == 18
        assert loaded[0][1][0] == -2
        assert loaded[0][1][1] == 15

    def test_part1(self, loaded):
        result = part1(loaded, depth=10)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded, max=20)
        assert result == PART2_RESULT

    @pytest.mark.parametrize("cut, expected", (
            ((0, 4), [(5, 15)]),
            ((0, 5), [(6, 15)]),
            ((0, 6), [(7, 15)]),
            ((14, 20), [(5, 13)]),
            ((15, 20), [(5, 14)]),
            ((16, 20), [(5, 15)]),
            ((7, 10), [(5, 6), (11, 15)]),
            ((4, 16), []),
            ((4, 10), [(11, 15)]),
            ((5, 10), [(11, 15)]),
            ((6, 10), [(5, 5), (11, 15)]),
            ((10, 16), [(5, 9)]),
            ((10, 15), [(5, 9)]),
            ((10, 14), [(5, 9), (15, 15)]),
    ))
    def test_remove_single(self, cut, expected):
        line = [(5, 15)]
        actual = remove(line, cut)
        assert actual == expected

    @pytest.mark.parametrize("cut, expected", (
            ((0, 4), [(5, 10), (15, 20)]),
            ((0, 5), [(6, 10), (15, 20)]),
            ((0, 6), [(7, 10), (15, 20)]),
            ((14, 20), [(5, 10)]),
            ((15, 20), [(5, 10)]),
            ((16, 20), [(5, 10), (15, 15)]),
            ((7, 10), [(5, 6), (15, 20)]),
            ((4, 16), [(17, 20)]),
            ((4, 10), [(15, 20)]),
            ((5, 10), [(15, 20)]),
            ((6, 10), [(5, 5), (15, 20)]),
            ((10, 16), [(5, 9), (17, 20)]),
            ((10, 15), [(5, 9), (16, 20)]),
            ((10, 14), [(5, 9), (15, 20)]),
            ((0, 20), []),
    ))
    def test_remove_multi(self, cut, expected):
        line = [(5, 10), (15, 20)]
        actual = remove(line, cut)
        assert actual == expected
