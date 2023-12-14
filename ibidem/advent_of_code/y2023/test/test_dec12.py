import io

import pytest

from ibidem.advent_of_code.y2023.dec12 import load, part1, part2, arrangements, unfold

TEST_INPUT = io.StringIO("""\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""")

PART1_RESULT = 21
PART2_RESULT = 525152


class TestDec12():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        for row, groups in loaded:
            assert isinstance(row, str)
            assert isinstance(groups, tuple)
            assert all(isinstance(i, int) for i in groups)

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    @pytest.mark.skip(reason="Takes too long")
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT

    @pytest.mark.parametrize("maprow,groups,expected", [
        ("???.###", (1, 1, 3), 1),
        (".??..??...?##.", (1, 1, 3), 4),
        ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
        ("????.#...#...", (4, 1, 1), 1),
        ("????.######..#####.", (1, 6, 5), 4),
        ("?###????????", (3, 2, 1), 10),
    ])
    def test_arrangements(self, maprow, groups, expected):
        actual = arrangements(maprow, groups)
        assert actual == expected

    @pytest.mark.parametrize("maprow,groups,expected_row,expected_groups", [
        (".#", (1,), ".#?.#?.#?.#?.#", (1, 1, 1, 1, 1)),
        ("???.###", (1, 1, 3), "???.###????.###????.###????.###????.###", (1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3))
    ])
    def test_unfold(self, maprow, groups, expected_row, expected_groups):
        actual_row, actual_groups = unfold(maprow, groups)
        assert actual_row == expected_row
        assert actual_groups == expected_groups
