#!/usr/bin/env python
import dataclasses
from typing import Optional

from ibidem.advent_of_code.util import get_input_name, gen_list


@dataclasses.dataclass
class Element:
    value: int
    next: Optional["Element"] = None
    previous: Optional["Element"] = None
    reading: bool = False

    def __str__(self):
        next_value = self.next.value if self.next else "None"
        prev_value = self.previous.value if self.previous else "None"
        return f"Element(value={self.value}, next={next_value}, previous={prev_value})"

    def __repr__(self):
        return self.__str__()

    def insert(self, other: "Element"):
        other.next = self.next
        other.previous = self
        self.next = other

    def cut(self) -> "Element":
        self.previous.next = self.next
        self.next.previous = self.previous
        self.next = self.previous = None
        return self

    def find_first(self, value: int) -> Optional["Element"]:
        cur = self
        while cur.value != value and cur.next != self:
            cur = cur.next
        if cur.value == value:
            return cur
        return None

    def get_at(self, offset: int) -> "Element":
        if offset > 0:
            return self.get_at_forwards(offset)
        else:
            return self.get_at_backwards(offset)

    def get_at_forwards(self, offset: int) -> "Element":
        cur = self
        while offset > 0:
            cur = cur.next
            offset -= 1
        return cur

    def get_at_backwards(self, offset: int) -> "Element":
        cur = self
        while offset < 0:
            cur = cur.previous
            offset += 1
        return cur

    def values_as_list(self, result=None):
        if self.reading:
            return
        if result is None:
            result = []
        result.append(self.value)
        self.reading = True
        try:
            self.next.values_as_list(result)
            return result
        finally:
            self.reading = False

    def values_as_rev_list(self, result=None):
        if self.reading:
            return
        if result is None:
            result = []
        result.append(self.value)
        self.reading = True
        try:
            self.previous.values_as_rev_list(result)
            return result
        finally:
            self.reading = False


@gen_list
def load(fobj):
    head = None
    previous = None
    new = None
    for line in fobj:
        value = int(line.strip())
        new = Element(value)
        yield new
        if not head:
            head = new
        if previous:
            previous.next = new
            new.previous = previous
        previous = new
    if new:
        new.next = head
        head.previous = new


def part1(input: list[Element]):
    for item in input:
        # print(f"Item: {item}")
        # print("Before:", item.values_as_list())
        prev = item.previous
        item.cut()
        target = prev.get_at(item.value)
        # print(f"Target: {target}")
        insert_after(item, target)
        # print("After :", target.values_as_list())
        # print("AfterR:", list(reversed(target.previous.values_as_rev_list())))
    zero_element = input[0].find_first(0)
    first = zero_element.get_at(1000)
    second = zero_element.get_at(2000)
    third = zero_element.get_at(3000)
    return first.value + second.value + third.value


def insert_after(item, target):
    t_next = target.next
    item.next = t_next
    t_next.previous = item
    item.previous = target
    target.next = item


def part2(input: list[Element]):
    input_length = len(input)
    for item in input:
        item.value *= 811589153
    for i in range(10):
        for item in input:
            # print(f"Item: {item}")
            # print("Before:", item.values_as_list())
            prev = item.previous
            item.cut()
            target = prev.get_at(get_offset(input_length, item.value))
            # print(f"Target: {target}")
            insert_after(item, target)
            # print("After :", target.values_as_list())
            # print("AfterR:", list(reversed(target.previous.values_as_rev_list())))
    zero_element = input[0].find_first(0)
    first = zero_element.get_at(get_offset(input_length, 1000))
    second = zero_element.get_at(get_offset(input_length, 2000))
    third = zero_element.get_at(get_offset(input_length, 3000))
    return first.value + second.value + third.value


def get_offset(input_length, value):
    offset = 0
    if value < 0:
        offset = 1
    return (value % input_length) + offset


if __name__ == "__main__":
    with open(get_input_name(20, 2022)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(20, 2022)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
