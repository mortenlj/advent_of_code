#!/usr/bin/env python

import collections
import operator
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
    invalid, _ = find_invalid(input.field_rules, nearby)
    idx = np.where(invalid)
    errors = nearby[idx]
    error_rate = np.sum(errors)
    print(f"Ticket scanning error rate: {error_rate}")
    return error_rate


def find_invalid(field_rules, nearby):
    rule_check = []
    for rule in field_rules:
        rule_check.append(np.logical_or(
            np.logical_and(nearby >= rule.first.start, nearby <= rule.first.end),
            np.logical_and(nearby >= rule.second.start, nearby <= rule.second.end)
        ))
    results = np.logical_not(np.array(rule_check))
    invalid = results.all(axis=0)
    return invalid, results


def find_invalid_tickets(nearby, invalid):
    invalid_rows = invalid.any(axis=1)
    idx = np.where(invalid_rows)
    return nearby[idx]


def find_field_order(field_rules, invalid_tickets, results):
    count = len(invalid_tickets[0])
    possible_fields = _prep_possible_fields(count, field_rules)
    # TODO: Remove results for invalid tickets

    _filter_invalid_rules(field_rules, possible_fields, results)
    return _decide_field_order(field_rules, possible_fields)


def _decide_field_order(field_rules, possible_fields):
    """For each field_idx with a single rule, take note, and remove rule from all others
    Repeat until all field_idx assigned"""
    decided_fields = {}
    while len(decided_fields) < len(field_rules):
        removable = set()
        for idx, options in possible_fields.items():
            if len(options) == 1:
                fieldname = options[0]
                decided_fields[fieldname] = idx
                removable.add(fieldname)
        for fieldname in removable:
            for options in possible_fields.values():
                if fieldname in options:
                    options.remove(fieldname)
    return decided_fields


def _filter_invalid_rules(field_rules, possible_fields, results):
    """For each field_idx, remove rules that have invalid tickets"""
    for layer, rule in enumerate(field_rules):
        invalid_grid = results[layer]
        invalid_idx = np.where(invalid_grid.any(axis=0))
        for idx in invalid_idx[0]:
            possible_fields[idx].remove(rule.fieldname)


def _prep_possible_fields(count, field_rules):
    all_fields = [rule.fieldname for rule in field_rules]
    possible_fields = {}
    for i in range(count):
        possible_fields[i] = all_fields.copy()
    return possible_fields


def part2(input):
    nearby = np.array(input.nearby_tickets)
    invalid, results = find_invalid(input.field_rules, nearby)
    invalid_tickets = find_invalid_tickets(nearby, invalid)
    field_order = find_field_order(input.field_rules, invalid_tickets, results)
    ticket_values = []
    for fieldname, idx in field_order.items():
        if fieldname.startswith("departure"):
            ticket_values.append(input.your_ticket[idx])
    assert len(ticket_values) == 6
    result = map(operator.mul, ticket_values)
    print(f"The final result is {result}")


if __name__ == "__main__":
    input = load()
    part1(input)
    part2(input)
