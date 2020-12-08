#!/usr/bin/env python
# -*- coding: utf-8

import pkg_resources


def get_input_name(day, year):
    return pkg_resources.resource_filename(f"ibidem.advent_of_code.y{year}", f"data/dec{day:02}.txt")
