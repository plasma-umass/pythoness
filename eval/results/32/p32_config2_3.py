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
        if char == '(':  # push the index of the '(' onto the stack
            stack.append(i)
        else:  # char == ')'
            stack.pop()  # pop the last '(' index or the base index
            if not stack:  # if stack is empty after popping
                stack.append(i)  # append the current index as the new base
            else:
                # Calculate the current length of the valid substring
                max_length = max(max_length, i - stack[-1])
    return max_length
longestValidParentheses(s='(()')