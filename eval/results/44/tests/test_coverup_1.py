# file: src/oracle44.py:1-25
# asked: {"lines": [1, 2, 3, 4, 6, 7, 9, 10, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 25], "branches": [[12, 13], [12, 16], [13, 12], [13, 14], [16, 17], [16, 25], [17, 16], [17, 18], [18, 19], [18, 22], [22, 17], [22, 23]]}
# gained: {"lines": [1, 2, 3, 4, 6, 7, 9, 10, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 25], "branches": [[12, 13], [12, 16], [13, 12], [13, 14], [16, 17], [16, 25], [17, 16], [17, 18], [18, 19], [18, 22], [22, 17], [22, 23]]}

import pytest
from src.oracle44 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_isMatch_empty_strings(solution):
    assert solution.isMatch("", "") == True

def test_isMatch_only_pattern_empty(solution):
    assert solution.isMatch("a", "") == False

def test_isMatch_only_string_empty(solution):
    assert solution.isMatch("", "a") == False

def test_isMatch_single_char_match(solution):
    assert solution.isMatch("a", "a") == True

def test_isMatch_single_char_no_match(solution):
    assert solution.isMatch("a", "b") == False

def test_isMatch_single_char_wildcard(solution):
    assert solution.isMatch("a", "?") == True

def test_isMatch_multiple_char_match(solution):
    assert solution.isMatch("abc", "abc") == True

def test_isMatch_multiple_char_no_match(solution):
    assert solution.isMatch("abc", "abd") == False

def test_isMatch_multiple_char_wildcard(solution):
    assert solution.isMatch("abc", "a?c") == True

def test_isMatch_star_match_empty(solution):
    assert solution.isMatch("abc", "a*") == True

def test_isMatch_star_match_some(solution):
    assert solution.isMatch("abc", "a*c") == True

def test_isMatch_star_match_all(solution):
    assert solution.isMatch("abc", "*") == True

def test_isMatch_star_no_match(solution):
    assert solution.isMatch("abc", "a*d") == False

def test_isMatch_complex_pattern(solution):
    assert solution.isMatch("abcde", "a*de") == True

def test_isMatch_complex_pattern_no_match(solution):
    assert solution.isMatch("abcde", "a*d?f") == False
