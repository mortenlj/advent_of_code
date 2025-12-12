#!/usr/bin/env python
# -*- coding: utf-8

import pytest

from ..dec12 import load_input, Moon, perform_step, Vector, simulate, find_cycle


@pytest.mark.parametrize(
    "lines, io, europa, ganymede, callisto",
    (
        (
            [
                "<x=-1, y=0, z=2>",
                "<x=2, y=-10, z=-7>",
                "<x=4, y=-8, z=8>",
                "<x=3, y=5, z=-1>",
            ],
            Moon("Io", -1, 0, 2),
            Moon("Europa", 2, -10, -7),
            Moon("Ganymede", 4, -8, 8),
            Moon("Callisto", 3, 5, -1),
        ),
        (
            [
                "<x=-8, y=-10, z=0>",
                "<x=5, y=5, z=10>",
                "<x=2, y=-7, z=3>",
                "<x=9, y=-8, z=-3>",
            ],
            Moon("Io", -8, -10, 0),
            Moon("Europa", 5, 5, 10),
            Moon("Ganymede", 2, -7, 3),
            Moon("Callisto", 9, -8, -3),
        ),
    ),
)
def test_load(lines, io, europa, ganymede, callisto):
    moons = load_input(lines)
    assert moons[0] == io
    assert moons[1] == europa
    assert moons[2] == ganymede
    assert moons[3] == callisto


@pytest.mark.parametrize(
    "moons, steps, final_moons",
    (
        (
            [
                Moon("Io", -1, 0, 2),
                Moon("Europa", 2, -10, -7),
                Moon("Ganymede", 4, -8, 8),
                Moon("Callisto", 3, 5, -1),
            ],
            3,
            [
                Moon("Io", 5, -6, -1, Vector(0, -3, 0)),
                Moon("Europa", 0, 0, 6, Vector(-1, 2, 4)),
                Moon("Ganymede", 2, 1, -5, Vector(1, 5, -4)),
                Moon("Callisto", 1, -8, 2, Vector(0, -4, 0)),
            ],
        ),
        (
            [
                Moon("Io", -8, -10, 0),
                Moon("Europa", 5, 5, 10),
                Moon("Ganymede", 2, -7, 3),
                Moon("Callisto", 9, -8, -3),
            ],
            70,
            [
                Moon("Io", -33, -6, 5, Vector(-5, -4, 7)),
                Moon("Europa", 13, -9, 2, Vector(-2, 11, 3)),
                Moon("Ganymede", 11, -8, 2, Vector(8, -6, -7)),
                Moon("Callisto", 17, 3, 1, Vector(-1, -1, -3)),
            ],
        ),
    ),
)
def test_perform_step(moons, steps, final_moons):
    for _ in range(steps):
        perform_step(moons)
    for actual, expected in zip(moons, final_moons):
        assert actual == expected


@pytest.mark.parametrize(
    "moons, steps, final_moons",
    (
        (
            [
                Moon("Io", -1, 0, 2),
                Moon("Europa", 2, -10, -7),
                Moon("Ganymede", 4, -8, 8),
                Moon("Callisto", 3, 5, -1),
            ],
            10,
            [
                Moon("Io", 5, -6, -1, Vector(0, -3, 0)),
                Moon("Europa", 0, 0, 6, Vector(-1, 2, 4)),
                Moon("Ganymede", 2, 1, -5, Vector(1, 5, -4)),
                Moon("Callisto", 1, -8, 2, Vector(0, -4, 0)),
            ],
        ),
        (
            [
                Moon("Io", -8, -10, 0),
                Moon("Europa", 5, 5, 10),
                Moon("Ganymede", 2, -7, 3),
                Moon("Callisto", 9, -8, -3),
            ],
            100,
            [
                Moon("Io", -33, -6, 5, Vector(-5, -4, 7)),
                Moon("Europa", 13, -9, 2, Vector(-2, 11, 3)),
                Moon("Ganymede", 11, -8, 2, Vector(8, -6, -7)),
                Moon("Callisto", 17, 3, 1, Vector(-1, -1, -3)),
            ],
        ),
    ),
)
def test_simulate(moons, steps, final_moons):
    simulate(moons, steps)


@pytest.mark.parametrize(
    "moons, steps",
    (
        (
            [
                Moon("Io", -1, 0, 2),
                Moon("Europa", 2, -10, -7),
                Moon("Ganymede", 4, -8, 8),
                Moon("Callisto", 3, 5, -1),
            ],
            2772,
        ),
        (
            [
                Moon("Io", -8, -10, 0),
                Moon("Europa", 5, 5, 10),
                Moon("Ganymede", 2, -7, 3),
                Moon("Callisto", 9, -8, -3),
            ],
            4686774924,
        ),
    ),
)
def test_find_cycle(moons, steps):
    actual_steps = find_cycle(moons)
    assert actual_steps == steps
