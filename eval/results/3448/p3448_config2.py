import pythoness
from typing import List, Optional

@pythoness.spec(
    """You are given a string s consisting of digits.
Return the number of substrings of s divisible by their non-zero last digit.
Note: A substring may contain leading zeros.
 
Constraints:

1 <= s.length <= 10^5
s consists of digits only.""",
    tests=['countSubstrings(s = "12936") == 11', 'countSubstrings(s = "5701283") == 18', 'countSubstrings(s = "1010101010") == 25'],
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def countSubstrings(s: str) -> int:
    """"""

countSubstrings(s = "12936") 