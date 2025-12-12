import pytest

from ibidem.advent_of_code.y2020.dec07 import (
    parse_color,
    TARGET,
    parse_network,
    count_children,
    find_containers,
)

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
""".splitlines(keepends=False)

ALTERNATE_RULES = """\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""".splitlines(keepends=False)

VALID_BAGS = {"bright white", "muted yellow", "dark orange", "light red"}


class TestDec07:
    @pytest.mark.parametrize(
        "spec, color",
        (
            ("light red bags", "light red"),
            ("1 bright white bag", "bright white"),
            ("2 muted yellow bags.", "muted yellow"),
            ("dark orange bags", "dark orange"),
            ("3 bright white bags", "bright white"),
            ("4 muted yellow bags.", "muted yellow"),
        ),
    )
    def test_parse_color(self, spec, color):
        assert parse_color(spec)[1] == color

    def test_no_other_color(self):
        assert parse_color("no other bags.") == ("", "no other")

    def test_find_containers(self):
        colors = find_containers(RULES, TARGET)
        assert VALID_BAGS == set(colors)

    @pytest.mark.parametrize(
        "rules, target, count",
        (
            (RULES, TARGET, 32),
            (
                [
                    "faded blue bags contain no other bags.",
                    "muted yellow bags contain 9 faded blue bags.",
                ],
                "muted yellow",
                9,
            ),
            (ALTERNATE_RULES, TARGET, 126),
        ),
    )
    def test_count_children(self, rules, target, count):
        g = parse_network(rules)
        assert (count_children(g, target) - 1) == count
