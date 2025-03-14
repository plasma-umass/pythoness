# file: src/oracle2872.py:1-29
# asked: {"lines": [1, 2, 9, 10, 12, 14, 16, 17, 18, 20, 21, 22, 24, 25, 26, 28, 29], "branches": [[16, 17], [16, 20], [17, 16], [17, 18], [20, 21], [20, 22], [24, 25], [24, 28]]}
# gained: {"lines": [1, 2, 9, 10, 12, 14, 16, 17, 18, 20, 21, 22, 24, 25, 26, 28, 29], "branches": [[16, 17], [16, 20], [17, 16], [17, 18], [20, 21], [24, 25], [24, 28]]}

import pytest
from src.oracle2872 import Solution

def test_maxKDivisibleComponents():
    solution = Solution()
    
    # Test case 1
    n = 3
    edges = [[0, 1], [1, 2]]
    values = [3, 6, 9]
    k = 3
    assert solution.maxKDivisibleComponents(n, edges, values, k) == 3
    
    # Test case 2
    n = 4
    edges = [[0, 1], [1, 2], [1, 3]]
    values = [2, 4, 6, 8]
    k = 2
    assert solution.maxKDivisibleComponents(n, edges, values, k) == 4
    
    # Test case 3
    n = 5
    edges = [[0, 1], [0, 2], [1, 3], [1, 4]]
    values = [1, 2, 3, 4, 5]
    k = 1
    assert solution.maxKDivisibleComponents(n, edges, values, k) == 5

    # Test case 4
    n = 2
    edges = [[0, 1]]
    values = [5, 10]
    k = 5
    assert solution.maxKDivisibleComponents(n, edges, values, k) == 2

    # Test case 5
    n = 1
    edges = []
    values = [7]
    k = 7
    assert solution.maxKDivisibleComponents(n, edges, values, k) == 1
