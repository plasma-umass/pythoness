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
    # Initialize a DP table with False
    dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
    # Empty pattern matches empty string
    dp[0][0] = True
    # Fill the first row for matching patterns with empty s
    for j in range(1, len(p) + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
    # Fill the DP table
    for i in range(1, len(s) + 1):
        for j in range(1, len(p) + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[len(s)][len(p)]
isMatch(s='aa', p='a')