#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    for line in fobj:
        line = line.strip()
        if not line:
            continue
        row, groups = line.split()
        groups = tuple(map(int, groups.split(",")))
        yield row, groups


def arrangements(maprow, groups):
    # print("Mapping arrangements for row", maprow, "with groups", groups)
    count = 0
    for option in row_part(maprow):
        if identify_groups(option) == groups:
            # print("Found", option)
            count += 1
    return count


def identify_groups(row):
    groups = []
    count = 0
    for i, c in enumerate(row):
        if c == "#":
            count += 1
        else:
            if count:
                groups.append(count)
                count = 0
    if count:
        groups.append(count)
    return tuple(groups)


def row_part(row):
    if not row:
        yield []
        return
    head, tail = row[0], row[1:]
    if head == "?":
        for options in row_part(tail):
            yield ["."] + options
        for options in row_part(tail):
            yield ["#"] + options
    else:
        for options in row_part(tail):
            yield [head] + options


def part1(input):
    result = 0
    for row, groups in input:
        count = arrangements(row, groups)
        print("Found", count, "arrangements for row", row)
        result += count
    return result


def unfold(maprow, groups):
    new_row = "?".join([maprow for r in range(5)])
    new_groups = tuple(groups * 5)
    return new_row, new_groups


def part2(input):
    result = 0
    for row, groups in input:
        row, groups = unfold(row, groups)
        count = arrangements(row, groups)
        print("Found", count, "arrangements for row", row)
        result += count


if __name__ == "__main__":
    with open(get_input_name(12, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(12, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
