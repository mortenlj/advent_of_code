#!/usr/bin/env python
# -*- coding: utf-8
import functools
import time

import pkg_resources

NSEC = 1e9
MSEC = 1e3


def get_input_name(day, year):
    return pkg_resources.resource_filename(f"ibidem.advent_of_code.y{year}", f"data/dec{day:02}.txt")


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
