import pythoness
from typing import List, Optional

def countSubstrings(s: str) -> int:
    """
    You are given a string s consisting of digits.
    Return the number of substrings of s divisible by their non-zero last digit.
    Note: A substring may contain leading zeros.

    Constraints:

    1 <= s.length <= 10^5
    s consists of digits only.
    """
    count = 0
    n = len(s)
    for i in range(n):
        num = 0
        for j in range(i, n):
            num = num * 10 + int(s[j])
            last_digit = int(s[j])
            if last_digit != 0 and num % last_digit == 0:
                count += 1
    return count
countSubstrings(s='12936')