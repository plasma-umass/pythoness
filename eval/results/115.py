import pythoness
from typing import List

@pythoness.spec(
    """Given two strings s and t, return the number of distinct subsequences of s which equals t.
The test cases are generated so that the answer fits on a 32-bit signed integer.
 
Constraints:

1 <= s.length, t.length <= 1000
s and t consist of English letters.""",
    tests=['numDistinct(s = "rabbbit", t = "rabbit") == 3', 'numDistinct(s = "babgbag", t = "bag") == 5'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def numDistinct(s: str, t: str) -> int:
    """"""

numDistinct()