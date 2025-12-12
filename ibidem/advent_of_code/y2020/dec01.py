from ibidem.advent_of_code.util import get_input_name


def load():
    with open(get_input_name(1, 2020)) as fobj:
        return [int(line) for line in fobj]


def part1():
    report = load()
    for i in report:
        for j in report:
            if i + j == 2020:
                print(i * j)
                return


def part2():
    report = load()
    for i in report:
        for j in report:
            for k in report:
                if i + j + k == 2020:
                    print(i * j * k)
                    return


if __name__ == "__main__":
    part1()
    part2()
