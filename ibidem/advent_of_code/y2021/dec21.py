#!/usr/bin/env python
import itertools
import re
from collections import namedtuple

from ibidem.advent_of_code.util import get_input_name

PLAYER_PATTERN = re.compile(r"Player [12] starting position: (\d+)")

Player = namedtuple("Player", ("pos", "score"))


def load(fobj):
    for line in fobj:
        m = PLAYER_PATTERN.search(line)
        assert m
        yield Player(int(m.group(1)), 0)


def move(player, moves):
    newpos = player.pos + moves
    while newpos > 10:
        newpos -= 10
    return Player(newpos, player.score + newpos)


def deterministic_die():
    for i in itertools.cycle(range(100)):
        yield i + 1


def take(n, iterable):
    """Return first n items of the iterable as a list"""
    return list(itertools.islice(iterable, n))


def result(rolls, player):
    return rolls * player.score


def part1(players):
    players = list(players)
    current_player = 0
    rolls = 0
    die = deterministic_die()
    while all(p.score < 1000 for p in players):
        moves = sum(take(3, die))
        rolls += 3
        players[current_player] = move(players[current_player], moves)
        current_player = (current_player + 1) % 2
    if players[0].score >= 1000:
        return result(rolls, players[1])
    else:
        return result(rolls, players[0])


def part2(players):
    return None


if __name__ == "__main__":
    with open(get_input_name(21, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(21, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
