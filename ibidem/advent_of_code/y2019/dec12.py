#!/usr/bin/env python
# -*- coding: utf-8
import re
from functools import reduce
from multiprocessing import Process, Queue

import math
from vectormath import Vector3

from .util import get_input_name

INPUT_FORMAT = re.compile(r"<x=(.+), y=(.+), z=(.+)>")

MOON_NAMES = ["Io", "Europa", "Ganymede", "Callisto"]


class Vector(Vector3):
    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y and self.z == other.z
        except AttributeError:
            return False

    def energy(self):
        return sum((abs(v) for v in (self.x, self.y, self.z)))

    def __str__(self):
        return "<x={:2.0f}, y={:2.0f}, z={:2.0f}>".format(self.x, self.y, self.z)


class Moon(object):
    def __init__(self, name, x, y, z, vel=None):
        self.name = name
        self.pos = Vector(x, y, z)
        if vel is not None:
            self.vel = vel
        else:
            self.vel = Vector(0, 0, 0)

    def energy(self):
        return self.pos.energy() * self.vel.energy()

    def apply_gravity(self, other, axis=None):
        if other == self:
            return
        if axis == "x" or axis is None:
            self.vel.x += self._get_adjustment(self.pos.x, other.pos.x)
        if axis == "y" or axis is None:
            self.vel.y += self._get_adjustment(self.pos.y, other.pos.y)
        if axis == "z" or axis is None:
            self.vel.z += self._get_adjustment(self.pos.z, other.pos.z)

    def apply_velocity(self, axis=None):
        if axis is None:
            self.pos += self.vel
        else:
            old_value = getattr(self.pos, axis)
            adjustment = getattr(self.vel, axis)
            new_value = old_value + adjustment
            setattr(self.pos, axis, new_value)

    def __repr__(self):
        return "Moon(name={}, pos={}, vel={})".format(self.name, self.pos, self.vel)

    def __str__(self):
        return "pos={}, vel={}".format(self.pos, self.vel)

    def __eq__(self, other):
        try:
            return self.name == other.name and self.pos == other.pos and self.vel == other.vel
        except AttributeError:
            return False

    @staticmethod
    def _get_adjustment(mine, other):
        if mine < other:
            return 1
        if other < mine:
            return -1
        return 0


def load_input(lines):
    moons = []
    for i, line in enumerate(lines):
        name = MOON_NAMES[i]
        m = INPUT_FORMAT.match(line.strip())
        if not m:
            raise ValueError("Couldn't parse line: {!r}".format(line))
        moons.append(Moon(name, int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return moons


def perform_step(moons, axis=None):
    for moon in moons:
        for other in moons:
            moon.apply_gravity(other, axis)
    for moon in moons:
        moon.apply_velocity(axis)


def simulate(moons, steps):
    print("After 0 steps:")
    for moon in moons:
        print(moon)
    for step in range(steps):
        perform_step(moons)
        if steps <= 10 or (step + 1) % 10 == 0:
            print("After {} steps:".format(step + 1))
            for moon in moons:
                print(moon)
            print()
    total_energy = sum(m.energy() for m in moons)
    print("Total energy in the system after {} steps: {}".format(steps, total_energy))


def get_state(moons, axis):
    return tuple([(getattr(m.pos, axis), getattr(m.vel, axis)) for m in moons])


def find_axis_cycle(axis, moons, out):
    seen = {get_state(moons, axis): True}
    steps = 0
    while True:
        perform_step(moons, axis)
        steps += 1
        state = get_state(moons, axis)
        if seen.get(state, False):
            print("Axis {} repeats after {} steps, with state {}".format(axis, steps, state))
            out.put(steps)
            return
        seen[state] = True


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def find_cycle(moons):
    results = {}
    processes = []
    for axis in ("x", "y", "z"):
        results[axis] = Queue()
        process = Process(target=find_axis_cycle, args=(axis, moons, results[axis]))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    values = [r.get_nowait() for r in results.values()]
    return reduce(lcm, values)


def part1():
    with open(get_input_name("dec12")) as fobj:
        moons = load_input(fobj)
        simulate(moons, 1000)


def part2():
    with open(get_input_name("dec12")) as fobj:
        moons = load_input(fobj)
        cycle_interval = find_cycle(moons)
        print("These moons will cycle after {} steps".format(cycle_interval))


if __name__ == "__main__":
    part2()
