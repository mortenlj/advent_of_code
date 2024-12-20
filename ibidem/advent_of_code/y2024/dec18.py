#!/usr/bin/env python
from ibidem.advent_of_code.a_star import a_star, Node
from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name, gen_list, Vector


@gen_list
def load(fobj):
    for line in fobj:
        yield tuple(map(int, line.strip().split(',')))


def part1(positions, size, bytecount):
    board = Board(size[0], size[1], do_translate=False, flip=False, fill_value=".", growable=False)
    for x, y in positions[:bytecount]:
        board.set(x, y, "#")
    cost, _ = a_star(Node(Vector(0, 0)), Vector(size[0] - 1, size[1] - 1), board)
    return cost


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(18, 2024)) as fobj:
        p1_result = part1(load(fobj), (71, 71), 1024)
        print(f"Part 1: {p1_result}")
    with open(get_input_name(18, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
