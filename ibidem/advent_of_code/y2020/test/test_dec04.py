import pytest

from ibidem.advent_of_code.y2020.dec04 import VALIDATION


@pytest.mark.parametrize("field,valid,value", (
        ("byr", True, "2002"),
        ("byr", False, "2003"),
        ("hgt", True, "60in"),
        ("hgt", True, "190cm"),
        ("hgt", False, "190in"),
        ("hgt", False, "190"),
        ("hcl", True, "#123abc"),
        ("hcl", False, "#123abz"),
        ("hcl", False, "123abc"),
        ("ecl", True, "brn"),
        ("ecl", False, "wat"),
        ("pid", True, "000000001"),
        ("pid", False, "0123456789"),
))
def test_validation(field, valid, value):
    assert VALIDATION[field](value) == valid
