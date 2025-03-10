import pythoness
from typing import List

@pythoness.spec(
    """Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".
The testcases will be generated such that the answer is unique.
 
Constraints:

m == s.length
n == t.length
1 <= m, n <= 10^5
s and t consist of uppercase and lowercase English letters.

 
Follow up: Could you find an algorithm that runs in O(m + n) time?""",
    tests=['minWindow(s = "ADOBECODEBANC", t = "ABC") == "BANC"', 'minWindow(s = "a", t = "a") == "a"', 'minWindow(s = "a", t = "aa") == ""'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound="O(m + n)"
)
def minWindow(s: str, t: str) -> str:
    """"""

minWindow()