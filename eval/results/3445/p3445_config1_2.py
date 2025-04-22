import pythoness
from typing import List, Optional

class Solution:
    
    def maxDifference(self, s: str, k: int) -> int:
        """
        Find the maximum difference between the frequency of two characters in a substring of a given string,
        where one character has an odd frequency and the other an even frequency, and the substring size is
        at least k. The substring can contain more than two distinct characters, and the input guarantees the
        presence of at least one such valid substring. This problem is constrained by string lengths ranging
        from 3 to 30,000, containing only digits from '0' to '4'.
        """
        from collections import Counter
        max_diff = 0
        n = len(s)
        for start in range(n):
            count = Counter()
            even_frequencies = {}
            odd_frequencies = {}
            for end in range(start, n):
                count[s[end]] += 1
                if count[s[end]] % 2 == 0:
                    even_frequencies[s[end]] = count[s[end]]
                    if s[end] in odd_frequencies:
                        del odd_frequencies[s[end]]
                else:
                    odd_frequencies[s[end]] = count[s[end]]
                    if s[end] in even_frequencies:
                        del even_frequencies[s[end]]
                if end - start + 1 >= k:
                    # Calculate max difference between any odd frequency and any even frequency
                    if odd_frequencies and even_frequencies:
                        max_odd = max(odd_frequencies.values())
                        max_even = max(even_frequencies.values())
                        max_diff = max(max_diff, abs(max_odd - max_even))
        return max_diff