#!/usr/bin/env python
from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read(), fill_value=".")


def find_start(x, row):
    if x < 0:
        return 0
    if row[x].isdigit():
        return find_start(x - 1, row)
    return x + 1


def find_end(x, row):
    if x >= len(row):
        return len(row) - 1
    if row[x].isdigit():
        return find_end(x + 1, row)
    return x - 1


def part1(input: Board):
    parts = []
    for x in range(input.size_x):
        for y in range(input.size_y):
            c = input.get(x, y)
            if c != "." and not c.isdigit():
                parts.append((x, y))
    part_numbers = []
    for x, y in parts:
        numbers_for_part = set()
        for nx, ny in input.adjacent_indexes(x, y, include_diagonal=True):
            c = input.get(nx, ny)
            if c.isdigit():
                sx = find_start(nx, input.get_row(ny))
                ex = find_end(nx, input.get_row(ny))
                part_number = int("".join([input.get(ix, ny) for ix in range(sx, ex + 1)]))
                numbers_for_part.add(part_number)
        part_numbers.extend(numbers_for_part)
    return sum(part_numbers)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(3, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(3, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
