import io

import pytest

from ibidem.advent_of_code.y2022.dec09 import load, part1, part2

TEST1_INPUT = io.StringIO("""\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""")

TEST2_INPUT = io.StringIO("""\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""")

PART1_RESULT = 13
PART2_RESULT = 36


class TestDec09():
    @pytest.fixture
    def input1(self):
        TEST1_INPUT.seek(0)
        return TEST1_INPUT

    @pytest.fixture
    def loaded1(self, input1):
        return load(input1)

    @pytest.fixture
    def input2(self):
        TEST2_INPUT.seek(0)
        return TEST2_INPUT

    @pytest.fixture
    def loaded2(self, input2):
        return load(input2)

    def test_load(self, loaded1):
        steps = list(loaded1)
        assert len(steps) == 24
        assert steps[:8] == ["R", "R", "R", "R", "U", "U", "U", "U"]
        assert steps[-8:] == ["D", "L", "L", "L", "L", "L", "R", "R"]

    def test_part1(self, loaded1):
        result = part1(loaded1)
        assert result == PART1_RESULT

    def test_part2(self, loaded2):
        result = part2(loaded2, with_visual=True)
        assert result == PART2_RESULT
