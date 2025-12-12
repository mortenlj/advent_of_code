import io

import pytest

from ibidem.advent_of_code.y2022.dec13 import load, part1, part2, compare

TEST_INPUT = io.StringIO("""\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""")

PART1_RESULT = 13
PART2_RESULT = 140


class TestDec13:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 8
        assert all(len(pair) == 2 for pair in loaded)
        assert loaded[0][0] == [1, 1, 3, 1, 1]

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT

    @pytest.mark.parametrize(
        ("pair", "result"),
        (
            ((1, 1), 0),
            ((1, 2), -1),
            ((2, 1), 1),
            (([1], [1]), 0),
            (([1], [2]), -1),
            (([2], [1]), 1),
            (([1], [1, 2]), -1),
            ((1, [1]), 0),
            ((1, [2]), -1),
            ((2, [1]), 1),
        ),
    )
    def test_compare(self, pair, result):
        actual = compare(pair)
        assert actual == result
