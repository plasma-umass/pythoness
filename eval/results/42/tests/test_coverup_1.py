# file: src/oracle42.py:1-14
# asked: {"lines": [1, 2, 3, 4, 5, 7, 8, 10, 11, 13, 14], "branches": [[7, 8], [7, 10], [10, 11], [10, 13]]}
# gained: {"lines": [1, 2, 3, 4, 5, 7, 8, 10, 11, 13, 14], "branches": [[7, 8], [7, 10], [10, 11], [10, 13]]}

import pytest
from src.oracle42 import Solution

@pytest.mark.parametrize("height, expected", [
    ([0,1,0,2,1,0,1,3,2,1,2,1], 6),
    ([4,2,0,3,2,5], 9),
    ([], 0),
    ([1], 0),
    ([2,0,2], 2)
])
def test_trap(height, expected):
    solution = Solution()
    assert solution.trap(height) == expected
