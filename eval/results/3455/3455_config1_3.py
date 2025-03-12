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
    first_star = p.index('*')
    last_star = p.rindex('*')
    l_pattern = p[:first_star]
    m_pattern = p[first_star + 1:last_star]
    r_pattern = p[last_star + 1:]
    min_length = float('inf')
    i = 0
    while i <= len(s):
        if s[i:].startswith(l_pattern):
            start_idx = i + len(l_pattern)
            middle_start = s.find(m_pattern, start_idx)
            if middle_start != -1:
                end_idx = middle_start + len(m_pattern)
                r_start = s.find(r_pattern, end_idx)
                if r_start != -1:
                    length = r_start + len(r_pattern) - i
                    min_length = min(min_length, length)
        i += 1
    return min_length if min_length != float('inf') else -1
shortestMatchingSubstring(s='abaacbaecebce', p='ba*c*ce')