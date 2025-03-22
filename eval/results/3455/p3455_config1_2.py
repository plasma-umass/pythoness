import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """
        Find the length of the shortest substring in string `s` that matches the pattern `p`, where `p` contains exactly two '*' characters, each matching any sequence of characters. If no such substring exists, return -1. The empty substring is valid.
    
        Constraints: 1 <= s.length <= 10^5, 2 <= p.length <= 10^5, `s` contains only lowercase English letters, and `p` contains only lowercase English letters with exactly two '*'.
        """
        # Split the pattern `p` on '*' characters.
        parts = p.split('*')
        if len(parts) != 3:
            return -1
        (left, middle, right) = parts
        # Initialize variables.
        min_length = float('inf')
        left_len = len(left)
        right_len = len(right)
        # Check all possible substrings in `s`.
        for i in range(len(s)):
            if s[i:i + left_len] == left:
                # Find the starting index after the left part.
                start = i + left_len
                # Look for `right` starting from `start` position.
                for j in range(start, len(s) + 1):
                    # If `right` is matched, check the middle part in between.
                    if s[j:j + right_len] == right:
                        if middle in s[start:j]:
                            # Update the minimum length.
                            min_length = min(min_length, j + right_len - i)
                        break
        # Return the result.
        return min_length if min_length != float('inf') else -1