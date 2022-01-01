#!/usr/bin/env python

from setuptools import setup


def read(filename):
    f = open(filename)
    contents = f.read()
    f.close()
    return contents


setup(
    name="advent_of_code",
    version="1.0",
    packages=["ibidem", "ibidem.advent_of_code"],
    namespace_packages=["ibidem"],
    zip_safe=True,
    include_package_data=True,

    # Requirements
    install_requires=[
        "numpy",
        "vectormath",
        "colorama",
        "requests",
        "networkx",
        "bitstruct",
        "alive_progress",
        "tqdm",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-xdist",
            "pytest-sugar",
        ]
    },

    # Metadata
    author="Morten Lied Johansen",
    author_email="mortenjo@ifi.uio.no",
    description="Advent of Code solutions",
    long_description=read("README.rst"),
    license="MIT",
    keywords="ibidem advent_of_code",

    entry_points={
        "console_scripts": [
            "aoc = ibidem.advent_of_code.cli:main"
        ]
    }
)
