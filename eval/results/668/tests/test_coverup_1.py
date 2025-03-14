# file: src/oracle668.py:1-13
# asked: {"lines": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13], "branches": [[4, 5], [4, 13], [7, 8], [7, 9], [9, 10], [9, 12]]}
# gained: {"lines": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13], "branches": [[4, 5], [4, 13], [7, 8], [7, 9], [9, 10], [9, 12]]}

import pytest
from src.oracle668 import Solution

def test_findKthNumber_case1():
    sol = Solution()
    assert sol.findKthNumber(3, 3, 5) == 3

def test_findKthNumber_case2():
    sol = Solution()
    assert sol.findKthNumber(2, 3, 6) == 6

def test_findKthNumber_case3():
    sol = Solution()
    assert sol.findKthNumber(3, 3, 1) == 1

def test_findKthNumber_case4():
    sol = Solution()
    assert sol.findKthNumber(3, 3, 9) == 9

def test_findKthNumber_case5():
    sol = Solution()
    assert sol.findKthNumber(1, 10, 3) == 3

def test_findKthNumber_case6():
    sol = Solution()
    assert sol.findKthNumber(10, 1, 7) == 7
