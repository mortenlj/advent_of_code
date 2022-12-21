import io

import pytest

from ibidem.advent_of_code.y2022.dec20 import load, part1, part2, insert_after, Element

TEST_INPUT = io.StringIO("""\
1
2
-3
3
-2
0
4
""")

PART1_RESULT = 3
PART2_RESULT = 1623178306


class TestDec20():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert len(loaded) == 7
        assert loaded[0].value == 1
        assert loaded[-1].value == 4
        assert loaded[0].previous == loaded[-1]
        assert loaded[0].next == loaded[1]
        assert loaded[-1].previous == loaded[-2]
        assert loaded[-1].next == loaded[0]

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT

    @pytest.mark.parametrize(("item_value", "target_value"), (
            (-3, 0),
            (-2, 2),
            (0, -2),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 3),
    ))
    def test_insert_after(self, item_value, target_value, loaded: list[Element]):
        item = Element(item_value)
        target = loaded[0].find_first(target_value)
        t_next, t_prev = target.next, target.previous
        insert_after(item, target)
        assert target.next == item
        assert target.previous == t_prev
        assert item.next == t_next
        assert item.previous == target
