import pythoness
from typing import List, Optional

@pythoness.spec(
    """Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:

'.' Matches any single character.    
'*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).
 
Constraints:

1 <= s.length <= 20
1 <= p.length <= 20
s contains only lowercase English letters.
p contains only lowercase English letters, '.', and '*'.
It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.""",
    tests=['isMatch(s = "aa", p = "a") == False', 'isMatch(s = "aa", p = "a*") == True', 'isMatch(s = "ab", p = ".*") == True'],
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

isMatch(s = "aa", p = "a") 