#!/usr/bin/env python
# -*- coding: utf-8

import os


def get_input_name(day):
    return os.path.join(os.path.dirname(__file__), "data", "{}.txt".format(day))
