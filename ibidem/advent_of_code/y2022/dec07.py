#!/usr/bin/env python
import dataclasses

from ibidem.advent_of_code.util import get_input_name


@dataclasses.dataclass
class File:
    name: str
    size: int

    def __str__(self):
        return f"{self.name} (file, size={self.size})"

    def print_tree(self, indent):
        print(f"{indent}- {self}")

    def is_dir(self):
        return False


class Directory:
    name: str
    children: list["Directory|File"]
    parent: "Directory"

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []

    def is_dir(self):
        return True

    def cd(self, target):
        if target == "/":
            if self.parent:
                return self.parent.cd(target)
            return self
        if target == "..":
            if self.parent:
                return self.parent
            return self
        for c in self.children:
            if c.is_dir() and c.name == target:
                return c
        child = Directory(target, self)
        self.children.append(child)
        return child

    @property
    def size(self):
        return sum(c.size for c in self.children)

    def __str__(self):
        return "/".join((str(self.parent), self.name))

    __repr__ = __str__

    def print_tree(self, indent):
        print(f"{indent}- {self}")
        next_indent = "  " + indent
        for c in self.children:
            c.print_tree(next_indent)


class Os:
    cwd: Directory
    parsing_ls: bool

    def __init__(self):
        self.cwd = Directory("/", None)
        self.parsing_ls = False

    def __str__(self):
        return f"Os(cwd={self.cwd})"

    def cd(self, target):
        self.cwd = self.cwd.cd(target)
        return self

    def print_tree(self):
        self.cwd.print_tree("")

    def exec_line(self, line: str):
        if line.startswith("$"):
            self.parsing_ls = False
        if line.startswith("$ cd"):
            self.cd(line[5:])
            return
        if line.startswith("$ ls"):
            self.parsing_ls = True
            return
        if self.parsing_ls:
            if line.startswith("dir"):
                self.cwd.children.append(Directory(line[4:], self.cwd))
            else:
                size, name = line.split()
                self.cwd.children.append(File(name, int(size)))


def load(fobj):
    os = Os()
    for line in fobj:
        os.exec_line(line.strip())
    os.cd("/")
    os.print_tree()
    return os


def collect1(root, collected):
    if not root.is_dir():
        return
    if root.size <= 100000:
        collected.append(root)
    for child in root.children:
        collect1(child, collected)


def collect2(root, collected, request):
    if not root.is_dir():
        return
    if root.size >= request:
        collected.append(root)
    for child in root.children:
        collect2(child, collected, request)


def part1(os):
    root = os.cwd
    collected = []
    collect1(root, collected)
    return sum(d.size for d in collected)


def part2(os):
    TOTAL_DISK = 70000000
    NEEDED = 30000000
    root = os.cwd
    free = TOTAL_DISK - root.size
    request = NEEDED - free
    collected = []
    collect2(root, collected, request)
    return sorted((d.size for d in collected), reverse=True).pop()


if __name__ == "__main__":
    with open(get_input_name(7, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(7, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
