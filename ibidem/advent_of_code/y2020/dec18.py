#!/usr/bin/env python

import operator
import tokenize
from io import StringIO

from ibidem.advent_of_code.util import get_input_name


def load():
    homework = []
    with open(get_input_name(18, 2020)) as fobj:
        for line in fobj:
            tokens = tokenize_line(line)
            homework.append(tokens[:-2])
    return homework


def tokenize_line(line):
    exp = StringIO(line)
    tokens = list(tokenize.generate_tokens(exp.readline))
    return tokens


def select_op(s):
    return {
        "+": operator.add,
        "*": operator.mul,
    }[s]


def solve_expression(exp):
    result = 0
    op = operator.add
    exp_iter = iter(exp)
    for token in exp_iter:
        if token.type == tokenize.OP and token.string == "(":
            result = op(result, solve_expression(exp_iter))
        elif token.type == tokenize.OP and token.string == ")":
            return result
        elif token.type == tokenize.OP:
            op = select_op(token.string)
        elif token.type == tokenize.NUMBER:
            result = op(result, int(token.string))
    return result


def part1(homework):
    results = 0
    for exp in homework:
        result = solve_expression(exp)
        print(f"The expression {exp} evaluates to {result}")
        results += result
    print(f"The final result is {results}")
    return results


def part2():
    pass


if __name__ == "__main__":
    homework = load()
    part1(homework)
    part2()
