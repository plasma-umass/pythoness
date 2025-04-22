import pythoness
from typing import List, Optional

class Solution:
    
    def hasSameDigits(self, s: str) -> bool:
        """
        Process a string of digits by repeatedly replacing it with a sequence of the sum of each pair of consecutive digits modulo 10 until only two digits remain. Return True if the final two digits are the same, otherwise return False. The input string has a length between 3 and 100,000 digits and consists solely of digits.
        """
        current_string = s
        while len(current_string) > 2:
            next_string = []
            for i in range(len(current_string) - 1):
                pair_sum = (int(current_string[i]) + int(current_string[i + 1])) % 10
                next_string.append(str(pair_sum))
            current_string = ''.join(next_string)
        return current_string[0] == current_string[1]