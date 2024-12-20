from functools import total_ordering
from typing import Iterable

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.util import Vector
from ibidem.advent_of_code.visualizer import initialize_and_display_splash, Tiles, Sprites, Colors
from ibidem.advent_of_code.visualizer.board import BoardVisualizer


@total_ordering
class Node:
    """Node represents a position on the grid, and must be hashable

    This is a basic Node implementation, for special handling, override the methods
    """
    _pos: Vector

    def __init__(self, pos: Vector):
        self._pos = pos

    def __repr__(self):
        return f"Node({self._pos})"

    def __hash__(self):
        return hash(self._pos)

    def __eq__(self, other):
        return self._pos == other._pos

    def __lt__(self, other):
        return self._pos < other._pos

    @property
    def pos(self) -> Vector:
        return self._pos

    @property
    def current_symbol(self) -> str:
        return "S"

    def neighbors(self, board: Board) -> Iterable["Node"]:
        for nx, ny in board.adjacent_indexes(self.pos.x, self.pos.y, include_diagonal=False):
            if board.get(nx, ny) != "#":
                yield Node(Vector(nx, ny))

    def cost_to(self, target) -> int:
        if hasattr(target, "pos"):
            return self.pos.distance(target.pos)
        return self.pos.distance(target)


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path


def a_star(start: Node, goal: Vector, board: Board):
    """A* finds a path from start to goal"""

    initialize_and_display_splash()
    sprite_mapping = {
        ".": Tiles.Grass, "#": Tiles.Wall,
        "X": Tiles.Stone, "O": Tiles.Dirt,
        "S": Sprites.Tank, "E": Sprites.Tombstone,
        "R": Colors.Red,
    }
    visualizer = BoardVisualizer(board, sprite_mapping)

    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    open_set = set()

    def add_to_open_set(node: Node):
        open_set.add(node)
        visualizer.draw_single(node.pos.x, node.pos.y, "O")

    add_to_open_set(start)

    # For node n, came_from[n] is the node immediately preceding it on the cheapest path from the start to n currently known.
    came_from = {}

    # For node n, g_score[n] is the currently known cost of the cheapest path from start to n.
    g_score = {}

    def add_g_score(node: Node, score):
        g_score[node] = score
        visualizer.draw_single(node.pos.x, node.pos.y, "O")

    add_g_score(start, 0)

    # For node n, f_score[n] := g_score[n] + h(n). f_score[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    f_score = {start: start.cost_to(goal)}

    visualizer.pause()

    current = None
    while open_set:
        if current:
            visualizer.draw_single(current.pos.x, current.pos.y, "X")
        # This operation can occur in O(Log(N)) time if open_set is a min-heap or a priority queue
        current = min(open_set, key=lambda x: f_score[x])
        visualizer.draw_single(current.pos.x, current.pos.y, current.current_symbol)
        if current.pos == goal:
            path = reconstruct_path(came_from, current)
            for node in path:
                visualizer.draw_single(node.pos.x, node.pos.y, "R")
            visualizer.pause()
            return g_score[current], path
        open_set.remove(current)
        for neighbor in current.neighbors(board):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_g_score is the distance from start to the neighbor through current
            tentative_g_score = g_score.get(current, float("inf")) + current.cost_to(neighbor)
            if tentative_g_score < g_score.get(neighbor, float("inf")):
                # This path to neighbor is better than any previous one. Record it!
                came_from[neighbor] = current
                if neighbor not in open_set:
                    add_to_open_set(neighbor)
                add_g_score(neighbor, tentative_g_score)
                f_score[neighbor] = tentative_g_score + neighbor.cost_to(goal)
        visualizer.flip()
    visualizer.pause()
    # Open set is empty but goal was never reached
    return float("inf"), None
