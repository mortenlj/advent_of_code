#!/usr/bin/env python
# -*- coding: utf-8

import pytest

from ..dec16 import process


@pytest.mark.parametrize("signal, result", (
    ("80871224585914546619083218645595", "24176176"),
    ("19617804207202209144916044189917", "73745418"),
    ("69317163492948606335995924319873", "52432133"),
))
def test_process(signal, result):
    actual = process(signal, offset=0)
    assert actual == result


@pytest.mark.parametrize("signal, result", (
    ("03036732577212944063491565474664", "84462026"),
    ("02935109699940807407585447034323", "78725270"),
    ("03081770884921959731165446850517", "53553731"),
))
def test_real_process(signal, result):
    actual = process(signal, repetitions=10000)
    assert actual == result
