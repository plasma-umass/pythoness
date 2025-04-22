import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """
        Find the length of the shortest substring in a given string `s` that matches a pattern `p`, where `p` contains exactly two '*' characters, which can match any sequence of zero or more characters. Return the length of the shortest matching substring or -1 if no such substring exists. The empty substring is considered valid.
        """
        if len(p) < 2 or p.count('*') != 2:
            return -1
        # Split the pattern on '*' to handle the fixed parts
        parts = p.split('*')
        pre_pattern = parts[0]
        suf_pattern = parts[2] if len(parts) > 2 else ''
        if not pre_pattern and (not suf_pattern):
            return 0  # Pattern is "**", so matches any substring
        min_length = float('inf')
        start_index = 0
        n = len(s)
        while start_index <= n:
            # Find the start matching pre_pattern
            if pre_pattern:
                start_pos = s.find(pre_pattern, start_index)
                if start_pos == -1:
                    break
                start_index = start_pos + len(pre_pattern)
            else:
                start_pos = start_index
            # From the start of the suffix part after matching prefix
            if suf_pattern:
                end_pos = s.find(suf_pattern, start_index)
                if end_pos == -1:
                    break
            else:
                end_pos = n
            # Calculate the matching substring
            if start_pos <= end_pos:
                min_length = min(min_length, end_pos - start_pos + len(suf_pattern))
            # Move start index forward for the next possible match
            start_index = start_pos + 1
        return min_length if min_length != float('inf') else -1