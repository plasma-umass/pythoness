import pythoness
from typing import List, Optional

def isMatch(s: str, p: str) -> bool:
    """
    Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:

    '?' Matches any single character.
    '*' Matches any sequence of characters (including the empty sequence).

    The matching should cover the entire input string (not partial).

    Constraints:

    0 <= s.length, p.length <= 2000
    s contains only lowercase English letters.
    p contains only lowercase English letters, '?' or '*'.
    """
    # dp[i][j] will be True if first i characters in the given string matches the first j characters of the pattern
    dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
    # An empty string and an empty pattern are a match
    dp[0][0] = True
    # Initialize dp table for patterns with '*' which can match empty string
    for j in range(1, len(p) + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
    for i in range(1, len(s) + 1):
        for j in range(1, len(p) + 1):
            if p[j - 1] == '?' or p[j - 1] == s[i - 1]:
                # If the pattern character is '?' or matches the string character
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                # '*' can be treated as empty or can match one more character
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
    return dp[len(s)][len(p)]
isMatch(s='aa', p='a')