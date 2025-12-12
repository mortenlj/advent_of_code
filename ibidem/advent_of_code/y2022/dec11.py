#!/usr/bin/env python
import logging
import math
import re
import typing

import alive_progress

from ibidem.advent_of_code.util import get_input_name

MONKEY_PAT = re.compile(r"Monkey (\d+):")
START_PAT = re.compile(r"Starting items: ((?:\d+(?:, )?)+)")
OPERATION_PAT = re.compile(r"Operation: new = (old|\d+) ([+*]) (old|\d+)")
TEST_PAT = re.compile(r"Test: divisible by (\d+)")
TRUE_PAT = re.compile(r"If true: throw to monkey (\d+)")
FALSE_PAT = re.compile(r"If false: throw to monkey (\d+)")


def make_operation(left, op, right):
    if left == right == "old":

        def multiplied_by_itself(item):
            return item * item

        multiplied_by_itself.__doc__ = "is multiplied by itself"
        return multiplied_by_itself
    if op == "+":
        value = int(right)

        def increases_by(item):
            return item + value

        increases_by.__doc__ = f"increases by {value}"
        return increases_by

    if op == "*":
        value = int(right)

        def multiplied_by(item):
            return item * value

        multiplied_by.__doc__ = f"is multiplied by {value}"
        return multiplied_by


class Monkey:
    index: int
    items: list[int]
    operation: typing.Callable
    test_divisor: int
    true_target: int
    false_target: int
    inspected: int

    def __init__(self, index: int, lines: typing.Iterator[str]):
        self.index = index
        self.inspected = 0
        for line in lines:
            if not line.strip():
                return
            line = line.strip()
            if m := START_PAT.match(line):
                self.items = [int(i) for i in m.group(1).split(", ")]
            elif m := OPERATION_PAT.match(line):
                self.operation = make_operation(m.group(1), m.group(2), m.group(3))
            elif m := TEST_PAT.match(line):
                self.test_divisor = int(m.group(1))
            elif m := TRUE_PAT.match(line):
                self.true_target = int(m.group(1))
            elif m := FALSE_PAT.match(line):
                self.false_target = int(m.group(1))

    def inspect(self, worry_level_adjustment):
        while self.items:
            item = self.items.pop(0)
            logging.debug(f"  Monkey inspects an item with a worry level of {item}.")
            item = self.operation(item)
            logging.debug(f"    Worry level {self.operation.__doc__} to {item}.")
            item = worry_level_adjustment(item)
            logging.debug(
                f"    Monkey gets bored with item. Worry level is adjusted to {item}."
            )
            divisible = item % self.test_divisor == 0
            if divisible:
                logging.debug(
                    f"    Current worry level is divisible by {self.test_divisor}."
                )
                target = self.true_target
            else:
                logging.debug(
                    f"    Current worry level is not divisible by {self.test_divisor}."
                )
                target = self.false_target
            logging.debug(f"    Item with worry level 26 is thrown to monkey {target}.")
            self.inspected += 1
            yield item, target


def load(fobj):
    monkeys = []
    for line in fobj:
        if m := MONKEY_PAT.match(line.strip()):
            monkeys.append(Monkey(int(m.group(1)), fobj))
    return monkeys


def play_monkey_round(monkeys, worry_level_adjustment):
    for monkey in monkeys:
        logging.debug(f"Monkey {monkey.index}:")
        for item, target in monkey.inspect(worry_level_adjustment):
            monkeys[target].items.append(item)


def part1(monkeys):
    for _ in range(20):
        play_monkey_round(monkeys, worry_level_adjustment=lambda item: item // 3)
    most_active = list(sorted((m.inspected for m in monkeys), reverse=True))
    return most_active[0] * most_active[1]


def part2(monkeys):
    logging.basicConfig(level=logging.INFO)
    multiplier = math.prod((m.test_divisor for m in monkeys))
    for _ in alive_progress.alive_it(range(10000), total=10000):
        play_monkey_round(
            monkeys, worry_level_adjustment=lambda item: item % multiplier
        )
    most_active = list(sorted((m.inspected for m in monkeys), reverse=True))
    return most_active[0] * most_active[1]


if __name__ == "__main__":
    with open(get_input_name(11, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(11, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
