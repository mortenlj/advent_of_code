#!/usr/bin/env python
import re

from ibidem.advent_of_code.util import get_input_name


class Hand:
    RED = re.compile("(\d+) red")
    BLUE = re.compile("(\d+) blue")
    GREEN = re.compile("(\d+) green")

    def __init__(self, part):
        self.red = self._parse(self.RED, part)
        self.blue = self._parse(self.BLUE, part)
        self.green = self._parse(self.GREEN, part)

    def _parse(self, pattern, part):
        if match := pattern.search(part):
            return int(match.group(1))
        return 0

    def subsetof(self, other):
        return self.red <= other.red and self.blue <= other.blue and self.green <= other.green

    def power(self):
        return self.red * self.blue * self.green


class Game:
    GAME = re.compile("Game (\d+): (.*)")

    def __init__(self, line):
        match = self.GAME.search(line)
        self.id = int(match.group(1))
        self.draws = [Hand(part) for part in match.group(2).split("; ")]


def load(fobj):
    for line in fobj:
        yield Game(line)


def part1(input):
    PART1_HAND = Hand("12 red, 13 green, 14 blue")
    return sum(game.id for game in input if all(draw.subsetof(PART1_HAND) for draw in game.draws))


def part2(input):
    result = 0
    for game in input:
        minimum = Hand("")
        for draw in game.draws:
            if draw.subsetof(minimum):
                continue
            minimum.red = max(minimum.red, draw.red)
            minimum.blue = max(minimum.blue, draw.blue)
            minimum.green = max(minimum.green, draw.green)
        result += minimum.power()
    return result


if __name__ == "__main__":
    with open(get_input_name(2, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(2, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
