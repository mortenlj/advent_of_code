#!/usr/bin/env python

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name
from ibidem.advent_of_code.visualizer import (
    initialize_and_display_splash,
    Tiles,
    Sprites,
)
from ibidem.advent_of_code.visualizer.board import BoardVisualizer


def load(fobj):
    return Board.from_string(fobj.read())


def part1(board):
    visualizing = initialize_and_display_splash()
    visualizer = BoardVisualizer(
        board, {"S": Tiles.Stone, ".": Tiles.Stone, "^": Tiles.Stone}
    )
    visualizer.pause()
    if visualizing:
        for x in range(board.size_x):
            for y in range(board.size_y):
                if board.get(x, y) == "^":
                    visualizer.draw(x, y, Sprites.Triangle)
    beams = set()
    old_beams = set()
    for x in range(board.size_x):
        if board.get(x, 0) == "S":
            beams.add(x)
            break
    splits = 0
    for y in range(1, board.size_y):
        new_beams = set()
        for beam in beams:
            if board.get(beam, y) == "^":
                visualizer.draw(beam, y, Sprites.BeamNorthWest, 90)
                visualizer.draw(beam, y, Sprites.BeamNorthWest, 180)
                splits += 1
                if beam - 1 >= 0:
                    new_beams.add(beam - 1)
                if beam + 1 < board.size_x:
                    new_beams.add(beam + 1)
            else:
                visualizer.draw(beam, y, Sprites.BeamNorth, 180)
                new_beams.add(beam)
            if beam - 1 in old_beams and board.get(beam - 1, y - 1) == "^":
                visualizer.draw(beam, y, Sprites.BeamNorthWest)
            if beam + 1 in old_beams and board.get(beam + 1, y - 1) == "^":
                visualizer.draw(beam, y, Sprites.BeamNorthWest, -90)
            if beam in old_beams:
                visualizer.draw(beam, y, Sprites.BeamNorth)
        visualizer.flip()
        old_beams = beams
        beams = new_beams
    visualizer.pause()
    return splits


def part2(board):
    beams = {}
    for x in range(board.size_x):
        if board.get(x, 0) == "S":
            beams[x] = 1
            break
    splits = 0
    for y in range(1, board.size_y):
        print(f"Assessing row {y}, with {len(beams.keys())} beams to assess")
        new_beams = {}
        for beam in beams.keys():
            if board.get(beam, y) == "^":
                splits += 1
                if beam > 0:
                    x = beam - 1
                    new_beams[x] = new_beams.get(x, 0) + beams[beam]
                if beam < board.size_x - 1:
                    x = beam + 1
                    new_beams[x] = new_beams.get(x, 0) + beams[beam]
            else:
                new_beams[beam] = new_beams.get(beam, 0) + beams[beam]
        beams = new_beams
    return sum(beams.values())


if __name__ == "__main__":
    with open(get_input_name(7, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(7, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
