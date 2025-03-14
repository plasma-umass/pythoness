# file: src/oracle493.py:4-32
# asked: {"lines": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 32], "branches": [[7, 8], [7, 9], [13, 14], [13, 19], [14, 15], [14, 17], [20, 21], [20, 27], [21, 22], [21, 25]]}
# gained: {"lines": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 32], "branches": [[7, 8], [7, 9], [13, 14], [13, 19], [14, 15], [14, 17], [20, 21], [20, 27], [21, 22], [21, 25]]}

import pytest
from src.oracle493 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_reverse_pairs_no_pairs(solution):
    nums = [1, 2, 3, 4, 5]
    assert solution.reversePairs(nums) == 0
    assert nums == [1, 2, 3, 4, 5]  # Ensure the list remains sorted

def test_reverse_pairs_with_pairs(solution):
    nums = [5, 4, 3, 2, 1]
    assert solution.reversePairs(nums) == 4
    assert nums == [1, 2, 3, 4, 5]  # Ensure the list is sorted after function call

def test_reverse_pairs_mixed(solution):
    nums = [2, 4, 3, 5, 1]
    assert solution.reversePairs(nums) == 3
    assert nums == [1, 2, 3, 4, 5]  # Ensure the list is sorted after function call

def test_reverse_pairs_single_element(solution):
    nums = [1]
    assert solution.reversePairs(nums) == 0
    assert nums == [1]  # Ensure the list remains unchanged

def test_reverse_pairs_empty(solution):
    nums = []
    assert solution.reversePairs(nums) == 0
    assert nums == []  # Ensure the list remains unchanged
