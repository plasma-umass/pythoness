import pythoness
from typing import List, Optional

class Solution:
    
    def hasSameDigits(self, s: str) -> bool:
        """
        Process a string of digits by repeatedly replacing it with a sequence of the sum of each pair of consecutive digits modulo 10 until only two digits remain. Return True if the final two digits are the same, otherwise return False. The input string has a length between 3 and 100,000 digits and consists solely of digits.
        """
        while len(s) > 2:
            s = ''.join((str((int(s[i]) + int(s[i + 1])) % 10) for i in range(len(s) - 1)))
        return s[0] == s[1]