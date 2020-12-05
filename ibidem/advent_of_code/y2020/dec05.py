#!/usr/bin/env python

from ibidem.advent_of_code.y2020.util import get_input_name


class BoardingPass():
    def __init__(self, s):
        s = s.translate(str.maketrans("FBLR", "0101"))
        self.row = int(s[:7], 2)
        self.column = int(s[7:], 2)
        self.seat_id = self.row * 8 + self.column

    def __str__(self):
        return f"BoardingPass(row={self.row}, column={self.column}, seat_id={self.seat_id})"


def load():
    passes = []
    with open(get_input_name("dec05")) as fobj:
        for line in fobj:
            passes.append(BoardingPass(line.strip()))
    return passes


def part1():
    passes = load()
    winner = max(p.seat_id for p in passes)
    print(f"The highest Seat ID in part 1 is {winner}")


def part2():
    passes = {bp.seat_id: bp for bp in load()}
    pass_ids = set(passes.keys())
    all_passes = set(row * 8 + column for row in range(127) for column in range(8))
    missing = all_passes - pass_ids
    print(f"Missing: {missing}")
    for id in missing:
        if id + 1 in missing or id - 1 in missing:
            continue
        print(f"My seat: {id}")


if __name__ == "__main__":
    part1()
    part2()
