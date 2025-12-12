from ibidem.advent_of_code.y2020.dec25 import part1


class TestDec25:
    def test_part1(self):
        actual = part1([5764801, 17807724])
        assert actual == 14897079
