#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


def load():
    with open(get_input_name(25, 2020)) as fobj:
        return [int(line.strip()) for line in fobj]


def transform_loop(value, subject):
    value *= subject
    value %= 20201227
    return value


def find_key(subject, loop_size):
    value = 1
    for _ in range(loop_size):
        value = transform_loop(value, subject)
    return value


def part1(keys):
    value = 1
    loop_size = 0
    while value not in keys:
        value = transform_loop(value, 7)
        loop_size += 1
        if loop_size % 100000 == 0:
            print(f"Tried {loop_size} transformations without luck")
    encryption_key = 0
    if value == keys[0]:
        encryption_key = find_key(keys[1], loop_size)
    elif value == keys[1]:
        encryption_key = find_key(keys[0], loop_size)
    print(f"Encryption key: {encryption_key}")
    return encryption_key


def part2():
    pass


if __name__ == "__main__":
    keys = load()
    part1(keys)
    part2()
