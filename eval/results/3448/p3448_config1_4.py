import pythoness
from typing import List, Optional

class Solution:
    
    def countSubstrings(self, s: str) -> int:
        """
        Counts the substrings of a digit string divisible by their non-zero last digit.
        Given a string `s` of digits, this function returns how many of its substrings can be divided by their last non-zero digit.
        Constraints: 1 <= len(s) <= 10^5, s contains digits only.
        """
        count = 0
        n = len(s)
        for i in range(n):
            last_digit = int(s[i])
            if last_digit == 0:
                continue
            num = 0
            for j in range(i, n):
                num = num * 10 + (ord(s[j]) - ord('0'))
                if num % last_digit == 0:
                    count += 1
        return count