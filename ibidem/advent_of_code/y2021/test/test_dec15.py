import io

import pytest

from ibidem.advent_of_code.y2021.dec15 import load1, load2, part1, part2

TEST_INPUT = io.StringIO("""\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""")

PART1_RESULT = 40
PART2_RESULT = 315


class TestDec15:
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded1(self, input):
        return load1(input)

    @pytest.fixture
    def loaded2(self, input):
        return load2(input)

    def test_load1(self, loaded1):
        graph, lr = loaded1
        assert len(graph.nodes) == 100
        assert graph[(0, 1)][(1, 1)]["risk"] == 3
        assert graph[(1, 0)][(1, 1)]["risk"] == 3
        assert lr == (9, 9)
        assert graph[lr][(lr[0] - 1, lr[1])]["risk"] == 8

    def test_load2(self, loaded2):
        graph, lr = loaded2
        assert len(graph.nodes) == 100 * 5 * 5
        assert graph[(0, 1)][(1, 1)]["risk"] == 3
        assert graph[(1, 0)][(1, 1)]["risk"] == 3
        assert lr == (49, 49)
        assert graph[lr][(lr[0] - 1, lr[1])]["risk"] == 7

    def test_part1(self, loaded1):
        result = part1(*loaded1)
        assert result == PART1_RESULT

    def test_part2(self, loaded2):
        result = part2(*loaded2)
        assert result == PART2_RESULT
