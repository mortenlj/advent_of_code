#!/usr/bin/env python
from dataclasses import dataclass
from operator import attrgetter

from alive_progress import alive_it

from ibidem.advent_of_code.util import get_input_name


@dataclass
class File:
    id: int
    num_blocks: int
    blocks: list[int]


class Disk:
    free_blocks: list[int]
    used_blocks: dict[int, File]
    files: dict[int, File]

    def __init__(self):
        self.free_blocks = []
        self.used_blocks = {}
        self.files = {}

    def create_file(self, file):
        self.files[file.id] = file
        for block in file.blocks:
            self.used_blocks[block] = file

    def _find_free_blocks(self, num_blocks, max_block):
        free_blocks = []
        for block in self.free_blocks:
            if len(free_blocks) == num_blocks:
                return free_blocks
            if block >= max_block:
                return None
            if free_blocks:
                if free_blocks[-1] + 1 == block:
                    free_blocks.append(block)
                    continue
            free_blocks = [block]
        return None

    def optimize_files(self):
        print("Starting optimize files ...")
        self.print()
        files = sorted(self.files.values(), key=attrgetter("id"), reverse=True)
        for file in alive_it(files):
            self.free_blocks.sort()
            block = file.blocks[0]
            free_blocks = self._find_free_blocks(file.num_blocks, block)
            if free_blocks is None:
                continue
            for b in file.blocks:
                del self.used_blocks[b]
            self.free_blocks.extend(file.blocks)
            for b in free_blocks:
                self.used_blocks[b] = file
                self.free_blocks.remove(b)
            file.blocks = free_blocks
        print("Optimize done.")
        self.print()

    def optimize_blocks(self):
        print("Starting optimize blocks ...")
        self.print()
        self.free_blocks.sort()
        for block in alive_it(sorted(self.used_blocks.keys(), reverse=True)):
            file = self.used_blocks[block]
            free_block = self.free_blocks.pop(0)
            if free_block >= block:
                self.free_blocks.insert(0, free_block)
                break
            self.used_blocks[free_block] = file
            del self.used_blocks[block]
            self.free_blocks.append(block)
            file.blocks.remove(block)
            file.blocks.append(free_block)
        print("Optimize done.")
        self.print()

    def checksum(self):
        block_sums = []
        for block, file in self.used_blocks.items():
            block_sums.append(block * file.id)
        return sum(block_sums)

    def print(self):
        last_block = max(max(self.free_blocks), max(self.used_blocks.keys()))
        if last_block > 160:
            print("!!! Too many blocks to print.")
            return
        output = []
        for block in range(last_block + 1):
            if block in self.free_blocks:
                output.append(".")
            elif block in self.used_blocks:
                output.append(str(self.used_blocks[block].id))
        print("".join(output))


def load(fobj):
    disk = Disk()
    cur_block = 0
    for i, nb in enumerate(fobj.read().strip()):
        num_blocks = int(nb)
        if i % 2 == 0:
            file = File(
                i // 2,
                num_blocks,
                [b for b in range(cur_block, cur_block + num_blocks)],
            )
            disk.create_file(file)
        else:
            disk.free_blocks.extend(range(cur_block, cur_block + num_blocks))
        cur_block += num_blocks
    return disk


def part1(disk: Disk):
    disk.optimize_blocks()
    return disk.checksum()


def part2(disk: Disk):
    disk.optimize_files()
    return disk.checksum()


if __name__ == "__main__":
    with open(get_input_name(9, 2024)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(9, 2024)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
