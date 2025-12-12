from ibidem.advent_of_code.y2020.dec12 import *

PART1_RESULT = 25
PART1_ROUTE = [
    Command(Action("F"), 10),
    Command(Action("N"), 3),
    Command(Action("F"), 7),
    Command(Action("R"), 90),
    Command(Action("F"), 11),
]


class TestDec12:
    def test_part1(self):
        actual = part1(PART1_ROUTE)
        assert actual == PART1_RESULT
