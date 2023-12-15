#!/usr/bin/env python
import re
from collections import defaultdict
from dataclasses import dataclass, field

from ibidem.advent_of_code.util import get_input_name

STEP_PATTERN = re.compile(r"([a-z]+)([=-])(\d+)?")


@dataclass
class Lens:
    label: str
    focal_length: int = field(compare=False)


def load(fobj):
    return fobj.read().strip().split(",")


def hash(step):
    cv = 0
    for c in step:
        cv += ord(c)
        cv = cv * 17
        cv = cv % 256
    return cv


def part1(input):
    return sum(hash(step) for step in input)


def focusing_power(box_num, slot, focal_length):
    return box_num * slot * focal_length


def part2(input):
    boxes = defaultdict(list)
    for step in input:
        if m := STEP_PATTERN.match(step):
            label = m.group(1)
            operation = m.group(2)
            box = boxes[hash(label)]
            if operation == "=":
                focal_length = int(m.group(3))
                lens = Lens(label, focal_length)
                if lens in box:
                    idx = box.index(lens)
                    box[idx] = lens
                else:
                    box.append(lens)
            else:
                lens = Lens(label, 0)
                if lens in box:
                    box.remove(lens)
    result = 0
    for box_num, box in boxes.items():
        if len(box) == 0:
            continue
        for slot, lens in enumerate(box):
            result += focusing_power(box_num + 1, slot + 1, lens.focal_length)
    return result


if __name__ == "__main__":
    with open(get_input_name(15, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(15, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
