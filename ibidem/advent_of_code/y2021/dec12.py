#!/usr/bin/env python

import networkx

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    G = networkx.Graph()
    for line in fobj:
        u, v = line.strip().split("-")
        G.add_edge(u, v)
    return G


def all_paths(G):
    cutoff = len(G) * 10
    source = "start"
    target = "end"
    visited = [source]
    stack = [iter(G[source])]
    while stack:
        children = stack[-1]
        child = next(children, None)
        if child is None:
            stack.pop()
            visited.pop()
        elif len(visited) < cutoff:
            if child in visited and child == child.lower():
                continue
            if child == target:
                yield tuple(visited + [child])
            visited.append(child)
            if target not in visited:  # expand stack until find all targets
                stack.append(iter(G[child]))
            else:
                visited.pop()  # maybe other ways to child
        else:  # len(visited) == cutoff:
            stack.pop()
            visited.pop()


def part1(G: networkx.Graph):
    paths = list(all_paths(G))
    for p in paths:
        print(",".join(p))
    return len(paths)


def part2(G: networkx.Graph):
    small_caves = [n for n in G.nodes if n.islower()]
    paths = set()
    for cave in small_caves:
        if cave in ("start", "end"):
            continue
        neighbors = G.neighbors(cave)
        g = G.copy()
        cave_alt = cave + "*"
        for n in neighbors:
            g.add_edge(cave_alt, n)
        for path in all_paths(g):
            actual_path = tuple(c[:-1] if "*" in c else c for c in path)
            paths.add(actual_path)
    for p in paths:
        print(",".join(p))
    return len(paths)


if __name__ == "__main__":
    with open(get_input_name(12, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(12, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
