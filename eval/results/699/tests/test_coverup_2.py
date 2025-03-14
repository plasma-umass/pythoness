# file: src/oracle699.py:66-77
# asked: {"lines": [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77], "branches": [[71, 72], [71, 77]]}
# gained: {"lines": [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77], "branches": [[71, 72], [71, 77]]}

import pytest
from src.oracle699 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_falling_squares_single_position(solution):
    positions = [[1, 2]]
    expected = [2]
    result = solution.fallingSquares(positions)
    assert result == expected

def test_falling_squares_multiple_positions(solution):
    positions = [[1, 2], [2, 3], [6, 1]]
    expected = [2, 5, 5]
    result = solution.fallingSquares(positions)
    assert result == expected

def test_falling_squares_overlapping_positions(solution):
    positions = [[1, 2], [2, 2], [3, 1]]
    expected = [2, 4, 5]
    result = solution.fallingSquares(positions)
    assert result == expected

def test_falling_squares_non_overlapping_positions(solution):
    positions = [[1, 2], [4, 3], [8, 1]]
    expected = [2, 3, 3]
    result = solution.fallingSquares(positions)
    assert result == expected

def test_falling_squares_large_input(solution):
    positions = [[1, 1000000000]]
    expected = [1000000000]
    result = solution.fallingSquares(positions)
    assert result == expected
