import pythoness
from typing import List, Optional

class Solution:
    
    def generateString(self, str1: str, str2: str) -> str:
        """
        Generate the lexicographically smallest string from str1 and str2 given specific matching conditions.
        For each index in str1, if str1[i] is 'T', the substring of length m starting at that index must match str2,
        otherwise, it must not match. If generating such a string is not possible, return an empty string.
        """
        m = len(str2)
        n = len(str1)
        result = list(str1)  # Create a modifiable list of characters from str1
        # Iterate through each position in str1
        for i in range(n):
            if result[i] == 'T':
                if i + m > n or result[i:i + m] != ['T'] * m:
                    # If there's not enough room for str2 or there's a mismatch pattern of 'T's
                    return ''
                result[i:i + m] = list(str2)  # Replace with str2
        # Create the smallest possible valid result by prioritizing 'a' where no 'T'
        for i in range(n):
            if result[i] != 'T':
                result[i] = 'a'
        return ''.join(result)