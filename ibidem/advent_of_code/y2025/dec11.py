#!/usr/bin/env python
import networkx as nx
from rich.progress import track

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


def part2(G: nx.Graph):
    paths = nx.all_simple_paths(G, "svr", "out")
    count = 0
    for path in track(paths, description="Generating paths"):
        path = frozenset(path)
        if "dac" in path and "fft" in path:
            print(f"{path=} has both dac and fft")
            count += 1
    return count


if __name__ == "__main__":
    with open(get_input_name(11, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(11, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
