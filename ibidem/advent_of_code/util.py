#!/usr/bin/env python
# -*- coding: utf-8
import enum
import functools
import time
from dataclasses import dataclass
from importlib import resources

NSEC = 1e9
MSEC = 1e3


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Direction):
            other = other.vector
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, Direction):
            other = other.vector
        return Vector(self.x - other.x, self.y - other.y)

    def distance(self, other):
        if isinstance(other, Direction):
            other = other.vector
        return abs(self.x - other.x) + abs(self.y - other.y)


class Direction(enum.StrEnum):
    Up = ("^", Vector(0, -1))
    North = Up
    Down = ("v", Vector(0, 1))
    South = Down
    Left = ("<", Vector(-1, 0))
    West = Left
    Right = (">", Vector(1, 0))
    East = Right

    def __new__(cls, symbol: str, vector: Vector):
        obj = str.__new__(cls, symbol)
        obj._value_ = symbol
        obj.symbol = symbol
        obj.vector = vector
        return obj

    def reverse(self):
        return {
            Direction.Up: Direction.Down,
            Direction.Down: Direction.Up,
            Direction.Left: Direction.Right,
            Direction.Right: Direction.Left,
        }[self]


def get_input_name(day, year):
    year_dir = resources.files(f"ibidem.advent_of_code.y{year}")
    return year_dir / "data" / f"dec{day:02}.txt"


def format_delta(ns):
    s = int(ns // NSEC)
    ms = ((ns / NSEC) * MSEC) - (s * MSEC)
    return f"{s} seconds, {ms} milliseconds"


def time_this(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time.monotonic_ns()
        try:
            return f(*args, **kwargs)
        finally:
            end = time.monotonic_ns()
            delta = (end - start)
            print(f"Spent {format_delta(delta)} in call")

    return wrapper


def gen_list(f):
    """Make generator function return list"""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return list(f(*args, **kwargs))

    return wrapper
