import io
import pytest

from ibidem.advent_of_code.y2021.dec11 import load, part1, part2, simulate_step

TEST_INPUT = io.StringIO("""\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""")

STEP1 = load(io.StringIO("""\
6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637
"""))

STEP2 = load(io.StringIO("""\
8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848
"""))

PART1_RESULT = 1656
PART2_RESULT = 195


class TestDec11():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded.size_x == 10
        assert loaded.size_y == 10

    def test_simulate_step(self, loaded):
        flashes = simulate_step(loaded)
        assert flashes == 0
        assert loaded == STEP1
        flashes = simulate_step(loaded)
        assert flashes == 35
        assert loaded == STEP2

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT
        
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
