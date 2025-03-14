# file: src/oracle3474.py:35-40
# asked: {"lines": [35, 37, 38, 39, 40], "branches": [[37, 38], [37, 40], [38, 37], [38, 39]]}
# gained: {"lines": [35, 37, 38, 39, 40], "branches": [[37, 38], [37, 40], [38, 37], [38, 39]]}

import pytest
from src.oracle3474 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_match_true(solution):
    ans = ['a', 'b', 'c', 'd', 'e']
    i = 1
    s = 'bcd'
    assert solution._match(ans, i, s) == True

def test_match_false(solution):
    ans = ['a', 'b', 'c', 'd', 'e']
    i = 1
    s = 'bce'
    assert solution._match(ans, i, s) == False

def test_match_out_of_bounds(solution):
    ans = ['a', 'b', 'c', 'd', 'e']
    i = 3
    s = 'de'
    assert solution._match(ans, i, s) == True

def test_match_empty_string(solution):
    ans = ['a', 'b', 'c', 'd', 'e']
    i = 2
    s = ''
    assert solution._match(ans, i, s) == True
