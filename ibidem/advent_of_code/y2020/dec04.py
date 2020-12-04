#!/usr/bin/env python
import re

from ibidem.advent_of_code.y2020.util import get_input_name


def hgt_validator(v):
    """a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    """
    m = re.match("(\d+)(cm|in)", v)
    if m:
        height = int(m.group(1))
        unit = m.group(2)
        if unit == "cm":
            return number_validator(150, 193)(height)
        else:
            return number_validator(59, 76)(height)
    return False


def number_validator(min, max):
    def validator(x):
        v = int(x)
        return min <= v <= max

    return validator


VALIDATION = {
    "byr": number_validator(1920, 2002),
    "iyr": number_validator(2010, 2020),
    "eyr": number_validator(2020, 2030),
    "hgt": hgt_validator,
    "hcl": lambda x: bool(re.match(r"#[0-9a-f]{6}$", x)),
    "ecl": lambda x: bool(re.match(r"(amb|blu|brn|gry|grn|hzl|oth)$", x)),
    "pid": lambda x: bool(re.match(r"\d{9}$", x)),
}


def parse(s):
    s = " ".join(s)
    fields = s.split()
    record = {}
    for field in fields:
        key, value = field.split(":")
        record[key.strip()] = value.strip()
    return record


def load():
    records = []
    with open(get_input_name("dec04")) as fobj:
        record = []
        for line in fobj:
            line = line.strip()
            if line:
                record.append(line)
            else:
                records.append(parse(record))
                record = []
    return records


def part1():
    records = load()
    count = 0
    for record in records:
        if VALIDATION.keys() <= record.keys():
            count += 1
    print(f"Part 1 counted {count} valid records")


def part2():
    records = load()
    count = 0
    for record in records:
        if VALIDATION.keys() <= record.keys():
            validation = []
            for key, value in record.items():
                if key in VALIDATION:
                    validation.append(VALIDATION[key](value))
            if all(validation):
                count += 1
    print(f"Part 2 counted {count} valid records")


if __name__ == "__main__":
    part1()
    part2()
