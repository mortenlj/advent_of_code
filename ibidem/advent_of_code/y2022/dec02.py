#!/usr/bin/env python
import enum

from ibidem.advent_of_code.util import get_input_name


class Outcome(enum.IntEnum):
    Loss = 0
    Draw = 3
    Win = 6

    @staticmethod
    def outcome(input):
        return {
            "X": Outcome.Loss,
            "Y": Outcome.Draw,
            "Z": Outcome.Win
        }[input.strip()]


class Play(enum.IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3

    @staticmethod
    def opponent(input):
        return {
            "A": Play.Rock,
            "B": Play.Paper,
            "C": Play.Scissors
        }[input.strip()]

    @staticmethod
    def player(input):
        return {
            "X": Play.Rock,
            "Y": Play.Paper,
            "Z": Play.Scissors
        }[input.strip()]


def load1(fobj):
    game = []
    for line in fobj:
        if line.strip():
            opponent, player = line.strip().split()
            game.append((Play.opponent(opponent), Play.player(player)))
    return game


def load2(fobj):
    game = []
    for line in fobj:
        if line.strip():
            opponent, outcome = line.strip().split()
            game.append((Play.opponent(opponent), Outcome.outcome(outcome)))
    return game


def play_round1(round):
    match round:
        case (Play.Rock, Play.Rock):
            return Outcome.Draw + Play.Rock
        case (Play.Rock, Play.Paper):
            return Outcome.Win + Play.Paper
        case (Play.Rock, Play.Scissors):
            return Outcome.Loss + Play.Scissors
        case (Play.Paper, Play.Rock):
            return Outcome.Loss + Play.Rock
        case (Play.Paper, Play.Paper):
            return Outcome.Draw + Play.Paper
        case (Play.Paper, Play.Scissors):
            return Outcome.Win + Play.Scissors
        case (Play.Scissors, Play.Rock):
            return Outcome.Win + Play.Rock
        case (Play.Scissors, Play.Paper):
            return Outcome.Loss + Play.Paper
        case (Play.Scissors, Play.Scissors):
            return Outcome.Draw + Play.Scissors


def play_round2(round):
    match round:
        case (Play.Rock, Outcome.Loss):
            return Outcome.Loss + Play.Scissors
        case (Play.Rock, Outcome.Draw):
            return Outcome.Draw + Play.Rock
        case (Play.Rock, Outcome.Win):
            return Outcome.Win + Play.Paper
        case (Play.Paper, Outcome.Loss):
            return Outcome.Loss + Play.Rock
        case (Play.Paper, Outcome.Draw):
            return Outcome.Draw + Play.Paper
        case (Play.Paper, Outcome.Win):
            return Outcome.Win + Play.Scissors
        case (Play.Scissors, Outcome.Loss):
            return Outcome.Loss + Play.Paper
        case (Play.Scissors, Outcome.Draw):
            return Outcome.Draw + Play.Scissors
        case (Play.Scissors, Outcome.Win):
            return Outcome.Win + Play.Rock


def part1(game):
    result = 0
    for round in game:
        result += play_round1(round)
    return result


def part2(game):
    result = 0
    for round in game:
        result += play_round2(round)
    return result


if __name__ == "__main__":
    with open(get_input_name(2, 2022)) as fobj:
        p1_result = part1(load1(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(2, 2022)) as fobj:
        p2_result = part2(load2(fobj))
        print(f"Part 2: {p2_result}")
