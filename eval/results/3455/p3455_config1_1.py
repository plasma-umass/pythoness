import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """
        Find the length of the shortest substring in string `s` that matches the pattern `p`, where `p` contains exactly two '*' characters, each matching any sequence of characters. If no such substring exists, return -1. The empty substring is valid.
    
        Constraints: 1 <= s.length <= 10^5, 2 <= p.length <= 10^5, `s` contains only lowercase English letters, and `p` contains only lowercase English letters with exactly two '*'.
        """
        # Split the pattern p into three parts based on '*'
        parts = p.split('*')
        if len(parts) != 3:
            return -1
        (part1, part2, part3) = parts
        # Initialize the minimum length to be a large number
        min_length = float('inf')
        # Track start and end positions
        start = 0
        # Iterate over the string s
        while start < len(s):
            # Try to find a starting match for part1
            start_index = s.find(part1, start)
            if start_index == -1:
                break
            # For a valid beginning, check the end indices
            # so that it matches part3
            end_index = start_index + len(part1)
            sub_start = end_index
            # Try to match part2 anywhere after part1
            sub_index = s.find(part2, sub_start)
            while sub_index != -1:
                sub_end = sub_index + len(part2)
                end_index_full = s.find(part3, sub_end)
                if end_index_full != -1:
                    total_length = end_index_full + len(part3) - start_index
                    min_length = min(min_length, total_length)
                sub_index = s.find(part2, sub_index + 1)
            start = start_index + 1
        return -1 if min_length == float('inf') else min_length