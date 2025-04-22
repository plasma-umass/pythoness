import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """
        Find the length of the shortest substring in a given string `s` that matches a pattern `p`, where `p` contains exactly two '*' characters, which can match any sequence of zero or more characters. Return the length of the shortest matching substring or -1 if no such substring exists. The empty substring is considered valid.
        """
        if p.count('*') != 2:
            # Pattern must contain exactly two '*' characters; return -1 otherwise
            return -1
        start_star = p.index('*')
        end_star = p.index('*', start_star + 1)
        # Parts of the pattern split by '*'
        start_pattern = p[:start_star]
        mid_pattern = p[start_star + 1:end_star]
        end_pattern = p[end_star + 1:]
        min_length = float('inf')
        found = False
        for i in range(len(s)):
            if s[i:].startswith(start_pattern):
                for j in range(i, len(s)):
                    if s[j:].endswith(end_pattern):
                        # Calculate the substring in s from i to j that matches the pattern
                        sub = s[i:j]
                        # Check if mid_pattern is in the portion we assume as middle match
                        if mid_pattern in sub[len(start_pattern):len(sub) - len(end_pattern)]:
                            found = True
                            min_length = min(min_length, len(sub))
        return min_length if found else -1