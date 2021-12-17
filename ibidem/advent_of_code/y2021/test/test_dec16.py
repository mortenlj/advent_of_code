import io
from binascii import unhexlify

import pytest

from ibidem.advent_of_code.y2021.dec16 import load, part1, part2, parse_literal, get_bin_str

TEST_INPUT = io.StringIO("""D2FE28""")


class TestDec16():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert bin(int.from_bytes(loaded, byteorder="big")) == "0b110100101111111000101000"

    @pytest.mark.parametrize("input, expected", (
            ("8A004A801A8002F478", 16),
            ("620080001611562C8802118E34", 12),
            ("C0015000016115A2E0802F182340", 23),
            ("A0016C880162017C3686B18A3D4780", 31),
    ))
    def test_part1(self, input, expected):
        parsed = load(io.StringIO(input))
        result = part1(parsed)
        assert result == expected

    @pytest.mark.parametrize("input, expected", (
            ("C200B40A82", 3),
            ("04005AC33890", 54),
            ("880086C3E88112", 7),
            ("CE00C43D881120", 9),
            ("D8005AC2A8F0", 1),
            ("F600BC2D8F", 0),
            ("9C005AC2F8F0", 0),
            ("9C0141080250320F1802104A08", 1),
    ))
    def test_part2(self, input, expected):
        parsed = load(io.StringIO(input))
        result = part2(parsed)
        assert result == expected

    @pytest.mark.parametrize("input, offset, expected", (
            ("D2FE28", 6, 2021),
            ("38006F45291200", 28, 10),
            ("38006F45291200", 39, 20),
    ))
    def test_parse_literal(self, input, offset, expected):
        data = load(io.StringIO(input))
        _, value = parse_literal(data, offset)
        assert value == expected

    @pytest.mark.parametrize("input, expected", (
            ("38006F45291200", "00111000000000000110111101000101001010010001001000000000"),
            ("EE00D40C823060", "11101110000000001101010000001100100000100011000001100000"),
            ("D2FE28", "110100101111111000101000"),
    ))
    def test_get_bin_str(self, input, expected):
        actual = get_bin_str(unhexlify(input))
        assert actual == expected
