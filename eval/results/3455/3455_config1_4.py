import pythoness
from typing import List, Optional

def shortestMatchingSubstring(s: str, p: str) -> int:
    """
    You are given a string s and a pattern string p, where p contains exactly two '*' characters.
    The '*' in p matches any sequence of zero or more characters.
    Return the length of the shortest substring in s that matches p. If there is no such substring, return -1.
    Note: The empty substring is considered valid.

    Constraints:

    1 <= s.length <= 10^5
    2 <= p.length <= 10^5
    s contains only lowercase English letters.
    p contains only lowercase English letters and exactly two '*'.
    """
    # Split pattern on '*'. This gives us three parts: prefix, infix and suffix
    (prefix, rest) = p.split('*', 1)
    (infix, suffix) = rest.rsplit('*', 1)
    n = len(s)
    min_length = float('inf')
    left = 0
    while left < n:
        # Find the first substring in `s` starting from `left` that matches the `prefix`
        if s[left:].startswith(prefix):
            # Start looking for the `suffix` from the end
            right = left + len(prefix)
            while right <= n:
                # If suffix is found and the infix can be anything, check for the match
                if s[right:].startswith(suffix):
                    # Check if the middle part is within the large substring
                    if infix in s[left + len(prefix):right]:
                        # Calculate total length of this substring
                        total_length = right + len(suffix) - left
                        min_length = min(min_length, total_length)
                        break
                # Move right pointer one step to the right
                right += 1
        # Move left pointer forward
        left += 1
    return min_length if min_length != float('inf') else -1
shortestMatchingSubstring(s='abaacbaecebce', p='ba*c*ce')