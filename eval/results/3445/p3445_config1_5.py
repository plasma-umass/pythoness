import pythoness
from typing import List, Optional

class Solution:
    
    def maxDifference(self, s: str, k: int) -> int:
        """
        Find the maximum difference between the frequency of two characters in a substring of a given string,
        where one character has an odd frequency and the other an even frequency, and the substring size is at least k.
        The substring can contain more than two distinct characters, and the input guarantees the presence of at least
        one such valid substring. This problem is constrained by string lengths ranging from 3 to 30,000, containing
        only digits from '0' to '4'.
        """
    
        def is_valid(freqs):
            # Function to check if there's at least one character with odd frequency and one with even frequency
            has_odd = any((f % 2 == 1 for f in freqs))
            has_even = any((f % 2 == 0 and f > 0 for f in freqs))
            return has_odd and has_even
        n = len(s)
        max_diff = 0
        # Try every possible substring of size >= k
        for start in range(n):
            # Frequency array for '0' to '4'
            freqs = [0] * 5
            for end in range(start, n):
                freqs[int(s[end])] += 1
                # Consider substrings of length at least k
                if end - start + 1 >= k and is_valid(freqs):
                    # Get maximum odd frequency and minimum even frequency
                    odd_freqs = [f for f in freqs if f % 2 == 1]
                    even_freqs = [f for f in freqs if f % 2 == 0 and f > 0]
                    if odd_freqs and even_freqs:
                        max_odd = max(odd_freqs)
                        min_even = min(even_freqs)
                        max_diff = max(max_diff, abs(max_odd - min_even))
        return max_diff