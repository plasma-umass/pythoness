import pythoness
from typing import List

@pythoness.spec(
    """Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring.
 
Constraints:

0 <= s.length <= 3 * 10^4
s[i] is '(', or ')'.""",
    tests=['longestValidParentheses(s = "(()") == 2', 'longestValidParentheses(s = ")()())") == 4'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def longestValidParentheses(s: str) -> int:
    """"""

longestValidParentheses()