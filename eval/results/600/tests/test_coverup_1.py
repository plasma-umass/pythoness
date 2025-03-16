# file: src/oracle600.py:4-18
# asked: {"lines": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18], "branches": [[8, 9], [8, 10], [12, 13], [12, 16], [13, 14], [13, 15]]}
# gained: {"lines": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18], "branches": [[8, 9], [8, 10], [12, 13], [12, 16], [13, 14], [13, 15]]}

import pytest
from src.oracle600 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_findIntegers_basic_case(solution):
    assert solution.findIntegers(0) == 1

def test_findIntegers_single_bit(solution):
    assert solution.findIntegers(1) == 2

def test_findIntegers_two_bits(solution):
    assert solution.findIntegers(2) == 3

def test_findIntegers_three_bits(solution):
    assert solution.findIntegers(3) == 3

def test_findIntegers_large_number(solution):
    assert solution.findIntegers(5) == 5

def test_findIntegers_no_consecutive_ones(solution):
    assert solution.findIntegers(8) == 6

def test_findIntegers_edge_case(solution):
    assert solution.findIntegers(1023) == 144

@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 5),
    (7, 5),
    (8, 6),
    (9, 7),
    (10, 8),
    (11, 8),
    (12, 8),
    (13, 8),
    (14, 8),
    (15, 8),
    (16, 9),
    (1023, 144)
])
def test_findIntegers_various_cases(solution, n, expected):
    assert solution.findIntegers(n) == expected
