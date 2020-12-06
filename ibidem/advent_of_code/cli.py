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

from ibidem.advent_of_code.y2020.util import get_input_name


def load():
    with open(get_input_name("dec{:02}")) as fobj:
        fobj.read()


def part1():
    pass

    
def part2():
    pass

    
if __name__ == "__main__":
    part1()
    part2()
"""


def _get_session_cookie_value():
    with open(HTTPIE_SESSION_PATH) as fobj:
        data = json.load(fobj)
        return data["cookies"]["session"]["value"]


def get_input():
    now = datetime.datetime.now()
    filepath = pkg_resources.resource_filename(f"ibidem.advent_of_code.y{now.year}", f"data/dec{now.day:02}.txt")
    if os.path.exists(filepath):
        return filepath
    url = f"https://adventofcode.com/{now.year}/day/{now.day}/input"
    cookies = {"session": _get_session_cookie_value()}
    resp = requests.get(url, cookies=cookies)
    with open(filepath, 'wb') as fd:
        for chunk in resp.iter_content(chunk_size=128):
            fd.write(chunk)
    return filepath


def create_solution():
    now = datetime.datetime.now()
    filepath = pkg_resources.resource_filename(f"ibidem.advent_of_code.y{now.year}", f"dec{now.day:02}.py")
    if os.path.exists(filepath):
        return filepath
    with open(filepath, "w") as fd:
        fd.write(SOLUTION_TEMPLATE.format(now.day))
    return filepath


def main():
    filepath = get_input()
    print(f"Downloaded todays input to {filepath}")
    filepath = create_solution()
    print(f"Created solution file at {filepath}")


if __name__ == "__main__":
    main()
