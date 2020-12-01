#!/usr/bin/env python
# -*- coding: utf-8

import pytest

from ..dec04 import decreasing, no_double, just_double


@pytest.mark.parametrize("s, result", (
    ("111111", False),
    ("123456", False),
    ("111110", True),
))
def test_decreasing(s, result):
    assert decreasing(s) == result


@pytest.mark.parametrize("s, result", (
        ("111111", False),
        ("123456", True),
        ("122345", False),
        ("123455", False),
))
def test_no_double(s, result):
    assert no_double(s) == result


@pytest.mark.parametrize("s, result", (
        ("111111", False),
        ("123456", False),
        ("122345", True),
        ("123455", True),
        ("111122", True),
        ("112222", True),
        ("111233", True),
))
def test_just_double(s, result):
    assert just_double(s) == result


if __name__ == "__main__":
    pass
