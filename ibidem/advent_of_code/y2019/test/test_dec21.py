#!/usr/bin/env python
# -*- coding: utf-8
import pytest


@pytest.mark.parametrize(
    "a, b, c, d, result",
    (
        (True, True, True, True, False),
        (False, True, True, True, True),
        (True, False, True, True, True),
        (True, True, False, True, True),
        (True, True, True, False, False),
        (True, False, True, False, False),
        (True, True, False, False, False),
    ),
)
def test_logic1(a, b, c, d, result):
    t = not a  # t
    t = not t  # t
    t = b and t
    t = c and t
    j = not t
    j = d and j

    assert j == result


@pytest.mark.parametrize(
    "ground, result",
    (
        (".########", True),
        ("###.#####", False),
        ("#.#.#####", False),
        ("##..#####", False),
        ("###..####", False),
        ("###.####.", False),
        ("#...#####", False),
        ("##.#.##.#", False),
        ("#.#.##.##", False),
        (".#.##.###", True),
        ("#.##.#.##", True),
        ("#.##.###.", True),
        ("#.##.####", True),
        ("#..#.####", True),
        ("...####.#", True),
        ("#.###..#.", True),
    ),
)
def test_logic2(ground, result):
    a, b, c, d, e, f, g, h, i = [v == "#" for v in ground]
    t = j = False

    # Jump if b false and e or f false
    j = not f  # j
    t = not e  # t
    t = j or t
    j = not b  # t
    j = t and j

    # Jump if already jumping, and c false, and h true
    t = not c  # t
    j = t or j
    t = not h  # t
    t = not t  # t
    j = t and j

    # Jump if already jumping, or a false
    t = not a  # t
    j = t or j

    # Don't jump if d false
    j = d and j

    assert j == result


def operations():
    a = b = c = d = t = j = False  # noqa

    j = a and j
    j = b or j
    j = not c  # j
