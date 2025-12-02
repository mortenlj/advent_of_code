#!/usr/bin/env python
import itertools

from ibidem.advent_of_code.util import get_input_name, gen_list


@gen_list
def load(fobj):
    ranges = fobj.read().strip().split(",")
    result = []
    for rng in ranges:
        p = rng.split("-")
        yield int(p[0]), int(p[1])+1


def part1(ranges):
    result = 0
    for start, end in ranges:
        for id in range(start, end):
            value = str(id)
            mid_point = len(value) // 2
            if value[:mid_point] == value[mid_point:]:
                result += id
    return result


def part2(ranges):
    invalid = set()
    for start, end in ranges:
        for id in range(start, end):
            value = str(id)
            max_batch_size = (len(value) // 2) + 1
            for batch_size in range(1, max_batch_size):
                if len(value) % batch_size != 0:
                    continue
                parts = list(itertools.batched(value, batch_size))
                if all(x == parts[0] for x in parts):
                    invalid.add(id)
    return sum(invalid)


if __name__ == "__main__":
    with open(get_input_name(2, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(2, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
