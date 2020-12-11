import textwrap

from ibidem.advent_of_code.y2020.dec11 import *

TEST_BOARDS = (
    textwrap.dedent("""\
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
    """),
    textwrap.dedent("""\
    #.##.##.##
    #######.##
    #.#.#..#..
    ####.##.##
    #.##.##.##
    #.#####.##
    ..#.#.....
    ##########
    #.######.#
    #.#####.##
    """),
    textwrap.dedent("""\
    #.LL.L#.##
    #LLLLLL.L#
    L.L.L..L..
    #LLL.LL.L#
    #.LL.LL.LL
    #.LLLL#.##
    ..L.L.....
    #LLLLLLLL#
    #.LLLLLL.L
    #.#LLLL.##
    """),
    textwrap.dedent("""\
    #.##.L#.##
    #L###LL.L#
    L.#.#..#..
    #L##.##.L#
    #.##.LL.LL
    #.###L#.##
    ..#.#.....
    #L######L#
    #.LL###L.L
    #.#L###.##
    """),
    textwrap.dedent("""\
    #.#L.L#.##
    #LLL#LL.L#
    L.L.L..#..
    #LLL.##.L#
    #.LL.LL.LL
    #.LL#L#.##
    ..L.L.....
    #L#LLLL#L#
    #.LLLLLL.L
    #.#L#L#.##
    """),
    textwrap.dedent("""\
    #.#L.L#.##
    #LLL#LL.L#
    L.#.L..#..
    #L##.##.L#
    #.#L.LL.LL
    #.#L#L#.##
    ..L.L.....
    #L#L##L#L#
    #.LLLLLL.L
    #.#L#L#.##
    """),
)


class TestDec11():
    def test_step_one(self):
        actual = step(Board.from_string(TEST_BOARDS[0]))
        assert actual == Board.from_string(TEST_BOARDS[1])

    def test_step_last(self):
        actual = step(Board.from_string(TEST_BOARDS[-1]))
        assert actual == Board.from_string(TEST_BOARDS[-1])

    def test_part1(self):
        actual = part1(Board.from_string(TEST_BOARDS[0]))
        assert actual == 37
