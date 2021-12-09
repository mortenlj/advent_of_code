#!/usr/bin/env python

"""CLI to make working with Advent of Code slightly simpler
"""
import argparse
import json
import os
import webbrowser
from datetime import datetime

import pkg_resources
import requests

HTTPIE_SESSION_PATH = os.path.join(os.path.expanduser("~"), ".config", "httpie", "sessions", "adventofcode.com",
                                   "session.json")

SOLUTION_TEMPLATE = """\
#!/usr/bin/env python

from ibidem.advent_of_code.util import get_input_name


def load(fobj):
    return fobj.read()


def part1(input):
    return None


def part2(input):
    return None


if __name__ == "__main__":
    with open(get_input_name({day}, {year})) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {{p1_result}}")
    with open(get_input_name({day}, {year})) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {{p2_result}}")
"""

TEST_TEMPLATE = """\
import io
import pytest

from ibidem.advent_of_code.y{year}.dec{day:02} import load, part1, part2


TEST_INPUT = io.StringIO(\"\"\"\\
\"\"\")

PART1_RESULT = NotImplemented
PART2_RESULT = NotImplemented


class TestDec{day:02}():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded
        
    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT
        
    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
"""


def _get_session_cookie_value():
    with open(HTTPIE_SESSION_PATH) as fobj:
        data = json.load(fobj)
        return data["cookies"]["session"]["value"]


def get_input(options):
    def generator(year, day):
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        cookies = {"session": _get_session_cookie_value()}
        resp = requests.get(url, cookies=cookies)
        return resp.text

    return _create_file("data/", "txt", generator, options)


def create_solution(options):
    return _create_file("", "py", SOLUTION_TEMPLATE.format, options)


def create_test(options):
    return _create_file("test/test_", "py", TEST_TEMPLATE.format, options)


def _create_file(prefix, ext, content_generator, now):
    filepath = pkg_resources.resource_filename(f"ibidem.advent_of_code.y{now.year}", f"{prefix}dec{now.day:02}.{ext}")
    if os.path.exists(filepath):
        return filepath
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as fd:
        fd.write(content_generator(year=now.year, day=now.day))
    return filepath


def main():
    parser = argparse.ArgumentParser()
    now = datetime.now()
    parser.add_argument("--year", type=int, help="Year of the code", default=now.year)
    parser.add_argument("--day", type=int, help="Day of the code", default=now.day)
    options = parser.parse_args()
    filepath = get_input(options)
    print(f"Downloaded todays input to {filepath}")
    filepath = create_solution(options)
    print(f"Created solution file at {filepath}")
    filepath = create_test(options)
    print(f"Created test file at {filepath}")
    problem_url = f"https://adventofcode.com/{options.year}/day/{options.day}"
    print(f"Read the problem description at {problem_url} (I've tried opening it for you)")
    webbrowser.open_new_tab(problem_url)


if __name__ == "__main__":
    main()
