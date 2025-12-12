#!/usr/bin/env python

import numpy as np

from ibidem.advent_of_code.util import get_input_name


def load():
    with open(get_input_name(13, 2020)) as fobj:
        estimate = int(fobj.readline().strip())
        busses = [
            int(v) if v != "x" else None for v in fobj.readline().strip().split(",")
        ]
        return estimate, busses


def part1(estimate, busses):
    busses = np.array([v for v in busses if v])
    factors = estimate / busses
    factors = np.ceil(factors)
    departures = factors * busses
    first_departure_idx = np.argmin(departures)
    first_departure = departures[first_departure_idx]
    first_departing_bus = busses[first_departure_idx]
    waiting_time = first_departure - estimate
    result = waiting_time * first_departing_bus
    print(
        f"The first departing bus is {first_departing_bus}, leaving at {first_departure}.\n"
        f"That is {waiting_time} after the estimated ferry arrival at {estimate}.\n"
        f"This gives a result of {result}."
    )
    return waiting_time, first_departing_bus, result


def is_valid(ts, busses):
    ts_series = np.arange(ts, ts + len(busses))
    mods = np.mod(ts_series, busses) == 0
    return np.all(mods)


def part2(busses, upper_bound=None):
    busses = np.array([v if v else 1 for v in busses])
    ts = busses[0]
    ts_series = np.arange(ts, ts + len(busses))
    mods = np.mod(ts_series, busses) == 0
    while not np.all(mods):
        valid = busses[mods]
        ts += np.multiply.reduce(valid)
        ts_series = np.arange(ts, ts + len(busses))
        mods = np.mod(ts_series, busses) == 0
        if upper_bound and ts > upper_bound:
            raise ValueError(f"timestamp {ts} is above upper bound {upper_bound}")
    print(f"The first possible timestamp is {ts}")
    return ts


if __name__ == "__main__":
    estimate, busses = load()
    part1(estimate, busses)
    part2(busses)
