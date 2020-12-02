import pytest

from ibidem.advent_of_code.y2020.dec02 import Policy2


@pytest.mark.parametrize("policy, password, valid", (
        ("1-3 a", "abcde", True),
        ("1-3 b", "cdefg", False),
        ("2-9 c", "ccccccccc", False),
        ("1-3 a", "ababa", False),
        ("1-3 a", "aab", True),
        ("1-3 a", "baba", False),
        ("10-11 a", "aaaaaaaaaaa", False),
        ("10-11 a", "aaaaaaaaaab", True),
        ("10-11 a", "aaaaaaaaaba", True),
        ("10-11 a", "aaaaaaaaabb", False),
        ("4-10 v", "snspvprnvwz", False),
))
def test_policy2(policy, password, valid):
    policy = Policy2(policy)
    assert policy.valid(password) == valid
