#!/usr/bin/env python
from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read())


def tilt_column(column):
    new_column = column.copy()
    insert_at = 0
    for i, c in enumerate(column):
        if c == ".":
            continue
        if c == "#":
            insert_at = i + 1
        if c == "O":
            new_column[i] = "."
            new_column[insert_at] = "O"
            insert_at += 1
    return new_column


def calculate_load(column):
    total_load = 0
    for i, c in enumerate(reversed(column)):
        if c == "O":
            total_load += i + 1
    return total_load


def part1(input: Board):
    result = 0
    for x in range(input.size_x):
        column = input.grid[:, x]
        new_column = tilt_column(column)
        total_load = calculate_load(new_column)
        result += total_load
    return result


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(14, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(14, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
