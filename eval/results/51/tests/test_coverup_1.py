# file: src/oracle51.py:1-21
# asked: {"lines": [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 20, 21], "branches": [[9, 10], [9, 13], [13, 0], [13, 14], [14, 15], [14, 16]]}
# gained: {"lines": [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 20, 21], "branches": [[9, 10], [9, 13], [13, 0], [13, 14], [14, 15], [14, 16]]}

import pytest
from src.oracle51 import Solution

def test_solveNQueens_1():
    solution = Solution()
    result = solution.solveNQueens(1)
    expected = [['Q']]
    assert result == expected

def test_solveNQueens_2():
    solution = Solution()
    result = solution.solveNQueens(2)
    expected = []
    assert result == expected

def test_solveNQueens_3():
    solution = Solution()
    result = solution.solveNQueens(3)
    expected = []
    assert result == expected

def test_solveNQueens_4():
    solution = Solution()
    result = solution.solveNQueens(4)
    expected = [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."]
    ]
    assert result == expected
