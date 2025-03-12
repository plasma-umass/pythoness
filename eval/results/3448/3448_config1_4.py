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
    n = len(s)
    count = 0
    for i in range(n):
        current_number = 0
        for j in range(i, n):
            current_number = current_number * 10 + int(s[j])
            last_digit = int(s[j])
            # Check divisibility by the last digit if it's not zero
            if last_digit != 0 and current_number % last_digit == 0:
                count += 1
    return count
countSubstrings(s='12936')