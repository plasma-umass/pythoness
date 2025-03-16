import pythoness
from typing import List, Optional

def longestValidParentheses(s: str) -> int:
    """
    Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring.

    Constraints:

    0 <= s.length <= 3 * 10^4
    s[i] is '(', or ')'.
    """
    max_length = 0
    stack = [-1]  # Stack to keep track of indices
    for (i, char) in enumerate(s):
        if char == '(':  # Push the index onto the stack if '(' is found
            stack.append(i)
        else:  # When ')' is found
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                max_length = max(max_length, i - stack[-1])
    return max_length
longestValidParentheses(s='(()')