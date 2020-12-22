#!/usr/bin/env python
from collections import deque

from ibidem.advent_of_code.util import get_input_name


class Player:
    def __init__(self):
        self.deck = deque()

    def add_card(self, value):
        self.deck.append(value)

    def draw(self):
        return self.deck.popleft()

    def has_lost(self):
        return len(self.deck) == 0

    def calculate_score(self):
        score = 0
        for i, card in enumerate(reversed(self.deck)):
            multiplier = i + 1
            score += card * multiplier
        return score


def load():
    player1 = Player()
    player2 = Player()
    p = player1
    with open(get_input_name(22, 2020)) as fobj:
        for line in fobj:
            line = line.strip()
            if not line:
                p = player2
                continue
            if line.startswith("Player"):
                continue
            p.add_card(int(line))
    return player1, player2


def part1(player1, player2):
    while not any((player1.has_lost(), player2.has_lost())):
        c1 = player1.draw()
        c2 = player2.draw()
        if c1 > c2:
            player1.add_card(c1)
            player1.add_card(c2)
        elif c2 > c1:
            player2.add_card(c2)
            player2.add_card(c1)
        else:
            raise ValueError("Players both played the same card!")
    if player1.has_lost():
        result = player2.calculate_score()
        print(f"Player 2 had the winning score: {result}")
    else:
        result = player1.calculate_score()
        print(f"Player 1 had the winning score: {result}")
    return result


def part2():
    pass


if __name__ == "__main__":
    player1, player2 = load()
    part1(player1, player2)
    part2()
