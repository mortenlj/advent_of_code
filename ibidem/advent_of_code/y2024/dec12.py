#!/usr/bin/env python
from collections import defaultdict
from dataclasses import dataclass

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
        return sum(perimeters.get(x, y).perimeters for x, y in self.parcels)

    def sides(self, perimeters):
        return sum(perimeters.get(x, y).corners() for x, y in self.parcels)


@dataclass
class Parcel:
    tl: int = 1
    tr: int = 1
    bl: int = 1
    br: int = 1

    perimeters: int = 4

    def corners(self):
        return self.tl + self.tr + self.bl + self.br


def load(fobj):
    return Board.from_string(fobj.read(), growable=False)


def solve(board: Board):
    perimeters = Board(size_x=board.size_x + 1, size_y=board.size_y + 1,
                       do_translate=False, flip=False, fill_value=None,
                       dtype=Parcel, growable=False)
    start_x, start_y = board.size_x, board.size_y
    unclaimed = set()
    for y in range(start_y):
        for x in range(start_x):
            unclaimed.add((x, y))
            parcel = _get_perimeter_parcel(perimeters, x, y)
            plot_name = board.get(x, y)
            if x + 1 < start_x:
                right_coord = (x + 1, y)
                if board.get(*right_coord) == plot_name:
                    right_parcel = _get_perimeter_parcel(perimeters, *right_coord)
                    _join_right(parcel, right_parcel)
            if y + 1 < start_y:
                down_coord = (x, y + 1)
                if board.get(*down_coord) == plot_name:
                    down_parcel = _get_perimeter_parcel(perimeters, *down_coord)
                    _join_down(parcel, down_parcel)

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
    bulk_price = 0
    for plot in plots:
        perimeter = plot.perimeter(perimeters)
        print(f"Perimeter of {plot.name}: {perimeter}")
        sides = plot.sides(perimeters)
        print(f"Sides of {plot.name}: {sides}")
        area = plot.area()
        print(f"Area of {plot.name}: {area}")
        price = perimeter * area
        print(f"Price of fencing for {plot.name}: {price}")
        discounted_price = sides * area
        print(f"Discounted price of fencing for {plot.name}: {discounted_price}")
        total_price += price
        bulk_price += discounted_price
    return total_price, bulk_price


def _join_down(parcel, down_parcel):
    parcel.perimeters -= 1
    down_parcel.perimeters -= 1

    down_parcel.tl = (parcel.bl + down_parcel.tl) % 2
    parcel.bl = 0
    down_parcel.tr = (parcel.br + down_parcel.tr) % 2
    parcel.br = 0


def _join_right(parcel, right_parcel):
    parcel.perimeters -= 1
    right_parcel.perimeters -= 1

    right_parcel.tl = (parcel.tr + right_parcel.tl) % 2
    parcel.tr = 0
    right_parcel.bl = (parcel.br + right_parcel.bl) % 2
    parcel.br = 0


def _get_perimeter_parcel(perimeters, x, y):
    parcel = perimeters.get(x, y)
    if parcel is None:
        parcel = Parcel()
        perimeters.set(x, y, parcel)
    return parcel


def map_plot(board, parcel, plot, unclaimed):
    for nx, ny in board.adjacent_indexes(*parcel, include_diagonal=False):
        if board.get(nx, ny) == plot.name and (nx, ny) in unclaimed:
            unclaimed.remove((nx, ny))
            plot.add((nx, ny))
            map_plot(board, (nx, ny), plot, unclaimed)


if __name__ == "__main__":
    with open(get_input_name(12, 2024)) as fobj:
        p1_result, p2_result = solve(load(fobj))
        print(f"Part 1: {p1_result}")
        print(f"Part 2: {p2_result}")
