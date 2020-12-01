#!/usr/bin/env python
# -*- coding: utf-8

import pytest
from vectormath import Vector2

from ..dec10 import solve_map, present_result, Asteroid, decide_firing_order, shoot

BIG_MAP = [".#..##.###...#######",
           "##.############..##.",
           ".#.######.########.#",
           ".###.#######.####.#.",
           "#####.##.#.##.###.##",
           "..#####..#.#########",
           "####################",
           "#.####....###.#.#.##",
           "##.#################",
           "#####.##.###..####..",
           "..######..##.#######",
           "####.##.####...##..#",
           ".#####..#.######.###",
           "##...#.##########...",
           "#.##########.#######",
           ".####.#.###.###.#.##",
           "....##.##.###..#####",
           ".#.#.###########.###",
           "#.#.#.#####.####.###",
           "###.##.####.##.#..##"]


@pytest.mark.parametrize("lines, count, best", (
        ([".#..#",
          ".....",
          "#####",
          "....#",
          "...##"], 8, Asteroid(3, 4)),
        (["......#.#.",
          "#..#.#....",
          "..#######.",
          ".#.#.###..",
          ".#..#.....",
          "..#....#.#",
          "#..#....#.",
          ".##.#..###",
          "##...#..#.",
          ".#....####"], 33, Asteroid(5, 8)),
        (["#.#...#.#.",
          ".###....#.",
          ".#....#...",
          "##.#.#.#.#",
          "....#.#.#.",
          ".##..###.#",
          "..#...##..",
          "..##....##",
          "......#...",
          ".####.###."], 35, Asteroid(1, 2)),
        ([".#..#..###",
          "####.###.#",
          "....###.#.",
          "..###.##.#",
          "##.##.#.#.",
          "....###..#",
          "..#.#..#.#",
          "#..#.#.###",
          ".##...##.#",
          ".....#.#.."], 41, Asteroid(6, 3)),
        (BIG_MAP, 210, Asteroid(11, 13))
))
def test_solve_map(lines, count, best):
    actual_best, board, actual_count = solve_map(lines)
    present_result(actual_best, board, actual_count)
    assert actual_best == best
    assert actual_count == count


@pytest.mark.parametrize("lines, first, second", (
        ([".#....#####...#..",
          "##...##.#####..##",
          "##...#...#.#####.",
          "..#.....#...###..",
          "..#.#.....#....##"], Asteroid(8, 1), Asteroid(9, 0)),
        (BIG_MAP, Asteroid(11, 12), Asteroid(12, 1))
))
def test_shoot(lines, first, second):
    station, board, _ = solve_map(lines)
    vectors = [d[0][0] for d in station.lines_of_sight.values()]
    firing_order = decide_firing_order(vectors)
    targets = [first, second]
    for target in shoot(firing_order, station, board):
        assert target == targets.pop(0)
        if not targets:
            break


@pytest.mark.parametrize("vectors, first, second, last", (
        ([Vector2(0, 1), Vector2(1, 0), Vector2(1, 1)], Vector2(1, 0), Vector2(1, 1), Vector2(0, 1)),
        ([Vector2(0, 2), Vector2(0, -1), Vector2(1, 1)], Vector2(0, -1), Vector2(1, 1), Vector2(0, 2)),
        ([Vector2(-6, 0), Vector2(8, 1), Vector2(6, 0), Vector2(0, -3), Vector2(-1, -3)],
         Vector2(0, -3), Vector2(6, 0), Vector2(-1, -3))
))
def test_firing_order(vectors, first, second, last):
    firing_order = decide_firing_order(vectors)
    assert firing_order[0] == first.theta
    assert firing_order[1] == second.theta
    assert firing_order[-1] == last.theta


@pytest.mark.parametrize("a, b, vector", (
        (Asteroid(0, 1), Asteroid(0, 2), Vector2(0, 1)),
        (Asteroid(1, 0), Asteroid(2, 0), Vector2(1, 0)),
        (Asteroid(0, 0), Asteroid(1, 1), Vector2(1, 1)),
        (Asteroid(0, 1), Asteroid(1, 1), Vector2(1, 0)),
))
def test_vector_to(a, b, vector):
    actual_vector = a.vector_to(b)
    assert actual_vector.theta == vector.theta


@pytest.mark.parametrize("a, b, vector", (
        (Asteroid(0, 1), Asteroid(0, 2), Vector2(0, 1)),
        (Asteroid(1, 0), Asteroid(2, 0), Vector2(1, 0)),
        (Asteroid(0, 0), Asteroid(1, 1), Vector2(1, 1)),
        (Asteroid(0, 1), Asteroid(1, 1), Vector2(1, 0)),
        (Asteroid(1, 0), Asteroid(1, 2), Vector2(0, 2)),
))
def test_add(a, b, vector):
    a.add(b)
    assert len(a.lines_of_sight) == 1
    assert len(a.lines_of_sight[vector.theta]) == 1
    target_vector, target = a.lines_of_sight[vector.theta][0]
    assert target_vector.x == vector.x
    assert target_vector.y == vector.y
    assert target == b
