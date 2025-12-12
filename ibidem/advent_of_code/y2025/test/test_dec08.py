import io
import textwrap
from collections import namedtuple
from heapq import heappop, heapify

import pytest
from vectormath import Vector3Array, Vector3

from ibidem.advent_of_code.y2025.dec08 import load, part1, part2, distances

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        40,
        25272,
        io.StringIO(
            textwrap.dedent("""\
        162,817,812
        57,618,57
        906,360,560
        592,479,940
        352,342,300
        466,668,158
        542,29,236
        431,825,988
        739,650,466
        52,470,668
        216,146,977
        819,987,18
        117,168,530
        805,96,715
        346,949,466
        970,615,88
        941,993,340
        862,61,35
        984,92,344
        425,690,689
    """)
        ),
    ),
]


class TestDec08:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        assert isinstance(loaded, Vector3Array)
        assert len(loaded) == 20

    def test_distances(self, loaded):
        heap = distances(loaded, 10)
        assert len(heap) == 10
        heapify(heap)
        min_distance, min_v1, min_v2 = heappop(heap)
        expected_v1 = Vector3(162, 817, 812)
        expected_v2 = Vector3(425, 690, 689)
        assert (expected_v1 == min_v1).all()
        assert (expected_v2 == min_v2).all()

    def test_part1(self, loaded, case):
        result = part1(loaded, 10)
        assert result == case.part1

    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
