# file: src/oracle466.py:10-35
# asked: {"lines": [10, 11, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 31, 32, 33, 35], "branches": [[18, 19], [18, 28], [20, 21], [20, 26], [21, 20], [21, 22], [23, 20], [23, 24], [31, 32], [31, 35]]}
# gained: {"lines": [10, 11, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 31, 32, 33, 35], "branches": [[18, 19], [18, 28], [20, 21], [20, 26], [21, 20], [21, 22], [23, 20], [23, 24], [31, 32], [31, 35]]}

import pytest
from src.oracle466 import Solution, Record

def test_getMaxRepetitions():
    solution = Solution()
    
    # Test case to cover lines 10-35
    s1 = "acb"
    n1 = 4
    s2 = "ab"
    n2 = 2
    
    result = solution.getMaxRepetitions(s1, n1, s2, n2)
    
    # Verify the result
    assert result == 2

    # Additional test case to ensure full coverage
    s1 = "abc"
    n1 = 3
    s2 = "ac"
    n2 = 1
    
    result = solution.getMaxRepetitions(s1, n1, s2, n2)
    
    # Verify the result
    assert result == 3

    # Clean up if necessary (not needed in this case as no state is maintained)

