# file: src/oracle552.py:1-30
# asked: {"lines": [1, 2, 3, 5, 6, 8, 9, 12, 15, 18, 21, 22, 25, 28, 30], "branches": [[8, 9], [8, 30]]}
# gained: {"lines": [1, 2, 3, 5, 6, 8, 9, 12, 15, 18, 21, 22, 25, 28, 30], "branches": [[8, 9], [8, 30]]}

import pytest
from src.oracle552 import Solution

def test_checkRecord():
    solution = Solution()
    
    # Test case 1: n = 1
    assert solution.checkRecord(1) == 3  # "P", "L", "A"
    
    # Test case 2: n = 2
    assert solution.checkRecord(2) == 8  # "PP", "PL", "LP", "LL", "AP", "AL", "PA", "LA"
    
    # Test case 3: n = 3
    assert solution.checkRecord(3) == 19  # Various combinations
    
    # Test case 4: n = 0
    assert solution.checkRecord(0) == 1  # Empty string is a valid record
    
    # Test case 5: Larger n
    assert solution.checkRecord(4) == 43  # Various combinations

    # Clean up if necessary (not needed in this case as no state is maintained between tests)
