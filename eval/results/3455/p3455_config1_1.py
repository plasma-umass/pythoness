import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """
        Find the length of the shortest substring in a given string `s` that matches a pattern `p`, where `p` contains exactly two '*' characters, which can match any sequence of zero or more characters. Return the length of the shortest matching substring or -1 if no such substring exists. The empty substring is considered valid.
        """
    
        def matches(sub: str, pattern: str) -> bool:
            parts = pattern.split('*')
            if len(parts) != 3:
                return False
            (prefix, middle, suffix) = parts
            if not sub.startswith(prefix):
                return False
            if not sub.endswith(suffix):
                return False
            start = len(prefix)
            end = len(sub) - len(suffix)
            return middle in sub[start:end]
        min_length = float('inf')
        pattern_parts = p.split('*')
        if len(pattern_parts) != 3:
            return -1
        (prefix, middle, suffix) = pattern_parts
        for start in range(len(s) + 1):
            for end in range(start, len(s) + 1):
                substring = s[start:end]
                if matches(substring, p):
                    min_length = min(min_length, len(substring))
        return min_length if min_length != float('inf') else -1