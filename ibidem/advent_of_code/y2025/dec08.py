#!/usr/bin/env python
import itertools
from heapq import heapify_max, heappush_max, heappushpop_max, heapify, heappop
from math import prod

from alive_progress import alive_it
from vectormath import Vector3, Vector3Array

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    vectors = []
    for line in fobj:
        line = line.strip()
        x, y, z = (int(c) for c in line.split(","))
        vectors.append(Vector3(x, y, z))
    return Vector3Array(vectors)


def distances(vectors, num_distances):
    heap = []
    heapify_max(heap)
    count = 0
    for v1, v2 in alive_it(itertools.combinations(vectors, 2)):
        distance = Vector3(v1 - v2).length
        entry = (distance, tuple(int(x) for x in v1), tuple(int(x) for x in v2))
        if count < num_distances:
            heappush_max(heap, entry)
            count += 1
        else:
            heappushpop_max(heap, entry)
    return heap


def part1(vectors, num_distances=1000):
    heap = distances(vectors, num_distances)
    circuits = {}
    for _d, v1, v2 in heap:
        l1 = circuits.get(v1, {v1})
        l2 = circuits.get(v2, {v2})
        circuit = l1 | l2
        for v in circuit:
            circuits[v] = circuit
    scv = sorted(set(tuple(v) for v in circuits.values()), key=len, reverse=True)
    three_longest = itertools.islice(scv, 3)
    return prod(len(c) for c in three_longest)


def all_distances(vectors):
    heap = []
    heapify_max(heap)
    for v1, v2 in alive_it(itertools.combinations(vectors, 2)):
        distance = Vector3(v1 - v2).length
        entry = (distance, tuple(int(x) for x in v1), tuple(int(x) for x in v2))
        heappush_max(heap, entry)
    return heap


def part2(vectors):
    len_vectors = len(vectors)
    heap = all_distances(vectors)
    heapify(heap)
    circuits = {}
    while heap:
        _, v1, v2 = heappop(heap)
        l1 = circuits.get(v1, {v1})
        l2 = circuits.get(v2, {v2})
        circuit = l1 | l2
        if len(circuit) == len_vectors:
            break
        for v in circuit:
            circuits[v] = circuit
    return v1[0] * v2[0]


if __name__ == "__main__":
    with open(get_input_name(8, 2025)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(8, 2025)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
