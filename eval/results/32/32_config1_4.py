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
    stack = [-1]
    for (i, char) in enumerate(s):
        if char == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                max_length = max(max_length, i - stack[-1])
    return max_length
longestValidParentheses(s='(()')