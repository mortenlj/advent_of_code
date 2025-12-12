#!/usr/bin/env python
from dataclasses import dataclass

from ibidem.advent_of_code.util import get_input_name, gen_list


@dataclass
class Card:
    count: int
    winning: set
    owned: set

    def lotto(self):
        return self.winning.intersection(self.owned)


@gen_list
def load(fobj):
    for line in fobj:
        line = line.strip()
        prefix, data = line.split(": ", maxsplit=1)
        winning_part, owned_part = data.split(" | ", maxsplit=1)
        winning = set(int(x) for x in winning_part.split())
        owned = set(int(x) for x in owned_part.split())
        yield Card(1, winning, owned)


def part1(input):
    result = 0
    for card in input:
        result += int(pow(2, len(card.lotto()) - 1))
    return result


def part2(input):
    for i, card in enumerate(input):
        for j in range(len(card.lotto())):
            input[i + 1 + j].count += card.count
    return sum(card.count for card in input)


if __name__ == "__main__":
    with open(get_input_name(4, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(4, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
