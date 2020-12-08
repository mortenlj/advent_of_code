#!/usr/bin/env python
# -*- coding: utf-8
import itertools
from collections import defaultdict

from colorama import Fore
from numpy import pi
from vectormath import Vector2

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name

COLORS = [a for a in dir(Fore) if a.isupper() and a not in ("RESET", "BLACK", "LIGHTWHITE_EX", "WHITE")]
STYLES = [(getattr(Fore, color), char) for char in "#@¤+*%$<>XOABCDEFGHIJKLMNPRSTUVWYZ" for color in COLORS]
SENTINEL = object()
UP = Vector2(0, -1)


class Asteroid(object):
    def __init__(self, x, y, color=Fore.LIGHTWHITE_EX, char="#"):
        self.x = x
        self.y = y
        self.color = color
        self.char = char
        self.lines_of_sight = defaultdict(list)

    def vector_to(self, other):
        if other == self:
            return None
        opp = other.y - self.y
        adj = other.x - self.x
        return Vector2(adj, opp)

    def add(self, other):
        vector = self.vector_to(other)
        self.lines_of_sight[vector.theta].append((vector, other))
        self.lines_of_sight[vector.theta].sort(key=lambda d: d[0].length, reverse=True)

    def set_style(self, color, char):
        self.color = color
        self.char = char

    def __str__(self):
        return self.color + self.char

    def __repr__(self):
        return "Asteroid({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except AttributeError:
            return False


def part1():
    with open(get_input_name(10, 2019)) as fobj:
        lines = fobj.readlines()
    best, board, count = solve_map(lines)
    present_result(best, board, count)
    return best, board


def solve_map(lines):
    asteroids, board = load_map(lines)
    results = calculate_lines_of_sight(asteroids)
    best, count = find_winner(results)
    return best, board, count


def find_winner(results):
    count, best = sorted(results, key=lambda x: x[0], reverse=True)[0]
    return best, count


def present_result(best, board, count):
    print("{!r} can see {} other asteroids".format(best, count))
    for i, theta in enumerate(sorted(best.lines_of_sight)):
        for _, asteroid in best.lines_of_sight[theta]:
            asteroid.set_style(*STYLES[i])
    board.print()
    print(Fore.RESET)


def calculate_lines_of_sight(asteroids):
    results = []
    for a in asteroids:
        for other in asteroids:
            if other == a:
                continue
            a.add(other)
            results.append((len(a.lines_of_sight), a))
    return results


def load_map(lines):
    board = Board(len(lines[0]), len(lines), do_translate=False)
    asteroids = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c == "#":
                asteroid = Asteroid(x, y)
                asteroids.append(asteroid)
                board.set(x, y, asteroid)
    board.print()
    return asteroids, board


def part2(station, board):
    vectors = [d[0][0] for d in station.lines_of_sight.values()]
    firing_order = decide_firing_order(vectors)
    count = 0
    for target in shoot(firing_order, station, board):
        vaporize(board, target)
        count += 1
        if count == 200:
            print("{!r} was the 200th asteroid vaporized. Its value is {}".format(target, target.x*100+target.y))
            break


def shoot(firing_order, station, board):
    count_last_rotation = 0
    firing_order.append(SENTINEL)
    for theta in itertools.cycle(firing_order):
        if theta == SENTINEL:
            print("Completed one rotation, killed {} objects this round".format(count_last_rotation))
            board.print()
            if count_last_rotation == 0:
                break
            count_last_rotation = 0
            continue
        targets = station.lines_of_sight[theta]
        if targets:
            _, target = targets.pop()
            yield target
            count_last_rotation += 1


def vaporize(board, target):
    board.set(target.x, target.y, Fore.LIGHTWHITE_EX + "💣")
    print("Vaporized {!r}".format(target))
    board.print()
    board.set(target.x, target.y, Fore.RESET + " ")
    return target


def decide_firing_order(vectors):
    vectors.sort(key=angle_sort)
    angles = [angle_sort(v) for v in vectors]
    firing_order = [v.theta for v in vectors]
    return firing_order


def angle_sort(v):
    angle = v.theta - UP.theta
    if angle < 0:
        angle += 2*pi
    return angle


if __name__ == "__main__":
    best, board = part1()
    part2(best, board)
