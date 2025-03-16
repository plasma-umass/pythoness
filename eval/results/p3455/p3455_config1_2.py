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
    segments = p.split('*')
    pre = segments[0]
    mid = segments[1]
    post = segments[2]
    n = len(s)
    len_pre = len(pre)
    len_mid = len(mid)
    len_post = len(post)
    # Initialize variables
    min_len = float('inf')
    (i, j) = (0, 0)
    # Traverse through each possible starting position
    while i < n:
        # Check if we can find 'pre' starting from i
        if len_pre > 0 and s[i:i + len_pre] != pre:
            i += 1
            continue
        # Find substring from pre to post which also includes mid
        j = i + len_pre
        # Edge case where mid is empty
        if len_mid == 0:
            k = j
        else:
            # Find where mid starts after pre
            k = s.find(mid, j, n)
        if k == -1:
            i += 1
            continue
        # Find where post starts after mid
        l = s.find(post, k + len_mid, n)
        if l == -1:
            i += 1
            continue
        # Calculate and update minimum length
        span_len = l + len_post - i
        if span_len < min_len:
            min_len = span_len
        i += 1
    # If min_len is unchanged, no valid substring found
    return min_len if min_len != float('inf') else -1
shortestMatchingSubstring(s='abaacbaecebce', p='ba*c*ce')