#!/usr/bin/env python
from collections import defaultdict

import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


class Plot:
    name: str
    counter: int
    parcels: set

    def __init__(self, name, counter, first):
        self.name = name
        self.counter = counter
        self.parcels = {first}

    def add(self, parcel):
        self.parcels.add(parcel)

    def area(self):
        return len(self.parcels)

    def perimeter(self, perimeters):
        return sum(perimeters.get(x, y) for x, y in self.parcels)



def load(fobj):
    return Board.from_string(fobj.read(), growable=False)

def part1(board: Board):
    perimeters = Board(size_x=board.size_x + 1, size_y=board.size_y + 1,
                       do_translate=False, flip=False, fill_value=4,
                       dtype=np.int_, growable=False)
    start_x, start_y = board.size_x, board.size_y
    unclaimed = set()
    for y in range(start_y):
        for x in range(start_x):
            unclaimed.add((x, y))
            plot_name = board.get(x, y)
            if x + 1 < start_x:
                right_coord = (x + 1, y)
                if board.get(*right_coord) == plot_name:
                    perimeters.set(x, y, perimeters.get(x, y) - 1)
                    perimeters.set(*right_coord, perimeters.get(*right_coord) - 1)
            if y + 1 < start_y:
                down_coord = (x, y + 1)
                if board.get(*down_coord) == plot_name:
                    perimeters.set(x, y, perimeters.get(x, y) - 1)
                    perimeters.set(*down_coord, perimeters.get(*down_coord) - 1)

    plot_name_counters = defaultdict(int)
    plots = []
    while unclaimed:
        parcel = unclaimed.pop()
        plot_name = board.get(*parcel)
        plot_name_counters[plot_name] += 1
        plot_idx = plot_name_counters[plot_name]
        plot = Plot(plot_name, plot_idx, parcel)
        plots.append(plot)
        map_plot(board, parcel, plot, unclaimed)

    total_price = 0
    for plot in plots:
        perimeter = plot.perimeter(perimeters)
        print(f"Perimeter of {plot.name}: {perimeter}")
        area = plot.area()
        print(f"Area of {plot.name}: {area}")
        price = perimeter * area
        print(f"Price of fencing for {plot.name}: {price}")
        total_price += price
    return total_price


def map_plot(board, parcel, plot, unclaimed):
    for nx, ny in board.adjacent_indexes(*parcel, include_diagonal=False):
        if board.get(nx, ny) == plot.name and (nx, ny) in unclaimed:
            unclaimed.remove((nx, ny))
            plot.add((nx, ny))
            map_plot(board, (nx, ny), plot, unclaimed)


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(12, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(12, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
