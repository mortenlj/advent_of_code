#!/usr/bin/env python
from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name, gen_list
from ibidem.advent_of_code.visualizer import Sprites, Tiles, initialize_and_display_splash
from ibidem.advent_of_code.visualizer.board import BoardVisualizer


@gen_list
def load(fobj):
    for line in fobj:
        yield tuple(map(int, line.strip().split(',')))


def part1(positions, size, bytecount):
    board = Board(size[0], size[1], do_translate=False, flip=False, fill_value=".", growable=False)
    for x, y in positions[:bytecount]:
        board.set(x, y, "#")
    initialize_and_display_splash()
    visualizer = BoardVisualizer(board, {"#": Tiles.Obstacle, ".": Tiles.Grass})
    visualizer.pause()
    return None


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(18, 2024)) as fobj:
        p1_result = part1(load(fobj), (71,71), 1024)
        print(f"Part 1: {p1_result}")
    with open(get_input_name(18, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
