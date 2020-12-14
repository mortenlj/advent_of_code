from ibidem.advent_of_code.y2020.dec12 import *

PART1_RESULT = 25
PART2_RESULT = 286
INPUT = [
    Command(Action("F"), 10),
    Command(Action("N"), 3),
    Command(Action("F"), 7),
    Command(Action("R"), 90),
    Command(Action("F"), 11),
]


class TestDec12():
    def test_part1(self):
        actual = part1(INPUT)
        assert actual == PART1_RESULT

    def test_part2(self):
        actual = part2(INPUT)
        assert actual == PART2_RESULT
