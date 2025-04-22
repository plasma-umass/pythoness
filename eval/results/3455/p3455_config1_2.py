import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """Find the length of the shortest substring in a given string `s` that matches a pattern `p`, where `p` contains exactly two '*' characters, which can match any sequence of zero or more characters. Return the length of the shortest matching substring or -1 if no such substring exists. The empty substring is considered valid."""
        if p.count('*') != 2:
            return -1
        # Split the pattern p by the '*' characters
        parts = p.split('*')
        # Define a function to check if a given substring matches the pattern
    
        def matches(sub: str) -> bool:
            # Attempt to match the start, middle, and end of the pattern to the substring
            # If the total length of parts exceeds the substring length, matching is impossible.
            if len(parts[0]) + len(parts[1]) + len(parts[2]) > len(sub):
                return False
            return sub.startswith(parts[0]) and sub.endswith(parts[2]) and (parts[1] in sub[len(parts[0]):len(sub) - len(parts[2])])
        # Initialize the length for shortest matching substring
        shortest_length = len(s) + 1
        # Iterate over all possible substrings of s
        for start in range(len(s)):
            for end in range(start, len(s) + 1):
                substring = s[start:end]
                if matches(substring):
                    shortest_length = min(shortest_length, end - start)
        return shortest_length if shortest_length <= len(s) else -1