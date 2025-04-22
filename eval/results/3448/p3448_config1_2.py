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
        # Iterate over every possible starting point of the substring
        for start in range(n):
            number = 0
            # Iterate over every possible ending point of the substring
            for end in range(start, n):
                number = number * 10 + int(s[end])
                last_digit = int(s[end])
                # Only consider substrings with non-zero last digit
                if last_digit != 0 and number % last_digit == 0:
                    count += 1
        return count