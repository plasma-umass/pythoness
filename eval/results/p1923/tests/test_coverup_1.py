# file: src/oracle1923.py:1-49
# asked: {"lines": [1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13, 15, 17, 19, 24, 27, 28, 29, 31, 33, 35, 36, 37, 39, 40, 41, 42, 43, 45, 46, 47, 49], "branches": [[10, 11], [10, 17], [12, 13], [12, 15], [27, 28], [27, 31], [28, 27], [28, 29], [39, 40], [39, 49], [41, 42], [41, 45], [46, 39], [46, 47]]}
# gained: {"lines": [1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13, 15, 17, 19, 24, 27, 28, 29, 31, 33, 35, 36, 37, 39, 40, 41, 42, 43, 45, 46, 47, 49], "branches": [[10, 11], [10, 17], [12, 13], [12, 15], [27, 28], [27, 31], [28, 27], [28, 29], [39, 40], [39, 49], [41, 42], [41, 45], [46, 39], [46, 47]]}

import pytest
from src.oracle1923 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_init(solution):
    assert solution.BASE == 165131
    assert solution.HASH == 8417508174513

def test_longestCommonSubpath(solution):
    paths = [[1, 2, 3, 4], [3, 4, 5, 6], [7, 8, 3, 4]]
    n = 3
    result = solution.longestCommonSubpath(n, paths)
    assert result == 2

def test_checkCommonSubpath(solution):
    paths = [[1, 2, 3, 4], [3, 4, 5, 6], [7, 8, 3, 4]]
    m = 2
    result = solution._checkCommonSubpath(paths, m)
    assert result == True

def test_rabinKarp(solution):
    path = [1, 2, 3, 4]
    m = 2
    result = solution._rabinKarp(path, m)
    expected_hashes = {solution._rabinKarp([1, 2], 2).pop(), solution._rabinKarp([2, 3], 2).pop(), solution._rabinKarp([3, 4], 2).pop()}
    assert result == expected_hashes
