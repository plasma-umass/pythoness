import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """
        Find the length of the shortest substring in string `s` that matches the pattern `p`, where `p` contains exactly two '*' characters, each matching any sequence of characters. If no such substring exists, return -1. The empty substring is valid.
    
        Constraints: 1 <= s.length <= 10^5, 2 <= p.length <= 10^5, `s` contains only lowercase English letters, and `p` contains only lowercase English letters with exactly two '*'.
        """
        # Split the pattern on '*' to get the fixed parts
        parts = p.split('*')
        if len(parts) != 3:
            return -1  # Pattern must contain exactly two '*'
        (left, middle, right) = (parts[0], parts[1], parts[2])
        # Use two pointers to find the shortest match
        n = len(s)
        min_length = float('inf')
        # Iterate over each possible starting point for left
        for i in range(n):
            # Try to match the left part at position i
            if s[i:i + len(left)] == left:
                # Find where we can start matching the middle part
                for j in range(i + len(left), n):
                    # Try to match the right part starting from j
                    if s[j:j + len(right)] == right:
                        # Check if the middle part appears in between
                        middle_start = s.find(middle, i + len(left), j)
                        if middle_start != -1:
                            # Calculate the full match length
                            match_length = j + len(right) - i
                            min_length = min(min_length, match_length)
        return min_length if min_length != float('inf') else -1