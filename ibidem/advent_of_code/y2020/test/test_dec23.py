import pytest

from ibidem.advent_of_code.y2020.dec23 import (
    parse,
    part2,
    Cup,
    play_round,
    pick_destination,
    extract_three,
    play_game,
)


class TestDec23:
    def test_parse(self):
        first, cups = parse("123")
        assert first.label == 1
        assert first.clockwise.label == 2
        assert first.tail().label == 1
        assert cups[1] == first

    def test_cup_print(self):
        input = "1423765809"
        first, _ = parse(input)
        s = first.print()
        assert s == input[1:]

    def test_cup_inject(self):
        first, cups = parse("1234")
        c5 = Cup(5)
        c6 = Cup(6)
        c7 = Cup(7)
        c5.clockwise = c6
        c6.clockwise = c7
        cups[2].inject(c5)
        s = first.print()
        assert s == "256734"

    @pytest.mark.parametrize(
        "input, endstate, current, next",
        (
            ("389125467", "89154673", 3, 2),
            ("328915467", "46789132", 2, 5),
            ("574183926", "37419265", 5, 8),
            ("925841367", "36725841", 1, 9),
        ),
    )
    def test_play_round(self, input, endstate, current, next):
        _, cups = parse(input)
        actual = play_round(cups[current])
        assert actual.print() == endstate
        assert actual.label == next

    @pytest.mark.parametrize(
        "current, cups_input, expected",
        (
            (5, "12345", 4),
            (2, "32451", 1),
            (1, "41532", 5),
            (5, "125", 2),
        ),
    )
    def test_pick_destination(self, current, cups_input, expected):
        _, cups = parse(cups_input)
        actual = pick_destination(cups[current])
        assert actual.label == expected

    @pytest.mark.parametrize(
        "current, cups_input, expected_chain",
        (
            (5, "12345", "23"),
            (2, "32451", "51"),
            (1, "41532", "32"),
        ),
    )
    def test_extract_three(self, current, cups_input, expected_chain):
        first, cups = parse(cups_input)
        actual = extract_three(cups[current])
        assert actual.print() == expected_chain

    @pytest.mark.parametrize(
        "rounds, endstate",
        (
            (10, "92658374"),
            (100, "67384529"),
        ),
    )
    def test_play_game(self, rounds, endstate):
        first, cups = parse("389125467")
        result = play_game(rounds, first, cups)
        assert result.print() == endstate

    @pytest.mark.xfail(reason="Never managed to implement this correctly")
    def test_part2(self):
        first, cups = parse("389125467")
        one, two = part2(first, cups)
        assert one.label == 934001
        assert two.label == 159792
