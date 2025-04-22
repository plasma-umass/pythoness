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
        from collections import defaultdict
        n = len(caption)
        if n < 3:
            return ''
        # Frequency count of each character
        freq = defaultdict(int)
        for c in caption:
            freq[c] += 1
        # Check if there are fewer than 3 unique letters
        if len(freq) < 3:
            return ''
        result = []
        i = 0
        while i < n:
            char = caption[i]
            count = 1
            # Count consecutive chars
            while i + 1 < n and caption[i + 1] == char:
                i += 1
                count += 1
            # If current group is large enough, add to result
            if count >= 3:
                result.append(char * count)
            else:
                # Try to make a good caption by adjusting the current group
                (start, end) = (i - count + 1, i + 1)
                if start > 0:
                    # Try increasing the previous character
                    prev_char = chr(ord(caption[start - 1]) + 1)
                    if prev_char <= 'z':
                        diff = min(3 - count, n - end)
                        result.append(prev_char * 3)
                        i += diff
                    else:
                        return ''
                if end < n:
                    # Try decreasing the next character
                    next_char = chr(ord(caption[end]) - 1)
                    if next_char >= 'a':
                        result.append(next_char * 3)
                        i += 3 - count
                    else:
                        return ''
            i += 1
        return ''.join(result)