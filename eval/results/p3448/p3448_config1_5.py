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
        current_value = 0
        for j in range(i, n):
            current_value = current_value * 10 + int(s[j])
            last_digit = int(s[j])
            # Check if last digit is non-zero and if the substring is divisible by the last digit
            if last_digit != 0 and current_value % last_digit == 0:
                count += 1
    return count
countSubstrings(s='12936')