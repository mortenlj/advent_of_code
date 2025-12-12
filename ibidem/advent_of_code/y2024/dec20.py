#!/usr/bin/env python
from rich.progress import track

from ibidem.advent_of_code.a_star import a_star, Node
from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import get_input_name, Vector


def load(fobj):
    return Board.from_string(fobj.read())


def part1(board: Board, cutoff):
    start_y, start_x = board.find("S")[0]
    goal_y, goal_x = board.find("E")[0]

    shortcuts = []

    start = Node(Vector(start_x, start_y))
    goal = Node(Vector(goal_x, goal_y))
    _, path = a_star(start, goal.pos, board)

    pos_to_idx = {pos: idx for idx, pos in enumerate(reversed(path))}
    for node in track(path):
        for j in (-1, 0, 1):
            for i in (-1, 0, 1):
                if i == j == 0:
                    continue
                if i != 0 and j != 0:
                    continue
                nx, ny = node.pos.x + i, node.pos.y + j
                nnx, nny = node.pos.x + 2 * i, node.pos.y + 2 * j
                if nx < 0 or ny < 0 or nnx < 0 or nny < 0:
                    continue
                if (
                    nx >= board.size_x
                    or ny >= board.size_y
                    or nnx >= board.size_x
                    or nny >= board.size_y
                ):
                    continue
                other = Node(Vector(nnx, nny))
                if (
                    board.get(nx, ny) == "#"
                    and board.get(nnx, nny) in (".", "E")
                    and other in path
                    and pos_to_idx[other] > pos_to_idx[node]
                ):
                    savings = pos_to_idx[other] - pos_to_idx[node] - 2
                    if savings >= cutoff:
                        shortcuts.append((node, other))
    good_shortcuts = len(shortcuts)
    print(f"Found {good_shortcuts} good shortcuts")
    return good_shortcuts


def part2(board: Board, cutoff):
    start_y, start_x = board.find("S")[0]
    goal_y, goal_x = board.find("E")[0]

    shortcuts = []

    start = Node(Vector(start_x, start_y))
    goal = Node(Vector(goal_x, goal_y))
    _, path = a_star(start, goal.pos, board)

    path = list(reversed(path))
    pos_to_idx = {pos: idx for idx, pos in enumerate(path)}
    for i, node in track(enumerate(path), total=len(path)):
        for other in path[i + cutoff :]:
            distance = node.pos.distance(other.pos)
            if distance <= 20:
                savings = pos_to_idx[other] - pos_to_idx[node] - distance
                if savings >= cutoff:
                    shortcuts.append((node, other))
    good_shortcuts = len(shortcuts)
    print(f"Found {good_shortcuts} good shortcuts")
    return good_shortcuts


if __name__ == "__main__":
    with open(get_input_name(20, 2024)) as fobj:
        p1_result = part1(load(fobj), 100)
        print(f"Part 1: {p1_result}")
    with open(get_input_name(20, 2024)) as fobj:
        p2_result = part2(load(fobj), 100)
        print(f"Part 2: {p2_result}")
