#!/usr/bin/env python
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    g = nx.Graph()
    for line in fobj:
        line = line.strip()
        source, targets = line.split(':')
        for target in targets.split():
            g.add_edge(source, target)
    return g


def part1(graph):
    nx.draw(graph)
    plt.show()
    cutset = nx.minimum_edge_cut(graph)
    graph.remove_edges_from(cutset)
    nx.draw(graph)
    plt.show()
    return np.prod([len(g) for g in nx.connected_components(graph)])


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name(25, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(25, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
