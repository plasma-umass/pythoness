import pythoness
from typing import List, Optional

@pythoness.spec(
    """You are given a string s and a pattern string p, where p contains exactly two '*' characters.
The '*' in p matches any sequence of zero or more characters.
Return the length of the shortest substring in s that matches p. If there is no such substring, return -1.
Note: The empty substring is considered valid.
 
Constraints:

1 <= s.length <= 10^5
2 <= p.length <= 10^5
s contains only lowercase English letters.
p contains only lowercase English letters and exactly two '*'.""",
    tests=['shortestMatchingSubstring(s = "abaacbaecebce", p = "ba*c*ce") == 8', 'shortestMatchingSubstring(s = "baccbaadbc", p = "cc*baa*adb") == -1', 'shortestMatchingSubstring(s = "a", p = "**") == 0', 'shortestMatchingSubstring(s = "madlogic", p = "*adlogi*") == 6'],
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def shortestMatchingSubstring(s: str, p: str) -> int:
    """"""

shortestMatchingSubstring(s = "abaacbaecebce", p = "ba*c*ce") 