# file: src/oracle902.py:1-19
# asked: {"lines": [1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19], "branches": [[6, 7], [6, 9], [9, 10], [9, 19], [11, 12], [11, 16], [12, 13], [12, 14], [14, 11], [14, 15], [16, 9], [16, 17]]}
# gained: {"lines": [1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19], "branches": [[6, 7], [6, 9], [9, 10], [9, 19], [11, 12], [11, 16], [12, 13], [12, 14], [14, 11], [14, 15], [16, 9], [16, 17]]}

import pytest
from src.oracle902 import Solution

def test_atMostNGivenDigitSet_case1():
    solution = Solution()
    digits = ["1", "3", "5", "7"]
    n = 100
    assert solution.atMostNGivenDigitSet(digits, n) == 20

def test_atMostNGivenDigitSet_case2():
    solution = Solution()
    digits = ["1", "4", "9"]
    n = 1000000000
    assert solution.atMostNGivenDigitSet(digits, n) == 29523

def test_atMostNGivenDigitSet_case3():
    solution = Solution()
    digits = ["7"]
    n = 8
    assert solution.atMostNGivenDigitSet(digits, n) == 1

def test_atMostNGivenDigitSet_case4():
    solution = Solution()
    digits = ["3", "4", "8"]
    n = 4
    assert solution.atMostNGivenDigitSet(digits, n) == 2

def test_atMostNGivenDigitSet_case5():
    solution = Solution()
    digits = ["5", "6"]
    n = 19
    assert solution.atMostNGivenDigitSet(digits, n) == 2
