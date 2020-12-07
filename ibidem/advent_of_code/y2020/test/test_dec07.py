import pytest

from ibidem.advent_of_code.y2020.dec07 import parse_color, parse, TARGET

RULES = """\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

VALID_BAGS = {"bright white", "muted yellow", "dark orange", "light red"}


class TestDec07:
    @pytest.mark.parametrize("spec, color", (
            ("light red bags", "light red"),
            ("1 bright white bag", "bright white"),
            ("2 muted yellow bags.", "muted yellow"),
            ("dark orange bags", "dark orange"),
            ("3 bright white bags", "bright white"),
            ("4 muted yellow bags.", "muted yellow"),
    ))
    def test_parse_color(self, spec, color):
        assert parse_color(spec) == color

    def test_parse(self):
        colors = parse(RULES.splitlines(keepends=False), TARGET)
        assert VALID_BAGS == set(colors)
