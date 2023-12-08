import io

import pytest

from ibidem.advent_of_code.y2023.dec08 import load, part1, part2

TEST_INPUTS = [
    io.StringIO("""\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""),
    io.StringIO("""\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""")]

PART2_INPUT = io.StringIO("""\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""")


PART1_RESULTS = [2, 6]
PART2_RESULT = 6


class TestDec08():
    @pytest.fixture
    def input(self):
        inputs = []
        for input in TEST_INPUTS:
            input.seek(0)
            inputs.append(input)
        return inputs

    @pytest.fixture
    def loaded(self, input):
        return [load(i) for i in input]

    @pytest.fixture
    def input2(self):
        PART2_INPUT.seek(0)
        return PART2_INPUT

    @pytest.fixture
    def loaded2(self, input2):
        return load(input2)

    def test_load(self, loaded):
        for directions, map in loaded:
            assert isinstance(directions, str)
            assert all(d in "LR" for d in directions)
            assert isinstance(map, dict)
            assert map.get("AAA") is not None

    def test_part1(self, loaded):
        for i, map in enumerate(loaded):
            result = part1(map)
            assert result == PART1_RESULTS[i]

    def test_part2(self, loaded2):
        result = part2(loaded2)
        assert result == PART2_RESULT
