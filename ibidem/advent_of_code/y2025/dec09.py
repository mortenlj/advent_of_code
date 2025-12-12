#!/usr/bin/env python
import dataclasses
import itertools
from functools import lru_cache
from heapq import heapify_max, heappush_max, heappop_max

from rich.progress import track

from ibidem.advent_of_code.util import get_input_name, gen_list, Vector, time_this


@gen_list
def load(fobj):
    for line in fobj:
        line = line.strip()
        yield Vector(*(int(c) for c in line.split(",")))


@time_this
def part1(red_tiles):
    areas = []
    heapify_max(areas)
    for v1, v2 in track(itertools.combinations(red_tiles, 2)):
        area = (abs(v1.x - v2.x) + 1) * (abs(v1.y - v2.y) + 1)
        heappush_max(areas, area)
    return heappop_max(areas)


def inside(poly, v1, v2):
    min_x = min(v1.x, v2.x)
    max_x = max(v1.x, v2.x)
    length = max_x - min_x
    min_y = min(v1.y, v2.y)
    max_y = max(v1.y, v2.y)
    width = max_y - min_y
    total = length * width
    for x, y in track(
        itertools.product(range(min_x, max_x + 1), range(min_y, max_y + 1)),
        transient=True,
        total=total,
        description=f"Checking {total} points",
    ):
        if Vector(x, y) not in poly:
            return False
    return True


def orientation(p: Vector, q: Vector, r: Vector):
    """find orientation of ordered triplet (p, q, r)
    0 --> p, q and r are collinear
    1 --> Clockwise
    2 --> Counterclockwise
    """
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

    # collinear
    if val == 0:
        return 0

    # clock or counterclock wise
    # 1 for clockwise, 2 for counterclockwise
    return 1 if val > 0 else 2


@dataclasses.dataclass(frozen=True)
class Line:
    start: Vector
    end: Vector

    def __contains__(self, point):
        return max(self.start.x, self.end.x) >= point.x >= min(
            self.start.x, self.end.x
        ) and max(self.start.y, self.end.y) >= point.y >= min(self.start.y, self.end.y)

    def intersects(self, other: Line):
        # find the four orientations needed
        # for general and special cases
        o1 = orientation(self.start, self.end, other.start)
        o2 = orientation(self.start, self.end, other.end)
        o3 = orientation(other.start, other.end, self.start)
        o4 = orientation(other.start, other.end, self.end)

        # general case
        if o1 != o2 and o3 != o4:
            return True

        # special cases
        # p1, q1 and p2 are collinear and p2 lies on segment p1q1
        if o1 == 0 and other.start in self:
            return True

        # p1, q1 and q2 are collinear and q2 lies on segment p1q1
        if o2 == 0 and other.end in self:
            return True

        # p2, q2 and p1 are collinear and p1 lies on segment p2q2
        if o3 == 0 and self.start in other:
            return True

        # p2, q2 and q1 are collinear and q1 lies on segment p2q2
        if o4 == 0 and self.end in other:
            return True

        return False

    def points(self):
        for x in range(self.start.x, self.end.x + 1):
            for y in range(self.start.y, self.end.y + 1):
                yield Vector(x, y)


class Polygon:
    def __init__(self, lines):
        self.lines = lines
        self.min_y = min(min(l.start.y, l.end.y) for l in lines) - 1

    @lru_cache(maxsize=None)
    def __contains__(self, item):
        exit_line = Line(item, Vector(item.x, self.min_y))
        count = 0
        for line in self.lines:
            if item == line.start or item == line.end:
                return True
            if item in line:
                return True
            if line.intersects(exit_line):
                count += 1
        return count % 2 != 0

    def __repr__(self):
        return f"Polygon(lines={self.lines})"


def make_poly(red_tiles):
    poly = []
    tiles = red_tiles + [red_tiles[0]]
    for v1, v2 in itertools.pairwise(tiles):
        assert v1.x == v2.x or v1.y == v2.y
        poly.append(Line(v1, v2))
    return Polygon(poly)


def part2(red_tiles):
    poly = make_poly(red_tiles)
    largest = 0
    total = len(list(itertools.combinations(red_tiles, 2)))
    for v1, v2 in track(
        itertools.combinations(red_tiles, 2),
        total=total,
        description=f"Checking {total} possible areas",
    ):
        area = (abs(v1.x - v2.x) + 1) * (abs(v1.y - v2.y) + 1)
        if area > largest and inside(poly, v1, v2):
            largest = area
    return largest


if __name__ == "__main__":
    with open(get_input_name(9, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(9, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
