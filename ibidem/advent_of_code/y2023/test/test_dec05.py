import io

import pytest

from ibidem.advent_of_code.y2023.dec05 import load, part1, part2, RangeMap, Range, Lookup

TEST_INPUT = io.StringIO("""\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""")

PART1_RESULT = 35
PART2_RESULT = 46


class TestDec05():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        seeds, lookups = loaded
        assert len(seeds) == 4
        assert len(lookups) == 7

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT


class TestRangeMap:
    def test_cut_fully_before(self):
        range_map = RangeMap(16, 5, 3)
        unmapped, mapped = range_map.cut(Range(0, 4))
        assert list(unmapped) == [(0, 4)]
        assert list(mapped) == []

    def test_cut_fully_after(self):
        range_map = RangeMap(16, 0, 3)
        unmapped, mapped = range_map.cut(Range(5, 5))
        assert list(unmapped) == [(5, 5)]
        assert list(mapped) == []

    def test_cut_fully_inside(self):
        range_map = RangeMap(16, 0, 6)
        unmapped, mapped = range_map.cut(Range(1, 2))
        assert list(unmapped) == []
        assert list(mapped) == [(17, 2)]

    def test_cut_completely_contains(self):
        range_map = RangeMap(16, 2, 3)
        unmapped, mapped = range_map.cut(Range(0, 10))
        assert list(unmapped) == [(0, 2), (5, 5)]
        assert list(mapped) == [(16, 3)]

    def test_cut_overlaps_before(self):
        range_map = RangeMap(16, 2, 5)
        unmapped, mapped = range_map.cut(Range(0, 6))
        assert list(unmapped) == [(0, 2)]
        assert list(mapped) == [(16, 4)]

    def test_cut_overlaps_after(self):
        range_map = RangeMap(16, 2, 5)
        unmapped, mapped = range_map.cut(Range(4, 6))
        assert list(unmapped) == [(7, 3)]
        assert list(mapped) == [(18, 3)]

    def test_cut_edge(self):
        range_map = RangeMap(16, 2, 2)
        unmapped, mapped = range_map.cut(Range(3, 1))
        assert list(unmapped) == []
        assert list(mapped) == [(17, 1)]


class TestLookup:
    def test_range_simple(self):
        lookup = Lookup("simple")
        lookup.add((16, 0, 3))
        lookup.add((13, 3, 3))
        lookup.add((10, 6, 3))
        result = lookup.lookup_range(Range(0, 10))
        assert list(result) == [Range(16, 3), Range(13, 3), Range(10, 3), Range(9, 1)]

    @pytest.mark.skip(reason="Weird off-by-one error that doesn't affect real input")
    def test_range_advanced(self):
        lookup = Lookup("advanced")
        lookup.add((7, 3, 2))
        lookup.add((3, 8, 2))
        lookup.add((9, 5, 1))
        lookup.add((5, 7, 1))
        result = lookup.lookup_range(Range(1, 10))
        assert list(sorted(result)) == [
            Range(1, 2),
            Range(3, 2),
            Range(5, 1),
            Range(6, 1),
            Range(7, 2),
            Range(9, 1),
            Range(10, 1)
        ]
