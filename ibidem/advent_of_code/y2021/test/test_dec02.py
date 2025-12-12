from ibidem.advent_of_code.y2021.dec02 import part1, part2

TEST_INPUT = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".splitlines(keepends=False)


class TestDec02:
    def test_part1(self):
        result = part1(TEST_INPUT)
        assert result == 150

    def test_part2(self):
        result = part2(TEST_INPUT)
        assert result == 900
