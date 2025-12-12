from ibidem.advent_of_code.y2020.dec09 import find_invalid, find_weakness

TEST_INVALID = 127
TEST_WEAKNESS = 62
TEST_PREAMBLE = 5
TEST_DATA = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]


class TestDec09:
    def test_find_invalid(self):
        actual = find_invalid(TEST_DATA, TEST_PREAMBLE)
        assert actual == TEST_INVALID

    def test_find_weakness(self):
        actual = find_weakness(TEST_DATA, TEST_INVALID)
        assert actual == TEST_WEAKNESS
