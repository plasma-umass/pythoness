import pythoness
from typing import List, Optional

@pythoness.spec(
    """Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring.
 
Constraints:

0 <= s.length <= 3 * 10^4
s[i] is '(', or ')'.""",
    tests=['longestValidParentheses(s = "(()") == 2', 'longestValidParentheses(s = ")()())") == 4', 'longestValidParentheses(s = "") == 0'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def longestValidParentheses(s: str) -> int:
    """"""

longestValidParentheses(s = "(()") 