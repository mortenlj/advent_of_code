#!/usr/bin/env python

import re
from abc import ABCMeta, abstractmethod

from ibidem.advent_of_code.util import get_input_name


class Policy(metaclass=ABCMeta):
    def __init__(self, s):
        m = re.match(r"(\d+)-(\d+) ([a-z])", s)
        if m:
            self._a = int(m.group(1))
            self._b = int(m.group(2))
            self.letter = m.group(3)

    @abstractmethod
    def valid(self, password):
        pass

    def __str__(self):
        return f"{self._a}-{self._b} {self.letter}"


class Policy1(Policy):
    def valid(self, password):
        c = password.count(self.letter)
        return self._a <= c <= self._b


class Policy2(Policy):
    def valid(self, password):
        first = password[self._a - 1]
        second = password[self._b - 1]
        return (first == self.letter) != (second == self.letter)


def load(klz):
    with open(get_input_name(2, 2020)) as fobj:
        for line in fobj:
            policy, password = line.strip().split(":")
            yield klz(policy), password.strip()


def execute(klz):
    count = 0
    for policy, password in load(klz):
        if policy.valid(password):
            print(f"Valid: {policy} {password}")
            count += 1
    return count


if __name__ == "__main__":
    print("Part 1: ", execute(Policy1))
    print("Part 2: ", execute(Policy2))
