# file: src/oracle3455.py:4-43
# asked: {"lines": [4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 35, 36, 37, 38, 39, 40, 41, 42, 43], "branches": [[16, 17], [16, 28], [17, 18], [17, 19], [19, 20], [19, 21], [21, 22], [21, 23], [23, 24], [23, 25], [37, 38], [37, 43], [38, 39], [38, 40], [40, 37], [40, 41]]}
# gained: {"lines": [4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 35, 36, 37, 38, 39, 40, 41, 42, 43], "branches": [[16, 17], [16, 28], [17, 18], [17, 19], [19, 20], [19, 21], [21, 22], [21, 23], [23, 24], [23, 25], [37, 38], [37, 43], [38, 39], [38, 40], [40, 37], [40, 41]]}

import pytest
from src.oracle3455 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_shortestMatchingSubstring_case1(solution):
    s = "abcde"
    p = "a*c*e"
    result = solution.shortestMatchingSubstring(s, p)
    assert result == 5

def test_shortestMatchingSubstring_case2(solution):
    s = "abcde"
    p = "a*b*d"
    result = solution.shortestMatchingSubstring(s, p)
    assert result == 4

def test_shortestMatchingSubstring_case3(solution):
    s = "abcabcabc"
    p = "a*b*c"
    result = solution.shortestMatchingSubstring(s, p)
    assert result == 3

def test_getLPS_case1(solution):
    pattern = "a#abcde"
    result = solution._getLPS(pattern)
    assert result == [0, 0, 1, 0, 0, 0, 0]

def test_getLPS_case2(solution):
    pattern = "b#abcde"
    result = solution._getLPS(pattern)
    assert result == [0, 0, 0, 1, 0, 0, 0]

def test_getLPS_case3(solution):
    pattern = "c#abcde"
    result = solution._getLPS(pattern)
    assert result == [0, 0, 0, 0, 1, 0, 0]
