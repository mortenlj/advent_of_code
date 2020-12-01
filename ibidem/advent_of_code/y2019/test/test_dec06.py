#!/usr/bin/env python
# -*- coding: utf-8
import pytest

from ..dec06 import calculate_transfers, calculate_orbits, load_planets, find_path_to_com


def test_part1():
    lines = """COM)B
C)D
B)C
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
""".splitlines(keepends=True)
    orbits = calculate_orbits(lines)
    assert orbits == 42


@pytest.fixture
def planets():
    lines = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
""".splitlines(keepends=True)
    return load_planets(lines)


@pytest.mark.parametrize("start, path", (
        ("YOU", ["K", "J", "E", "D", "C", "B"]),
        ("SAN", ["I", "D", "C", "B"]),
))
def test_find_path_to_com(start, path, planets):
    you_path = find_path_to_com(planets[start])
    assert you_path == path


def test_calculate_transfers(planets):
    transfers = calculate_transfers(planets)
    assert transfers == 4
