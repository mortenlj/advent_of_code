#!/usr/bin/env python
import itertools

from ibidem.advent_of_code.a_star import a_star, Node
from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name, gen_list, Vector


@gen_list
def load(fobj):
    for line in fobj:
        yield tuple(map(int, line.strip().split(",")))


def part1(positions, size, bytecount):
    board = Board(
        size[0], size[1], do_translate=False, flip=False, fill_value=".", growable=False
    )
    for x, y in positions[:bytecount]:
        board.set(x, y, "#")
    cost, _ = a_star(Node(Vector(0, 0)), Vector(size[0] - 1, size[1] - 1), board)
    return cost


def part2(positions, size, bytecount):
    current_bc = bytecount
    working_bytecount = 0
    working_board = Board(
        size[0], size[1], do_translate=False, flip=False, fill_value=".", growable=False
    )
    while current_bc > 0:
        this_bytecount, working_board = find_last_working_bytecount(
            current_bc, positions[working_bytecount:], size, working_board
        )
        working_bytecount += this_bytecount
        print(
            f"Stepping {current_bc}: Last working board at bytecount {working_bytecount}"
        )
        if current_bc == 1:
            break
        current_bc = current_bc // 2
    print("Last working board at bytecount", working_bytecount)
    x, y = positions[working_bytecount]
    return f"{x},{y}"


def find_last_working_bytecount(bytecount, positions, size, clear_board):
    working_board = clear_board.copy()
    working_bytecount = 0
    for i, bytes in enumerate(itertools.batched(positions, bytecount)):
        board = working_board.copy()
        for x, y in bytes:
            board.set(x, y, "#")
        _, path = a_star(Node(Vector(0, 0)), Vector(size[0] - 1, size[1] - 1), board)
        if path is not None:
            working_board = board
            working_bytecount = (i + 1) * bytecount
        else:
            break
    return working_bytecount, working_board


if __name__ == "__main__":
    with open(get_input_name(18, 2024)) as fobj:
        p1_result = part1(load(fobj), (71, 71), 1024)
        print(f"Part 1: {p1_result}")
    with open(get_input_name(18, 2024)) as fobj:
        p2_result = part2(load(fobj), (71, 71), 1024)
        print(f"Part 2: {p2_result}")
