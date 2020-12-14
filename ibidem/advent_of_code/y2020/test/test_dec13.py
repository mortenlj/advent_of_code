import pytest

from ibidem.advent_of_code.y2020.dec13 import *

TEST_BUSSES = [7, 13, None, None, 59, None, 31, 19]
PART1_ESTIMATE = 939
PART1_WAITING = 5
PART1_DEPARTING_BUS = 59
PART1_RESULT = 295


class TestDec13():
    def test_part1(self):
        waiting_time, first_departing_bus, result = part1(PART1_ESTIMATE, TEST_BUSSES)
        assert waiting_time == PART1_WAITING
        assert first_departing_bus == PART1_DEPARTING_BUS
        assert result == PART1_RESULT

    @pytest.mark.parametrize("busses, timestamp", (
            (TEST_BUSSES, 1068781),
            ((17, None, 13, 19), 3417),
            ((67, 7, 59, 61), 754018),
            ((67, None, 7, 59, 61), 779210),
            ((67, 7, None, 59, 61), 1261476),
            ((1789, 37, 47, 1889), 1202161486),
    ))
    def test_part2(self, busses, timestamp):
        actual = part2(busses, timestamp)
        assert actual == timestamp
