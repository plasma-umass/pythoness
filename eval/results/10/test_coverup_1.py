# file: src/oracle10.py:1-26
# asked: {"lines": [1, 2, 3, 4, 6, 7, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22, 23, 24, 26], "branches": [[12, 13], [12, 16], [13, 12], [13, 14], [16, 17], [16, 26], [17, 16], [17, 18], [18, 20], [18, 23], [23, 17], [23, 24]]}
# gained: {"lines": [1, 2, 3, 4, 6, 7, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22, 23, 24, 26], "branches": [[12, 13], [12, 16], [13, 12], [13, 14], [16, 17], [16, 26], [17, 16], [17, 18], [18, 20], [18, 23], [23, 17], [23, 24]]}

import pytest
from src.oracle10 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_isMatch_empty_string(solution):
    assert solution.isMatch("", "") == True

def test_isMatch_single_char_match(solution):
    assert solution.isMatch("a", "a") == True

def test_isMatch_single_char_no_match(solution):
    assert solution.isMatch("a", "b") == False

def test_isMatch_dot_char(solution):
    assert solution.isMatch("a", ".") == True

def test_isMatch_star_char(solution):
    assert solution.isMatch("aa", "a*") == True
    assert solution.isMatch("aa", ".*") == True
    assert solution.isMatch("ab", ".*") == True
    assert solution.isMatch("aab", "c*a*b") == True

def test_isMatch_complex_pattern(solution):
    assert solution.isMatch("mississippi", "mis*is*p*.") == False
    assert solution.isMatch("mississippi", "mis*is*ip*.") == True

def test_isMatch_no_star(solution):
    assert solution.isMatch("abcd", "d*") == False

def test_isMatch_empty_pattern(solution):
    assert solution.isMatch("a", "") == False

def test_isMatch_empty_string_with_star(solution):
    assert solution.isMatch("", "a*") == True
