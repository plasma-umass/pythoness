import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """
        Find the length of the shortest substring in string `s` that matches the pattern `p`, where `p` contains exactly two '*' characters, each matching any sequence of characters. If no such substring exists, return -1. The empty substring is valid.
    
        Constraints: 1 <= s.length <= 10^5, 2 <= p.length <= 10^5, `s` contains only lowercase English letters, and `p` contains only lowercase English letters with exactly two '*'.
        """
        # Split the pattern `p` by '*', which will give us three parts: before the first '*', between the two '*', and after the second '*'.
        parts = p.split('*')
        if len(parts) != 3:
            return -1  # Invalid pattern as it doesn't contain exactly two '*'.
        (prefix, middle, suffix) = parts
        (n, m) = (len(s), len(prefix) + len(middle) + len(suffix))
        min_len = float('inf')
        # We'll use a sliding window to try and match the prefix and suffix around each possible middle match
        for start in range(n):
            # Check if the prefix of `p` matches the start suffix of sliding window
            if start + len(prefix) > n:
                break
            if s[start:start + len(prefix)] != prefix:
                continue
            for end in range(start + len(prefix), n + 1):
                # Check if the suffix of `p` matches the end prefix of sliding window
                if end + len(suffix) > n:
                    break
                if end + len(suffix) > start + len(prefix) and s[end:end + len(suffix)] == suffix and (middle in s[start + len(prefix):end]):
                    min_len = min(min_len, end + len(suffix) - start)
                    break
        return -1 if min_len == float('inf') else min_len