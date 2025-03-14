# file: src/oracle41.py:1-17
# asked: {"lines": [1, 2, 3, 9, 10, 11, 13, 14, 15, 17], "branches": [[9, 10], [9, 13], [10, 9], [10, 11], [13, 14], [13, 17], [14, 13], [14, 15]]}
# gained: {"lines": [1, 2, 3, 9, 10, 11, 13, 14, 15, 17], "branches": [[9, 10], [9, 13], [10, 9], [10, 11], [13, 14], [13, 17], [14, 13], [14, 15]]}

import pytest
from src.oracle41 import Solution

@pytest.mark.parametrize("nums, expected", [
    ([1, 2, 0], 3),
    ([3, 4, -1, 1], 2),
    ([7, 8, 9, 11, 12], 1),
    ([1, 2, 3, 4, 5], 6),
    ([2, 3, 4, 5, 6], 1),
    ([0, 0, 0, 0, 0], 1),
    ([1], 2),
    ([2], 1),
    ([], 1)
])
def test_firstMissingPositive(nums, expected):
    solution = Solution()
    assert solution.firstMissingPositive(nums) == expected

def test_firstMissingPositive_cleanup(monkeypatch):
    solution = Solution()
    nums = [3, 4, -1, 1]
    expected = 2
    assert solution.firstMissingPositive(nums) == expected
    # Ensure no state pollution
    nums = [1, 2, 0]
    expected = 3
    assert solution.firstMissingPositive(nums) == expected
