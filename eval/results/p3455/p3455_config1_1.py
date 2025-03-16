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
    # Split the pattern based on '*'
    parts = p.split('*')
    prefix = parts[0]
    middle = parts[1]
    suffix = parts[2]
    min_length = float('inf')
    # Iterate through s to find the match
    i = 0
    while i <= len(s):
        # Check if the prefix matches
        if s.startswith(prefix, i):
            j = i + len(prefix)
            # Find the first occurrence of suffix after the prefix
            k = s.find(suffix, j)
            # Ensure that the middle part is between prefix and suffix
            while k != -1:
                if middle in s[j:k]:
                    match_length = k + len(suffix) - i
                    min_length = min(min_length, match_length)
                    break
                k = s.find(suffix, k + 1)
        i += 1
    return min_length if min_length != float('inf') else -1
shortestMatchingSubstring(s='abaacbaecebce', p='ba*c*ce')