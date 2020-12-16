#!/usr/bin/env python

import collections
import re

import numpy as np

from ibidem.advent_of_code.util import get_input_name

Input = collections.namedtuple("Input", ("fieldname", "first", "second"))
Range = collections.namedtuple("Range", ("start", "end"))


class Reader():
    RULE = re.compile(r"(?P<fieldname>[a-z _-]+): (?P<first_start>\d+)-(?P<first_end>\d+) or "
                      r"(?P<second_start>\d+)-(?P<second_end>\d+)")
    YOUR_HEADER = re.compile(r"your ticket:")
    NEARBY_HEADER = re.compile(r"nearby tickets:")

    def __init__(self):
        self.field_rules = []
        self.your_ticket = None
        self.nearby_tickets = []
        self.read = self._read_rules
        self._read_your_ticket_header = False
        self._read_nearby_tickets_header = False

    def _read_rules(self, line):
        m = self.RULE.match(line)
        if m:
            first = Range(int(m.group("first_start")), int(m.group("first_end")))
            second = Range(int(m.group("second_start")), int(m.group("second_end")))
            self.field_rules.append(Input(m.group("fieldname"), first, second))
        else:
            self.read = self._read_your_ticket

    def _read_your_ticket(self, line):
        if self._read_your_ticket_header:
            self.your_ticket = self._read_ticket(line)
            self.read = self._read_nearby_tickets
        else:
            m = self.YOUR_HEADER.match(line)
            if m:
                self._read_your_ticket_header = True

    def _read_nearby_tickets(self, line):
        if self._read_nearby_tickets_header:
            self.nearby_tickets.append(self._read_ticket(line))
        else:
            m = self.NEARBY_HEADER.match(line)
            if m:
                self._read_nearby_tickets_header = True

    @staticmethod
    def _read_ticket(line):
        return [int(v) for v in line.split(",")]


def load():
    reader = Reader()
    with open(get_input_name(16, 2020)) as fobj:
        for line in fobj:
            line = line.strip()
            reader.read(line)
    return reader


def part1(input):
    nearby = np.array(input.nearby_tickets)
    rule_check = []
    for rule in input.field_rules:
        rule_check.append(np.logical_or(
            np.logical_and(nearby >= rule.first.start, nearby <= rule.first.end),
            np.logical_and(nearby >= rule.second.start, nearby <= rule.second.end)
        ))
    results = np.logical_not(np.array(rule_check))
    invalid = results.all(axis=0)
    idx = np.where(invalid)
    errors = nearby[idx]
    error_rate = np.sum(errors)
    print(f"Ticket scanning error rate: {error_rate}")
    return error_rate


def part2(input):
    pass


if __name__ == "__main__":
    input = load()
    part1(input)
    part2(input)
