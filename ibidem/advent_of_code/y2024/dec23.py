#!/usr/bin/env python
import networkx as nx
from networkx.classes import Graph

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    G = nx.Graph()
    for line in fobj:
        a, b = line.strip().split("-")
        G.add_edge(a, b)
    return G


def part1(graph: Graph):
    count = 0
    for clique in nx.enumerate_all_cliques(graph):
        if len(clique) < 3:
            continue
        if len(clique) > 3:
            break
        for node in clique:
            if node.startswith("t"):
                count += 1
                break
    return count


def part2(graph: Graph):
    max_clique = max(nx.enumerate_all_cliques(graph), key=len)
    return ",".join(sorted(max_clique))


if __name__ == "__main__":
    with open(get_input_name(23, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(23, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
