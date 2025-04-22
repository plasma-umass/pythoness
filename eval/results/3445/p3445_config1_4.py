import pythoness
from typing import List, Optional

class Solution:
    
    def maxDifference(self, s: str, k: int) -> int:
        """
        Find the maximum difference between the frequency of two characters in a substring of a given string, where one character has an odd frequency and the other an even frequency, 
        and the substring size is at least k. The substring can contain more than two distinct characters, and the input guarantees the presence of at least one such valid substring. 
        This problem is constrained by string lengths ranging from 3 to 30,000, containing only digits from '0' to '4'.
        """
    
        def is_valid_substring(freq):
            odd_freq = even_freq = 0
            for f in freq:
                if f % 2 == 0 and f != 0:
                    even_freq += 1
                elif f % 2 == 1:
                    odd_freq += 1
            return odd_freq > 0 and even_freq > 0
        n = len(s)
        max_diff = 0
        for start in range(n):
            freq = [0] * 5  # As digits in s are in the range '0' to '4'
            for end in range(start, n):
                freq[int(s[end])] += 1
                if end - start + 1 >= k and is_valid_substring(freq):
                    odd_max = even_max = 0
                    for f in freq:
                        if f % 2 == 0:
                            even_max = max(even_max, f)
                        else:
                            odd_max = max(odd_max, f)
                    max_diff = max(max_diff, abs(odd_max - even_max))
        return max_diff