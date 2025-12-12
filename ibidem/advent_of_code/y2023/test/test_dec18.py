import io
import textwrap
from collections import namedtuple

import pytest
from vectormath import Vector2 as V2

from ibidem.advent_of_code.y2023.dec18 import (
    load1,
    part1,
    part2,
    load2,
    poly_area,
    Direction,
    generate_path,
    Instruction,
)

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        62,
        952408144115,
        io.StringIO(
            textwrap.dedent("""\
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
    """)
        ),
    ),
]


class TestDec18:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded1(self, case):
        return load1(case.input)

    def test_load1(self, loaded1):
        assert len(loaded1) == 14

    @pytest.fixture
    def loaded2(self, case):
        return load2(case.input)

    def test_load2(self, loaded2):
        assert len(loaded2) == 14
        assert loaded2[0].distance == 461937
        assert loaded2[0].direction == Direction.RIGHT
        assert loaded2[1].distance == 56407
        assert loaded2[1].direction == Direction.DOWN
        assert loaded2[-1].distance == 500254
        assert loaded2[-1].direction == Direction.UP

    def test_part1(self, loaded1, case):
        result = part1(loaded1)
        assert result == case.part1

    @pytest.mark.parametrize(
        "instructions, expected_path, expected_addition",
        [
            (
                None,
                [
                    V2(0, 0),
                    V2(6, 0),
                    V2(6, -5),
                    V2(4, -5),
                    V2(4, -7),
                    V2(6, -7),
                    V2(6, -9),
                    V2(1, -9),
                    V2(1, -7),
                    V2(0, -7),
                    V2(0, -5),
                    V2(2, -5),
                    V2(2, -2),
                    V2(0, -2),
                ],
                20,
            ),
            (
                [
                    Instruction(Direction.RIGHT, 1),
                    Instruction(Direction.DOWN, 1),
                    Instruction(Direction.LEFT, 1),
                    Instruction(Direction.UP, 1),
                ],
                [V2(0, 0), V2(1, 0), V2(1, -1), V2(0, -1)],
                3,
            ),
        ],
    )
    def test_generate_path(
        self, loaded1, instructions, expected_path, expected_addition
    ):
        if instructions is None:
            instructions = loaded1
        actual_path, actual_addition = generate_path(instructions)
        assert actual_addition == expected_addition
        for i, pos in enumerate(actual_path):
            assert pos.x == expected_path[i].x
            assert pos.y == expected_path[i].y

    def test_part2(self, loaded2, case):
        result = part2(loaded2)
        assert result == case.part2

    @pytest.mark.parametrize(
        "path, expected",
        [
            ([V2(0, 0), V2(0, 1), V2(1, 1), V2(1, 0)], 1),
            (
                [
                    V2(0, 0),
                    V2(6, 0),
                    V2(6, -5),
                    V2(4, -5),
                    V2(4, -7),
                    V2(6, -7),
                    V2(6, -9),
                    V2(1, -9),
                    V2(1, -7),
                    V2(0, -7),
                    V2(0, -5),
                    V2(2, -5),
                    V2(2, -2),
                    V2(0, -2),
                ],
                42,
            ),
        ],
    )
    def test_poly_area(self, path, expected):
        assert poly_area(path) == expected
