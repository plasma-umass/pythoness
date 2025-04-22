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
        # This function may use the given classes and functions as tools for implementation
        n = len(caption)
        if n < 3:
            return ''
        # Store the result as a list for efficient character appending
        result = []
        i = 0
        while i < n:
            start = i
            # Find end of current character sequence
            while i < n and caption[start] == caption[i]:
                i += 1
            length = i - start
            if length >= 3:
                result.append(caption[start] * length)
            else:
                best_char = caption[start]
                if best_char > 'a':
                    left = max(ord(best_char) - 1, ord('a'))
                    result.append(chr(left) * 3)
                elif best_char < 'z':
                    right = min(ord(best_char) + 1, ord('z'))
                    result.append(chr(right) * 3)
                else:
                    return ''
        return ''.join(result)