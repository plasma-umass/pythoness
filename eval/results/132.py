import pythoness
from typing import List

@pythoness.spec(
    """Given a string s, partition s such that every substring of the partition is a palindrome.
Return the minimum cuts needed for a palindrome partitioning of s.
 
Constraints:

1 <= s.length <= 2000
s consists of lowercase English letters only.""",
    tests=['minCut(s = "aab") == 1'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def minCut(s: str) -> int:
    """"""

minCut()