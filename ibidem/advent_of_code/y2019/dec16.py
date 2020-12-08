#!/usr/bin/env python
# -*- coding: utf-8

import numpy as np

from ibidem.advent_of_code.util import get_input_name

BASE_PATTERN = [0, 1, 0, -1]


def pattern_generator(i):
    first = True
    while True:
        for v in BASE_PATTERN:
            for _ in range(i + 1):
                if first:
                    first = False
                    continue
                yield v


def process_signal(i, signal):
    return abs(sum((v * p) for (v, p) in zip(signal, pattern_generator(i)))) % 10


def process_phase(signal):
    return [process_signal(i, signal) for i in range(len(signal))]


def process_phase_offset(signal):
    cs = np.flip(np.cumsum(np.flip(signal)))
    return np.mod(np.abs(cs), 10)


def process(data, repetitions=1, offset=None):
    print("Starting new process")
    signal = np.fromiter((int(c) for c in data), dtype=np.int8)
    signal = np.tile(signal, repetitions)
    print("Signal is {} digits long".format(len(signal)))
    if offset is None:
        offset = int(data[:7])
        assert offset > len(signal) / 2
        print("Dropping first {} digits".format(offset))
        pp = process_phase_offset
    else:
        pp = process_phase
    signal = np.array(signal[offset:])
    print("Signal is {} digits long after dropping offset".format(len(signal)))
    for phase in range(100):
        signal = pp(signal)
        if phase % 10 == 0:
            print("Completed phase {}".format(phase))
    return "".join(str(d) for d in signal)[:8]


def part1():
    with open(get_input_name(16, 2019)) as fobj:
        data = fobj.read().strip()
    result = process(data, offset=0)
    print("After 100 phases, the cleaned signal starts with these 8 digits: {}".format(result))


def part2():
    with open(get_input_name(16, 2019)) as fobj:
        data = fobj.read().strip()
    result = process(data, repetitions=10000)
    print("After 100 phases, the cleaned signal starts with these 8 digits: {}".format(result))


if __name__ == "__main__":
    part1()
    part2()
