import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """
        Find the length of the shortest substring in string `s` that matches the pattern `p`, where `p` contains exactly two '*' characters, each matching any sequence of characters. If no such substring exists, return -1. The empty substring is valid.
    
        Constraints: 1 <= s.length <= 10^5, 2 <= p.length <= 10^5, `s` contains only lowercase English letters, and `p` contains only lowercase English letters with exactly two '*'.
        """
        parts = p.split('*')
        if len(parts) != 3:
            return -1  # should not happen due to constraints, as p is guaranteed to have exactly two '*'
        # Trim the parts, as there might be empty leading or trailing parts if * is first or last
        prefix = parts[0]
        middle = parts[1]
        suffix = parts[2]
        # Early return if middle is longer than s
        if len(prefix) + len(suffix) > len(s):
            return -1
        n = len(s)
        # Initialize pointers for prefix and suffix
        min_len = float('inf')
        start = 0
        prefix_len = len(prefix)
        suffix_len = len(suffix)
        # Attempt to find the prefix and suffix
        for start in range(n - prefix_len + 1):
            if s[start:start + prefix_len] == prefix:
                # Now find the suffix after matching the prefix
                for end in range(n, start + prefix_len + len(middle), -1):
                    if s[end - suffix_len:end] == suffix:
                        # Valid substring from start to end
                        current_len = end - start
                        if current_len < min_len:
                            min_len = current_len
        return min_len if min_len != float('inf') else -1