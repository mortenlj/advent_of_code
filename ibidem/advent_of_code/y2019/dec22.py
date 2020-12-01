#!/usr/bin/env python
# -*- coding: utf-8
import re

import numpy as np

from .util import get_input_name


class DealToNew(object):
    pattern = re.compile(r"deal into new stack")

    def __init__(self, m):
        pass

    def __call__(self, deck):
        return np.flip(deck)


class Cut(object):
    pattern = re.compile(r"cut (.*)")

    def __init__(self, m):
        self._n = int(m.group(1)) * -1

    def __call__(self, deck):
        return np.roll(deck, self._n)


class DealWithInc(object):
    pattern = re.compile(r"deal with increment (.*)")

    def __init__(self, m):
        self._n = int(m.group(1))

    def __call__(self, deck):
        dst = np.zeros(deck.shape, dtype=deck.dtype)
        src_idx = dst_idx = 0
        deck_length = len(deck)
        while src_idx < deck_length:
            dst[dst_idx] = deck[src_idx]
            dst_idx = (dst_idx + self._n) % deck_length
            src_idx += 1
        return dst


TECHNIQUES = (DealToNew, Cut, DealWithInc)


class Shuffler(object):
    def __init__(self, shuffle_algo, deck):
        self.moves = self._parse(shuffle_algo)
        self.deck = deck

    def _parse(self, algo):
        moves = []
        for line in algo:
            for t in TECHNIQUES:
                m = t.pattern.search(line)
                if m:
                    moves.append(t(m))
        return moves

    def shuffle(self):
        for move in self.moves:
            self.deck = move(self.deck)


def part1():
    with open(get_input_name("dec22")) as fobj:
        deck = np.arange(10007, dtype=np.int16)
        shuffler = Shuffler(fobj, deck)
        shuffler.shuffle()
        result = np.where(shuffler.deck == 2019)
        print("Card 2019 is in position {}".format(result[0][0]))


def part2():
    with open(get_input_name("dec22")) as fobj:
        deck = np.arange(119315717514047, dtype=np.int16)
        shuffler = Shuffler(fobj, deck)
        for _ in range(101741582076661):
            shuffler.shuffle()
        print("The card in position 2020 is {}".format(shuffler.deck[2020]))


if __name__ == "__main__":
    part1()
    part2()
