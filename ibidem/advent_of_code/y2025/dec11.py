#!/usr/bin/env python
from functools import cache

import networkx as nx

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    G = nx.DiGraph()
    for line in fobj:
        node, outputs = line.strip().split(":")
        for output in outputs.split():
            G.add_edge(node, output)
    return G


def part1(G: nx.Graph):
    paths = nx.all_simple_paths(G, "you", "out")
    return len(list(paths))


@cache
def count(start: str, G: nx.Graph, have_fft: bool = False, have_dac: bool = False) -> int:
    next_nodes = list(G.neighbors(start))
    if "out" in next_nodes and have_dac and have_fft:
        return 1
    elif "out" in next_nodes:
        return 0
    if start == "fft":
        have_fft = True
    elif start == "dac":
        have_dac = True
    path_count = 0
    for node in next_nodes:
        path_count += count(node, G, have_fft, have_dac)
    return path_count


def part2(G: nx.Graph):
    assert nx.is_directed_acyclic_graph(G)
    return count("svr", G)


if __name__ == "__main__":
    with open(get_input_name(11, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(11, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
