from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.y2020.util import get_input_name

PART1_SLOPE = (3, 1)
PART2_SLOPES = (
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
)


def load():
    with open(get_input_name("dec03")) as fobj:
        return Board.from_string(fobj.read())


def part1():
    slope = PART1_SLOPE
    return count_slope(slope)


def part2():
    result = 1
    for slope in PART2_SLOPES:
        result *= count_slope(slope)
    print(f"Part 2 result: {result}")


def count_slope(slope):
    board = load()
    x = y = 0
    count = 0
    while y < board.size_y:
        c = board.get(x, y)
        if c == "#":
            count += 1
            board.set(x, y, "X")
        else:
            board.set(x, y, "O")
        x += slope[0]
        if x >= board.size_x:
            x = x - board.size_x
        y += slope[1]
    print(f"Counted {count} trees for slope {slope}")
    return count


if __name__ == "__main__":
    part1()
    part2()
