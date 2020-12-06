#!/usr/bin/env python

"""CLI to make working with Advent of Code slightly simpler"""
import datetime
import json
import os

import pkg_resources
import requests

HTTPIE_SESSION_PATH = os.path.join(os.path.expanduser("~"), ".config", "httpie", "sessions", "adventofcode.com",
                                   "session.json")

# TODO: Refactor location of util to be non-year specific
SOLUTION_TEMPLATE = """\
#!/usr/bin/env python

from ibidem.advent_of_code.y{year}.util import get_input_name


def load():
    with open(get_input_name("dec{day:02}")) as fobj:
        fobj.read()


def part1():
    pass

    
def part2():
    pass

    
if __name__ == "__main__":
    part1()
    part2()
"""

TEST_TEMPLATE = """\

import pytest

from ibidem.advent_of_code.y{year}.dec{day:02} import *


class TestDec{day:02}():
    def test_load(self):
        pass
"""


def _get_session_cookie_value():
    with open(HTTPIE_SESSION_PATH) as fobj:
        data = json.load(fobj)
        return data["cookies"]["session"]["value"]


def get_input():
    def generator(year, day):
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        cookies = {"session": _get_session_cookie_value()}
        resp = requests.get(url, cookies=cookies)
        return resp.text

    return _create_file("data/", "txt", generator)


def create_solution():
    return _create_file("", "py", SOLUTION_TEMPLATE.format)


def create_test():
    return _create_file("test/", "py", TEST_TEMPLATE.format)


def _create_file(dir, ext, content_generator):
    now = datetime.datetime.now()
    filepath = pkg_resources.resource_filename(f"ibidem.advent_of_code.y{now.year}", f"{dir}{now.day:02}.{ext}")
    if os.path.exists(filepath):
        return filepath
    with open(filepath, "w") as fd:
        fd.write(content_generator(year=now.year, day=now.day))
    return filepath


def main():
    filepath = get_input()
    print(f"Downloaded todays input to {filepath}")
    filepath = create_solution()
    print(f"Created solution file at {filepath}")
    filepath = create_test()
    print(f"Created test file at {filepath}")


if __name__ == "__main__":
    main()
