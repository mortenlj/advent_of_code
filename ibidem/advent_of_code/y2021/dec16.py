#!/usr/bin/env python
import operator
from binascii import unhexlify
from functools import reduce

import bitstruct

from ibidem.advent_of_code.util import get_input_name, time_this


class Packet:
    def __init__(self, version, type_id, subpackets):
        self.version = version
        self.type_id = type_id
        self.subpackets = subpackets


class LiteralPacket(Packet):
    def __init__(self, version, type_id, value):
        super().__init__(version, type_id, [])
        self.value = value


class OperatorPacket(Packet):
    _func_map = {
        0: lambda *args: reduce(operator.add, args),
        1: lambda *args: reduce(operator.mul, args),
        2: lambda *args: min(args),
        3: lambda *args: max(args),
        5: lambda a, b: 1 if a > b else 0,
        6: lambda a, b: 1 if a < b else 0,
        7: lambda a, b: 1 if a == b else 0,
    }

    def __init__(self, version, type_id, subpackets):
        super().__init__(version, type_id, subpackets)

    @property
    def value(self):
        values = [p.value for p in self.subpackets]
        return self._func_map[self.type_id](*values)


def load(fobj):
    return unhexlify(fobj.read().strip())


def get_bin_str(data):
    b = bin(int.from_bytes(data, byteorder="big"))[2:]
    wanted_len = len(data) * 8
    missing = wanted_len - len(b)
    return ("0" * missing) + b


def parse_header(data, offset):
    return bitstruct.unpack_from_dict(">u3u3>", ["version", "type_id"], data, offset), offset + 6


def parse_literal(data, offset):
    bstr = get_bin_str(data)
    cont, b = bstr[offset], bstr[offset + 1:offset + 5]
    bits = [b]
    offset += 5
    while cont == "1":
        cont, b = bstr[offset], bstr[offset + 1:offset + 5]
        bits.append(b)
        offset += 5
    value = int("".join(bits), 2)
    return offset, value


def parse_operator(data, offset):
    length_type = bitstruct.unpack_from(">u1>", data, offset)[0]
    offset += 1
    subpackets = []
    if length_type == 0:
        length = bitstruct.unpack_from(">u15>", data, offset)[0]
        offset += 15
        end_offset = offset + length
        while offset < end_offset:
            offset, packet = parse_packet(data, offset)
            subpackets.append(packet)
    elif length_type == 1:
        length = bitstruct.unpack_from(">u11>", data, offset)[0]
        offset += 11
        for _ in range(length):
            offset, packet = parse_packet(data, offset)
            subpackets.append(packet)
    return offset, subpackets


def parse_packet(data: bytes, offset: int):
    """Parse a packet and all its subpackets

    :param data - databuffer
    :param offset - offset to start parsing from

    :return offset - the next offset
    :return packet - the parsed packet
    """
    header, offset = parse_header(data, offset)
    if header["type_id"] == 4:
        offset, value = parse_literal(data, offset)
        packet = LiteralPacket(header["version"], header["type_id"], value)
    else:
        offset, subpackets = parse_operator(data, offset)
        packet = OperatorPacket(header["version"], header["type_id"], subpackets)
    return offset, packet


def calculate_version_sum(packet):
    version_sum = packet.version
    for sub in packet.subpackets:
        version_sum += calculate_version_sum(sub)
    return version_sum


@time_this
def part1(data):
    offset, packet = parse_packet(data, 0)
    version_sum = calculate_version_sum(packet)
    return version_sum


@time_this
def part2(data):
    offset, packet = parse_packet(data, 0)
    return packet.value


if __name__ == "__main__":
    with open(get_input_name(16, 2021)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(16, 2021)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
