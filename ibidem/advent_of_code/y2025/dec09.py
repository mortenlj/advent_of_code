#!/usr/bin/env python
import itertools
from heapq import heapify_max, heappush_max, heappop_max

from rich.progress import track

from ibidem.advent_of_code.util import get_input_name, gen_list, Vector


@gen_list
def load(fobj):
    for line in fobj:
        line = line.strip()
        yield Vector(*(int(c) for c in line.split(",")))


def calculate_areas(red_tiles):
    areas = []
    heapify_max(areas)
    for v1, v2 in track(itertools.combinations(red_tiles, 2)):
        area = (abs(v1.x - v2.x) + 1) * (abs(v1.y - v2.y) + 1)
        heappush_max(areas, area)
    return areas


def part1(red_tiles):
    areas = calculate_areas(red_tiles)
    return heappop_max(areas)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(9, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(9, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
