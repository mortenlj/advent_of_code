#!/usr/bin/env python
# -*- coding: utf-8
import functools
import time
from importlib import resources

NSEC = 1e9
MSEC = 1e3


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
