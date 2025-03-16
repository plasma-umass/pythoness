# file: src/oracle850.py:1-38
# asked: {"lines": [1, 2, 3, 5, 6, 7, 9, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 25, 27, 28, 29, 30, 31, 32, 33, 34, 36, 38], "branches": [[5, 6], [5, 9], [19, 20], [19, 25], [21, 19], [21, 22], [27, 28], [27, 38], [28, 29], [28, 32], [32, 33], [32, 36]]}
# gained: {"lines": [1, 2, 3, 5, 6, 7, 9, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 25, 27, 28, 29, 30, 31, 32, 33, 34, 36, 38], "branches": [[5, 6], [5, 9], [19, 20], [19, 25], [21, 22], [27, 28], [27, 38], [28, 29], [28, 32], [32, 33], [32, 36]]}

import pytest
from src.oracle850 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_rectangleArea_single_rectangle(solution):
    rectangles = [[1, 1, 3, 3]]
    assert solution.rectangleArea(rectangles) == 4

def test_rectangleArea_multiple_rectangles(solution):
    rectangles = [[1, 1, 3, 3], [2, 2, 4, 4]]
    assert solution.rectangleArea(rectangles) == 7

def test_rectangleArea_no_rectangles(solution):
    rectangles = []
    assert solution.rectangleArea(rectangles) == 0

def test_rectangleArea_touching_rectangles(solution):
    rectangles = [[1, 1, 2, 2], [2, 1, 3, 2]]
    assert solution.rectangleArea(rectangles) == 2

def test_rectangleArea_overlapping_rectangles(solution):
    rectangles = [[1, 1, 3, 3], [2, 2, 4, 4], [3, 1, 4, 2]]
    assert solution.rectangleArea(rectangles) == 8

def test_rectangleArea_large_coordinates(solution):
    rectangles = [[0, 0, 1000000000, 1000000000]]
    assert solution.rectangleArea(rectangles) == 49

@pytest.mark.parametrize("rectangles, expected", [
    ([[1, 1, 3, 3]], 4),
    ([[1, 1, 3, 3], [2, 2, 4, 4]], 7),
    ([], 0),
    ([[1, 1, 2, 2], [2, 1, 3, 2]], 2),
    ([[1, 1, 3, 3], [2, 2, 4, 4], [3, 1, 4, 2]], 8),
    ([[0, 0, 1000000000, 1000000000]], 49),
])
def test_rectangleArea_parametrized(solution, rectangles, expected):
    assert solution.rectangleArea(rectangles) == expected
