# file: src/oracle3464.py:60-70
# asked: {"lines": [60, 65, 66, 67, 68, 69, 70], "branches": []}
# gained: {"lines": [60, 65, 66, 67, 68, 69, 70], "branches": []}

import pytest
from src.oracle3464 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_getOrderedPoints_all_quadrants(solution):
    points = [
        (0, 1), (0, 2),  # left
        (1, 3), (2, 3),  # top
        (3, 2), (3, 1),  # right
        (1, 0), (2, 0)   # bottom
    ]
    side = 3
    expected = [
        (0, 1), (0, 2),  # left
        (1, 3), (2, 3),  # top
        (3, 2), (3, 1),  # right
        (2, 0), (1, 0)   # bottom
    ]
    result = solution._getOrderedPoints(side, points)
    assert result == expected

def test_getOrderedPoints_empty(solution):
    points = []
    side = 3
    expected = []
    result = solution._getOrderedPoints(side, points)
    assert result == expected

def test_getOrderedPoints_only_left(solution):
    points = [(0, 1), (0, 2)]
    side = 3
    expected = [(0, 1), (0, 2)]
    result = solution._getOrderedPoints(side, points)
    assert result == expected

def test_getOrderedPoints_only_top(solution):
    points = [(1, 3), (2, 3)]
    side = 3
    expected = [(1, 3), (2, 3)]
    result = solution._getOrderedPoints(side, points)
    assert result == expected

def test_getOrderedPoints_only_right(solution):
    points = [(3, 2), (3, 1)]
    side = 3
    expected = [(3, 2), (3, 1)]
    result = solution._getOrderedPoints(side, points)
    assert result == expected

def test_getOrderedPoints_only_bottom(solution):
    points = [(1, 0), (2, 0)]
    side = 3
    expected = [(2, 0), (1, 0)]
    result = solution._getOrderedPoints(side, points)
    assert result == expected
