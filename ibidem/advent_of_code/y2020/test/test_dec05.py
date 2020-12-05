import pytest

from ibidem.advent_of_code.y2020.dec05 import BoardingPass


@pytest.mark.parametrize("code, row, column, seat_id", (
        ("BFFFBBFRRR", 70, 7, 567),
        ("FFFBBBFRRR", 14, 7, 119),
        ("BBFFBBFRLL", 102, 4, 820),
))
def test_boardingpass(code, row, column, seat_id):
    bp = BoardingPass(code)
    assert row == bp.row
    assert column == bp.column
    assert seat_id == bp.seat_id
