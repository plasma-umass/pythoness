import pythoness
from typing import List, Optional

class Solution:
    
    def maxDifference(self, s: str, k: int) -> int:
        """
        Find the maximum difference between the frequency of two characters in a substring
        of a given string, where one character has an odd frequency and the other an
        even frequency, and the substring size is at least k. The substring can contain
        more than two distinct characters, and the input guarantees the presence of at
        least one such valid substring. This problem is constrained by string lengths
        ranging from 3 to 30,000, containing only digits from '0' to '4'.
        """
        max_diff = 0
        n = len(s)
        for start in range(n):
            freq = [0] * 5  # Since the string only contains '0' to '4'
            for end in range(start, n):
                freq[int(s[end])] += 1
                if end - start + 1 >= k:
                    odd_freqs = [f for f in freq if f % 2 == 1]
                    even_freqs = [f for f in freq if f % 2 == 0]
                    if odd_freqs and even_freqs:
                        max_odd = max(odd_freqs)
                        max_even = max(even_freqs)
                        max_diff = max(max_diff, abs(max_odd - max_even))
        return max_diff