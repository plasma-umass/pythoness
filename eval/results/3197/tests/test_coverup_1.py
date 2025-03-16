# file: src/oracle3197.py:70-89
# asked: {"lines": [70, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89], "branches": [[82, 83], [82, 89], [83, 82], [83, 84], [84, 83], [84, 85]]}
# gained: {"lines": [70, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89], "branches": [[82, 83], [82, 89], [83, 82], [83, 84], [84, 83], [84, 85]]}

import pytest
from src.oracle3197 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_minimum_area_no_ones(solution):
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert solution._minimumArea(grid, 0, 2, 0, 2) == 0

def test_minimum_area_single_one(solution):
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    assert solution._minimumArea(grid, 0, 2, 0, 2) == 1

def test_minimum_area_multiple_ones(solution):
    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 0]
    ]
    assert solution._minimumArea(grid, 0, 2, 0, 2) == 4

def test_minimum_area_entire_grid(solution):
    grid = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    assert solution._minimumArea(grid, 0, 2, 0, 2) == 9

def test_minimum_area_partial_grid(solution):
    grid = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    assert solution._minimumArea(grid, 1, 2, 1, 2) == 4
