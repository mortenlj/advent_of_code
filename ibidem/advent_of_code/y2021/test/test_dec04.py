from ibidem.advent_of_code.y2021.dec04 import _load_input, part1, part2

TEST_INPUT = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

PART1_RESULT = 4512
PART2_RESULT = 1924


class TestDec04:
    def test_load_input(self):
        actual_numbers, actual_boards = _load_input(TEST_INPUT)
        assert len(actual_numbers) == 27
        assert len(actual_boards) == 3
        for i in range(3):
            assert actual_boards[i].size_x == 5
            assert actual_boards[i].size_y == 5

    def test_part1(self):
        numbers, boards = _load_input(TEST_INPUT)
        result = part1(numbers, boards)
        assert PART1_RESULT == result

    def test_part2(self):
        numbers, boards = _load_input(TEST_INPUT)
        result = part2(numbers, boards)
        assert PART2_RESULT == result
