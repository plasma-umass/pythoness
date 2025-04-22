import pythoness
from typing import List, Optional

class Solution:
    
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        """
        Find the length of the shortest substring in a given string `s` that matches a pattern `p`, where `p` contains exactly two '*' characters, which can match any sequence of zero or more characters. Return the length of the shortest matching substring or -1 if no such substring exists. The empty substring is considered valid.
        """
        # Splitting the pattern into three parts by separating at '*'
        parts = p.split('*')
        if len(parts) != 3:
            return -1  # Invalid pattern, as it must contain exactly two '*'
        (start, mid, end) = parts
        n = len(s)
        shortest = float('inf')  # Initialize shortest length as infinity
        # Iterate over the string to find potential matches
        for i in range(n):
            # Check if the prefix matches
            if s[i:i + len(start)] == start:
                # Now look for a potential end that can make the mid part valid
                for j in range(i + len(start), n):
                    # Check if the suffix matches
                    if s[j:j + len(end)] == end:
                        # Check if the middle part is there between these
                        if mid in s[i + len(start):j]:
                            # Update shortest length
                            shortest = min(shortest, j - i + len(end))
        # If shortest is not updated, return -1, else return shortest length found
        return -1 if shortest == float('inf') else shortest