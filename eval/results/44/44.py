import pythoness
from typing import List


@pythoness.spec(
    """Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:

'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).

The matching should cover the entire input string (not partial).
 
Constraints:

0 <= s.length, p.length <= 2000
s contains only lowercase English letters.
p contains only lowercase English letters, '?' or '*'.""",
    tests=[
        'isMatch(s = "aa", p = "a") == False',
        'isMatch(s = "aa", p = "*") == True',
        'isMatch(s = "cb", p = "?a") == False',
    ],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def isMatch(s: str, p: str) -> bool:
    """"""


isMatch(s="aa", p="a")
