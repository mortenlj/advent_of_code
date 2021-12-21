import io

import pytest

from ibidem.advent_of_code.y2021.dec21 import load, part1, part2, Player, move

TEST_INPUT = io.StringIO("""\
Player 1 starting position: 4
Player 2 starting position: 8
""")

PART1_RESULT = 739785
PART2_RESULT = NotImplemented


class TestDec21():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        player1, player2 = loaded
        assert player1.score == 0
        assert player2.score == 0
        assert player1.pos == 4
        assert player2.pos == 8

    @pytest.mark.parametrize("player, moves, expected", (
            (Player(4, 0), 6, Player(10, 10)),
            (Player(8, 0), 15, Player(3, 3)),
            (Player(10, 10), 24, Player(4, 14)),
            (Player(3, 3), 33, Player(6, 9)),
            (Player(4, 14), 13 + 14 + 15, Player(6, 20)),
            (Player(6, 9), 16 + 17 + 18, Player(7, 16)),
            (Player(6, 20), 19 + 20 + 21, Player(6, 26)),
            (Player(7, 16), 22 + 23 + 24, Player(6, 22)),
    ))
    def test_move(self, player, moves, expected):
        actual = move(player, moves)
        assert actual == expected

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
