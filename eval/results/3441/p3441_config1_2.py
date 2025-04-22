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
        result = []
        i = 0
        while i < n:
            count = 1
            # Count consecutive identical characters
            while i + 1 < n and caption[i] == caption[i + 1]:
                count += 1
                i += 1
            if count >= 3:
                result.extend([caption[i]] * count)
            else:
                needed = 3 - count
                changes = []
                for j in range(3):
                    modified = caption[i] if j < count else chr(ord(caption[i]) + 1)
                    changes.append(modified)
                changes.sort()
                result.extend(changes[:3])
            i += 1
        return ''.join(result)