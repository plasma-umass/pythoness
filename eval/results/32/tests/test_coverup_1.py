# file: src/oracle32.py:1-12
# asked: {"lines": [1, 2, 3, 6, 8, 9, 10, 12], "branches": [[8, 9], [8, 12], [9, 8], [9, 10]]}
# gained: {"lines": [1, 2, 3, 6, 8, 9, 10, 12], "branches": [[8, 9], [8, 12], [9, 8], [9, 10]]}

import pytest
from src.oracle32 import Solution

def test_longestValidParentheses():
    solution = Solution()
    
    # Test case 1: Simple case
    s = "(()"
    assert solution.longestValidParentheses(s) == 2
    
    # Test case 2: Another simple case
    s = ")()())"
    assert solution.longestValidParentheses(s) == 4
    
    # Test case 3: No valid parentheses
    s = ")))"
    assert solution.longestValidParentheses(s) == 0
    
    # Test case 4: All valid parentheses
    s = "()()"
    assert solution.longestValidParentheses(s) == 4
    
    # Test case 5: Nested valid parentheses
    s = "((()))"
    assert solution.longestValidParentheses(s) == 6

    # Test case 6: Empty string
    s = ""
    assert solution.longestValidParentheses(s) == 0
