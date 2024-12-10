#!/usr/bin/env python
from collections import defaultdict

import numpy as np

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return Board.from_string(fobj.read(), fill_value=0, dtype=np.int_, growable=False)


def find_scores1(board: Board, summits, start) -> set[tuple[int, int]]:
    current_elevation = board.get(*start)
    if current_elevation == 9:
        return {start}
    local_summits = set()
    for n in board.adjacent_indexes(*start, include_diagonal=False):
        if board.get(*n) == current_elevation + 1:
            if n in summits:
                local_summits |= summits[n]
            else:
                local_summits |= find_scores1(board, summits, n)
    summits[start] = local_summits
    return local_summits


def part1(board: Board):
    summits = defaultdict(set)
    starts = []
    for y in range(board.size_y):
        for x in range(board.size_x):
            if board[y, x] == 0:
                starts.append((y, x))
    for start in starts:
        find_scores1(board, summits, start)
    return sum(len(summits[s]) for s in starts)


def find_scores2(board: Board, scores, start) -> int:
    current_elevation = board.get(*start)
    if current_elevation == 9:
        return 1
    score = 0
    for n in board.adjacent_indexes(*start, include_diagonal=False):
        if board.get(*n) == current_elevation + 1:
            if n in scores:
                score += scores[n]
            else:
                score += find_scores2(board, scores, n)
    scores[start] = score
    return score


def part2(board: Board):
    scores = defaultdict(int)
    starts = []
    for y in range(board.size_y):
        for x in range(board.size_x):
            if board[y, x] == 0:
                starts.append((y, x))
    for start in starts:
        find_scores2(board, scores, start)
    return sum(scores[s] for s in starts)


if __name__ == "__main__":
    with open(get_input_name(10, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(10, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
