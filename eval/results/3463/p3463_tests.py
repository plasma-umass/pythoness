import pytest
from p3463oracle import Solution


@pytest.mark.parametrize(
    "s, expected",
    [
        ("1", True),
        ("22", True),
        ("123", False),
        ("112233", True),
        ("111222333", False),
        ("12345", False),
        ("0", True),
        ("10", True),
        ("314159", False),
        ("271828", False),
        ("1234321", False),
        ("1221", True),
        ("111222", True),
        ("333222111", False),
        ("9876543210", False),
        ("1" + "0" * 50, True),
        ("9" * 100 + "0", True),
        ("48" * 25, False),
        ("1023456789", False),
        ("96" * 50, True),
    ],
)
def test_hasSameDigits(s, expected):
    assert Solution().hasSameDigits(s) == expected
