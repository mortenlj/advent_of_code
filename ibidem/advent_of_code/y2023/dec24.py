#!/usr/bin/env python
import itertools

from Geometry3D import Point, Vector, HalfLine, set_sig_figures, set_eps
from rich.progress import track

from ibidem.advent_of_code.util import get_input_name, gen_list


@gen_list
def load(fobj):
    for line in fobj:
        coords, velocity = line.split('@')
        position = Point(ignore_z(coords))
        speed = Vector(ignore_z(velocity))
        yield HalfLine(position, speed)


@gen_list
def ignore_z(line):
    for v in line.split(",")[:2]:
        yield int(v.strip())
    yield 0


# Too low: 6990, 7226, 14006
# Wrong: 14433, 9703, 9453, 9339, 10855, 10873
def part1(lines, limit):
    set_eps(1)
    intersections = set()
    for a, b in track(list(itertools.permutations(lines, 2))):
        intersection = a.intersection(b)
        if intersection is None:
            continue
        if limit[0] <= intersection.x <= limit[1]:
            if limit[0] <= intersection.y <= limit[1]:
                intersections.add(intersection)
    return len(intersections)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(24, 2023)) as fobj:
        p1_result = part1(load(fobj), (200000000000000, 400000000000000))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(24, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
