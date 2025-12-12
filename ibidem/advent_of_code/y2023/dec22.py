#!/usr/bin/env python
import copy
import re

from Geometry3D import Point, Visualizer, Segment
from rich.progress import track

from ibidem.advent_of_code.util import get_input_name, gen_list

BRICK_PATTERN = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")
COLORS = ('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w')


class Brick:
    start: Point
    end: Point

    def __init__(self, start, end):
        self.start = start
        self.end = end
        if start == end:
            self.geo_body = start
        else:
            self.geo_body = Segment(start, end)

    @property
    def length(self):
        return self.geo_body.length()

    def low_point(self):
        return min(self.start.z, self.end.z)

    def high_point(self):
        return max(self.start.z, self.end.z)

    def intersects(self, other: 'Brick'):
        if isinstance(self.geo_body, Point):
            if isinstance(other.geo_body, Point):
                return self.geo_body == other.geo_body
            return other.intersects(self)
        return self.geo_body.intersection(other.geo_body)

    def drop(self, distance=1):
        new_start = Point(self.start.x, self.start.y, self.start.z - distance)
        new_end = Point(self.end.x, self.end.y, self.end.z - distance)
        return Brick(new_start, new_end)

    def lift(self):
        new_start = Point(self.start.x, self.start.y, self.start.z + 1)
        new_end = Point(self.end.x, self.end.y, self.end.z + 1)
        return Brick(new_start, new_end)

    def __repr__(self):
        return f"Brick({self.geo_body})"

    def __eq__(self, other):
        start_equal = self.start == other.start
        end_equal = self.end == other.end
        return start_equal and end_equal


@gen_list
def load(fobj):
    for line in fobj:
        if m := BRICK_PATTERN.match(line.strip()):
            start = Point(*map(int, m.group(1, 2, 3)))
            end = Point(*map(int, m.group(4, 5, 6)))
            yield Brick(start, end)


def settle(sorted_bricks: list[Brick], abort_on_drop=False):
    previous = []
    max_height = 0
    for brick in track(sorted_bricks, description="Settling bricks"):
        dropped = 0
        if brick.low_point() > max_height:
            brick = brick.drop(brick.low_point() - max_height - 1)
        intersects = False
        while not intersects:
            if brick.low_point() < 0:
                break
            for p in reversed(previous):
                if p.intersects(brick):
                    intersects = True
                    break
            else:
                brick = brick.drop()
                dropped += 1
        max_height = max(brick.high_point(), max_height)
        dropped -= 1
        if abort_on_drop and dropped > 0:
            return previous
        previous.append(brick.lift())
    return previous


def part1(bricks):
    sorted_bricks = sorted(bricks, key=lambda b: b.low_point())
    settled_bricks = settle(sorted_bricks)
    print("Bricks settled")
    #show_bricks(settled_bricks)
    count = 0
    for brick in settled_bricks:
        bricks = copy.deepcopy(settled_bricks)
        bricks.remove(brick)
        changed = settle(bricks, abort_on_drop=True)
        # show_bricks(changed)
        # show_bricks(bricks)
        if changed == bricks:
            count += 1
    return count


def show_bricks(bricks):
    r = Visualizer(backend='matplotlib')
    for i, brick in enumerate(bricks):
        r.add((brick.geo_body, COLORS[i % len(COLORS)], 10))
    r.show()


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(22, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(22, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
