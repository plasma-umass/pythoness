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
    # Split the pattern into its components
    parts = p.split('*')
    (prefix, middle, suffix) = (parts[0], parts[1], parts[2])

    def find_occurrences(substr: str, string: str) -> list:
        """ Helper function to find all occurrences of a substring in a string. """
        occurrences = []
        start = 0
        while start <= len(string):
            start = string.find(substr, start)
            if start == -1:
                break
            occurrences.append(start)
            start += 1
        return occurrences
    # Find all occurrences of prefix in s
    prefix_indices = find_occurrences(prefix, s)
    min_len = float('inf')
    for start_idx in prefix_indices:
        # Start searching from the end of the prefix substring
        search_start = start_idx + len(prefix)
        # Check for the middle part
        middle_idx = s.find(middle, search_start)
        if middle_idx == -1:
            continue
        # Start checking for the suffix after the middle part
        suffix_idx = s.find(suffix, middle_idx + len(middle))
        if suffix_idx == -1:
            continue
        # Calculate the total length of this matching substring
        substr_length = suffix_idx + len(suffix) - start_idx
        min_len = min(min_len, substr_length)
    return min_len if min_len != float('inf') else -1
shortestMatchingSubstring(s='abaacbaecebce', p='ba*c*ce')