import pythoness
from typing import List, Optional

class Solution:
    
    def minCostGoodCaption(self, caption: str) -> str:
        """
        Convert a given string caption into a 'good caption' where each character appears in groups of at least 3 consecutive occurrences. Utilize operations to change any character to its adjacent in the alphabet, aiming for the minimum number of changes. Return the lexicographically smallest possible good caption or an empty string if conversion is impossible.
    
        Constraints:
        - 1 <= caption.length <= 5 * 10^4
        - The string consists only of lowercase English letters.
        """
        n = len(caption)
        if n < 3:
            return ''
        # Convert into array for easy mutation
        result = list(caption)
        i = 0
        while i < n:
            start = i
            char = result[start]
            count = 0
            # Count the consecutive characters
            while i < n and result[i] == char:
                i += 1
                count += 1
            if count < 3:
                # Determine which character to change it to
                new_char = char
                if char > 'a':
                    new_char = chr(ord(char) - 1)
                elif char < 'z':
                    new_char = chr(ord(char) + 1)
                # Apply change for at least 3 times
                for j in range(start, start + 3):
                    if j < n:
                        result[j] = new_char
                    else:
                        return ''  # Impossible to construct a good caption
                i = start + 3
        return ''.join(result)