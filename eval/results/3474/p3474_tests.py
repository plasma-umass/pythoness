import pytest
from p3474oracle import Solution


@pytest.mark.parametrize(
    "str1, str2, expected",
    [
        ("T", "a", "a"),
        ("F", "a", "b"),
        ("TF", "aa", "aa"),
        ("FF", "aa", "ab"),
        ("TT", "aa", "aa"),
        ("TFT", "abc", "abc"),
        ("FTF", "aba", "bab"),
        ("TTT", "abc", "abc"),
        ("FFTF", "abcd", "bacd"),
        ("FTFF", "abcd", "bacd"),
        ("TFTF", "aabb", "aabb"),
        ("TFFF", "aabb", "abbb"),
        ("TTFT", "aaab", "aaab"),
        ("FTTT", "abcd", "abcd"),
        ("TF", "aa", "aa"),
        ("FT", "aa", "ba"),
        ("TFF", "abc", "abc"),
        ("F", "ab", "b"),
        ("T", "ab", "a"),
        ("TFTTF", "abcde", "abcde"),
    ],
)
def test_generateString(str1, str2, expected):
    assert Solution().generateString(str1, str2) == expected
