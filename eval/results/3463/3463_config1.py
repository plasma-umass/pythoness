import pythoness
from typing import List, Optional

@pythoness.spec(
    """You are given a string s consisting of digits. Perform the following operation repeatedly until the string has exactly two digits:

For each pair of consecutive digits in s, starting from the first digit, calculate a new digit as the sum of the two digits modulo 10.
Replace s with the sequence of newly calculated digits, maintaining the order in which they are computed.

Return true if the final two digits in s are the same; otherwise, return false.
 
Constraints:

3 <= s.length <= 10^5
s consists of only digits.""",
    tests=['hasSameDigits(s = "3902") == True', 'hasSameDigits(s = "34789") == False'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def hasSameDigits(s: str) -> bool:
    """"""

hasSameDigits(s = "3902") 