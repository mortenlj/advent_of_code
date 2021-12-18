import io

import pytest

from ibidem.advent_of_code.y2021.dec18 import load, part1, part2, snailadd, reduce, split, explode, magnitude

TEST_INPUT = io.StringIO("""\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""")

PART1_RESULT = 4140
PART2_RESULT = NotImplemented

LARGE_ADDITION_EXAMPLE = (
    [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
    [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
    [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
    [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]],
    [7, [5, [[3, 8], [1, 4]]]],
    [[2, [2, 2]], [8, [8, 1]]],
    [2, 9],
    [1, [[[9, 3], 9], [[9, 0], [0, 7]]]],
    [[[5, [7, 4]], 7], 1],
    [[[[4, 2], 2], 6], [8, 7]],
)


class TestDec18():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(list(loaded)) == 10

    @pytest.mark.parametrize("numbers, expected", (
            (([1, 1], [2, 2], [3, 3], [4, 4]), [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]),
            (([1, 1], [2, 2], [3, 3], [4, 4], [5, 5]), [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]),
            (([1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]), [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]),
            (LARGE_ADDITION_EXAMPLE, [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]),
    ))
    def test_snailadd(self, numbers, expected):
        actual = snailadd(numbers)
        assert actual == expected

    @pytest.mark.parametrize("action, number, expected", (
            (True, [[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]),
            (True, [7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
            (True, [[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
            (True, [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]),
            (True, [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]),
            (False, [1, 2], [1, 2]),
    ))
    def test_explode(self, action, number, expected):
        result = explode(number)
        assert result == action
        assert number == expected

    @pytest.mark.parametrize("action, number, expected", (
            (True, [[[[0, 7], 4], [15, [0, 13]]], [1, 1]], [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]),
            (True, [10], [[5, 5]]),
            (False, [1], [1]),
    ))
    def test_split(self, action, number, expected):
        result = split(number)
        assert result == action
        assert number == expected

    @pytest.mark.parametrize("number, expected", (
            ([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]], [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]),
    ))
    def test_reduce(self, number, expected):
        reduce(number)
        assert number == expected

    @pytest.mark.parametrize("number, expected", (
            ([[1, 2], [[3, 4], 5]], 143),
            ([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]], 1384),
            ([[[[1, 1], [2, 2]], [3, 3]], [4, 4]], 445),
            ([[[[3, 0], [5, 3]], [4, 4]], [5, 5]], 791),
            ([[[[5, 0], [7, 4]], [5, 5]], [6, 6]], 1137),
            ([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]], 3488),
    ))
    def test_magnitude(self, number, expected):
        actual = magnitude(number)
        assert actual == expected

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
