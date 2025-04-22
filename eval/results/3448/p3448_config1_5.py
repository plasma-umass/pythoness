import pythoness
from typing import List, Optional

class Solution:
    
    def countSubstrings(self, s: str) -> int:
        """Counts the substrings of a digit string divisible by their non-zero last digit.
        Given a string `s` of digits, this function returns how many of its substrings can be divided by their last non-zero digit.
        Constraints: 1 <= len(s) <= 10^5, s contains digits only.
        """
        count = 0
        length = len(s)
        for i in range(length):
            num = 0
            for j in range(i, length):
                num = num * 10 + int(s[j])
                last_digit = int(s[j])
                if last_digit != 0 and num % last_digit == 0:
                    count += 1
                elif last_digit == 0:
                    continue
        return count