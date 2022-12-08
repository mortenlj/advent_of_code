import io

import pytest

from ibidem.advent_of_code.y2022.dec05 import load, part1, part2, Move

TEST_INPUT = io.StringIO("""\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""")

PART1_RESULT = "CMZ"
PART2_RESULT = "MCD"


class TestDec05():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    @pytest.mark.parametrize(["line", "count", "source", "target"], (
            ("move 1 from 1 to 1", 1, 1, 1),
            ("move 2 from 2 to 1", 2, 2, 1),
            ("move 3 from 1 to 2", 3, 1, 2),
    ))
    def test_move(self, line, count, source, target):
        move = Move(line)
        assert move.count == count
        assert move.source == source
        assert move.target == target

    def test_load(self, loaded):
        assert len(loaded.moves) == 4
        assert len(loaded.stacks) == 3
        assert loaded.top() == "NDP"

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
