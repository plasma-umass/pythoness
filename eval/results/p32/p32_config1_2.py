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
        if char == '(':  # Push the index of the '(' onto the stack
            stack.append(i)
        else:  # Pop the topmost element 
            stack.pop()
            if len(stack) == 0:  # If the stack is empty, push the current index
                stack.append(i)
            else:
                # Calculate the length of the current valid substring
                length = i - stack[-1]
                max_length = max(max_length, length)
    return max_length
longestValidParentheses(s='(()')